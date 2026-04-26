"""
Pytest test cases for ACEest Fitness & Gym Flask Application.
"""
import pytest
import os
import tempfile
from app import app, init_db, get_db, PROGRAMS


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    db_fd, db_path = tempfile.mkstemp()
    app.config["TESTING"] = True
    os.environ["DB_NAME"] = db_path

    # Re-import to pick up new DB_NAME
    import app as app_module
    app_module.DB_NAME = db_path
    init_db()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def logged_in_client(client):
    """Return a test client that is already logged in."""
    client.post("/login", data={"username": "admin", "password": "admin"})
    return client


# ---------- HEALTH CHECK TESTS ----------
class TestHealthCheck:
    def test_health_endpoint(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["version"] == "3.2.4"

    def test_health_has_timestamp(self, client):
        response = client.get("/api/health")
        data = response.get_json()
        assert "timestamp" in data


# ---------- AUTH TESTS ----------
class TestAuthentication:
    def test_login_page_loads(self, client):
        response = client.get("/login")
        assert response.status_code == 200

    def test_login_success(self, client):
        response = client.post("/login", data={
            "username": "admin", "password": "admin"
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_login_failure(self, client):
        response = client.post("/login", data={
            "username": "wrong", "password": "wrong"
        }, follow_redirects=True)
        assert b"Invalid credentials" in response.data

    def test_login_empty_fields(self, client):
        response = client.post("/login", data={
            "username": "", "password": ""
        }, follow_redirects=True)
        assert b"Username and password required" in response.data

    def test_logout(self, logged_in_client):
        response = logged_in_client.get("/logout", follow_redirects=True)
        assert response.status_code == 200

    def test_dashboard_requires_login(self, client):
        response = client.get("/dashboard", follow_redirects=True)
        assert b"Please log in first" in response.data


# ---------- DASHBOARD TESTS ----------
class TestDashboard:
    def test_dashboard_loads(self, logged_in_client):
        response = logged_in_client.get("/dashboard")
        assert response.status_code == 200
        assert b"Client Dashboard" in response.data

    def test_dashboard_shows_programs_count(self, logged_in_client):
        response = logged_in_client.get("/dashboard")
        assert response.status_code == 200


# ---------- CLIENT MANAGEMENT TESTS ----------
class TestClientManagement:
    def test_add_client_page_loads(self, logged_in_client):
        response = logged_in_client.get("/client/add")
        assert response.status_code == 200

    def test_add_client_success(self, logged_in_client):
        response = logged_in_client.post("/client/add", data={
            "name": "Test User",
            "age": 25,
            "weight": 75.0,
            "height": 175.0,
            "program": "Fat Loss (FL)",
            "target_weight": 70.0,
            "target_adherence": 80,
            "membership_end": "2026-12-31"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Test User" in response.data

    def test_add_client_missing_fields(self, logged_in_client):
        response = logged_in_client.post("/client/add", data={
            "name": "",
            "program": ""
        }, follow_redirects=True)
        assert b"Name and program are required" in response.data

    def test_view_client(self, logged_in_client):
        # Add a client first
        logged_in_client.post("/client/add", data={
            "name": "View Test",
            "age": 30,
            "weight": 80.0,
            "program": "Muscle Gain (MG)"
        })
        response = logged_in_client.get("/client/1")
        assert response.status_code == 200
        assert b"View Test" in response.data

    def test_view_nonexistent_client(self, logged_in_client):
        response = logged_in_client.get("/client/9999", follow_redirects=True)
        assert b"Client not found" in response.data

    def test_calorie_calculation(self, logged_in_client):
        logged_in_client.post("/client/add", data={
            "name": "Calorie Test",
            "weight": 80.0,
            "program": "Fat Loss (FL)"  # factor=22
        })
        response = logged_in_client.get("/client/1")
        assert b"1760 kcal" in response.data  # 80 * 22 = 1760


# ---------- PROGRESS TESTS ----------
class TestProgress:
    def test_log_progress(self, logged_in_client):
        # Add client first
        logged_in_client.post("/client/add", data={
            "name": "Progress Test",
            "weight": 70.0,
            "program": "Beginner (BG)"
        })
        response = logged_in_client.post("/client/1/progress", data={
            "adherence": 85
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Progress logged" in response.data

    def test_log_workout(self, logged_in_client):
        logged_in_client.post("/client/add", data={
            "name": "Workout Test",
            "weight": 70.0,
            "program": "Beginner (BG)"
        })
        response = logged_in_client.post("/client/1/workout", data={
            "workout_date": "2025-04-18",
            "workout_type": "Strength",
            "duration": 60,
            "notes": "Good session"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Workout logged" in response.data


# ---------- PROGRAMS TESTS ----------
class TestPrograms:
    def test_programs_page_loads(self, logged_in_client):
        response = logged_in_client.get("/programs")
        assert response.status_code == 200

    def test_all_programs_exist(self):
        assert "Fat Loss (FL)" in PROGRAMS
        assert "Muscle Gain (MG)" in PROGRAMS
        assert "Beginner (BG)" in PROGRAMS

    def test_program_has_required_fields(self):
        for name, data in PROGRAMS.items():
            assert "workout" in data
            assert "diet" in data
            assert "calorie_factor" in data

    def test_calorie_factors_positive(self):
        for name, data in PROGRAMS.items():
            assert data["calorie_factor"] > 0


# ---------- API TESTS ----------
class TestAPI:
    def test_api_clients_empty(self, logged_in_client):
        response = logged_in_client.get("/api/clients")
        assert response.status_code == 200
        assert response.get_json() == []

    def test_api_clients_with_data(self, logged_in_client):
        logged_in_client.post("/client/add", data={
            "name": "API Test",
            "weight": 65.0,
            "program": "Beginner (BG)"
        })
        response = logged_in_client.get("/api/clients")
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["name"] == "API Test"

    def test_api_progress_empty(self, logged_in_client):
        logged_in_client.post("/client/add", data={
            "name": "Progress API",
            "weight": 65.0,
            "program": "Beginner (BG)"
        })
        response = logged_in_client.get("/api/client/1/progress")
        assert response.status_code == 200
        assert response.get_json() == []

    def test_api_requires_auth(self, client):
        response = client.get("/api/clients", follow_redirects=True)
        assert b"Please log in first" in response.data


# ---------- REDIRECT TESTS ----------
class TestRedirects:
    def test_root_redirects_to_login(self, client):
        response = client.get("/")
        assert response.status_code == 302
