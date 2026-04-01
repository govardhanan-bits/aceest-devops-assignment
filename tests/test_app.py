"""
Unit tests for ACEest Fitness Application
Tests all endpoints and core functionality
"""

import pytest
import json
import os
import sys
import tempfile

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, init_db


@pytest.fixture
def client():
    """Create test client with temporary database"""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    
    # Temporarily override DATABASE environment variable
    os.environ['DB_PATH'] = db_path
    
    # Initialize database
    init_db()
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


class TestHomeEndpoint:
    """Tests for home endpoint"""
    
    def test_home_endpoint_success(self, client):
        """Test home endpoint returns success"""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'application' in data
        assert 'ACEest' in data['application']
        assert data['status'] == 'Running'
        assert 'version' in data


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_endpoint_success(self, client):
        """Test health endpoint returns healthy status"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'database' in data
        assert 'timestamp' in data
    
    def test_health_endpoint_database_check(self, client):
        """Test health endpoint checks database connectivity"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['database'] == 'connected' or 'error' in data['database']


class TestClientsEndpoint:
    """Tests for clients endpoint"""
    
    def test_get_all_clients_success(self, client):
        """Test getting all clients returns success"""
        response = client.get('/clients')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'clients' in data
        assert 'count' in data
        assert data['count'] >= 0
    
    def test_get_all_clients_structure(self, client):
        """Test clients response has correct structure"""
        response = client.get('/clients')
        data = json.loads(response.data)
        
        if data['count'] > 0:
            client_data = data['clients'][0]
            assert 'id' in client_data
            assert 'name' in client_data
            assert 'program' in client_data
    
    def test_get_specific_client_success(self, client):
        """Test getting specific client by ID"""
        # First, get all clients to find a valid ID
        response = client.get('/clients')
        data = json.loads(response.data)
        
        if data['count'] > 0:
            client_id = data['clients'][0]['id']
            response = client.get(f'/clients/{client_id}')
            assert response.status_code == 200
            
            client_data = json.loads(response.data)
            assert client_data['id'] == client_id
    
    def test_get_nonexistent_client(self, client):
        """Test getting client that doesn't exist returns 404"""
        response = client.get('/clients/99999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_client_success(self, client):
        """Test creating new client"""
        new_client = {
            'name': 'Test User',
            'program': 'Fat Loss',
            'age': 30,
            'goal': 'Lose weight'
        }
        
        response = client.post(
            '/clients',
            data=json.dumps(new_client),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'client_id' in data
        assert data['message'] == 'Client created successfully'
    
    def test_create_client_missing_fields(self, client):
        """Test creating client with missing required fields"""
        incomplete_client = {
            'name': 'Test User'
            # Missing 'program' field
        }
        
        response = client.post(
            '/clients',
            data=json.dumps(incomplete_client),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestProgramsEndpoint:
    """Tests for programs endpoint"""
    
    def test_get_programs_success(self, client):
        """Test getting fitness programs"""
        response = client.get('/programs')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'programs' in data
        assert 'count' in data
        assert data['count'] > 0
    
    def test_programs_structure(self, client):
        """Test programs have correct structure"""
        response = client.get('/programs')
        data = json.loads(response.data)
        
        program = data['programs'][0]
        assert 'name' in program
        assert 'description' in program
        assert 'duration' in program
        assert 'difficulty' in program


class TestStatsEndpoint:
    """Tests for statistics endpoint"""
    
    def test_get_stats_success(self, client):
        """Test getting application statistics"""
        response = client.get('/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'total_clients' in data
        assert 'programs_breakdown' in data
    
    def test_stats_structure(self, client):
        """Test statistics have correct structure"""
        response = client.get('/stats')
        data = json.loads(response.data)
        
        assert isinstance(data['total_clients'], int)
        assert isinstance(data['programs_breakdown'], list)


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data


class TestDatabaseIntegration:
    """Integration tests for database operations"""
    
    def test_database_initialization(self, client):
        """Test database initializes with sample data"""
        response = client.get('/clients')
        data = json.loads(response.data)
        
        # Should have sample data
        assert data['count'] >= 5
    
    def test_create_and_retrieve_client(self, client):
        """Test creating and retrieving a client"""
        # Create client
        new_client = {
            'name': 'Integration Test User',
            'program': 'Muscle Gain',
            'age': 25,
            'goal': 'Build muscle'
        }
        
        create_response = client.post(
            '/clients',
            data=json.dumps(new_client),
            content_type='application/json'
        )
        
        assert create_response.status_code == 201
        client_id = json.loads(create_response.data)['client_id']
        
        # Retrieve client
        get_response = client.get(f'/clients/{client_id}')
        assert get_response.status_code == 200
        
        client_data = json.loads(get_response.data)
        assert client_data['name'] == new_client['name']
        assert client_data['program'] == new_client['program']


# Run tests with coverage if executed directly
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=app', '--cov-report=html', '--cov-report=term'])
