"""
ACEest Fitness & Gym - Flask Web Application
Version: 3.2.4
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import sqlite3
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "aceest-fitness-secret-key-2025")

DB_NAME = os.environ.get("DB_NAME", "aceest_fitness.db")

# ---------- PROGRAMS DATA ----------
PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: Back Squat 5x5 + Core | Tue: EMOM 20min Assault Bike | "
                   "Wed: Bench Press + 21-15-9 | Thu: Deadlift + Box Jumps | Fri: Zone 2 Cardio 30min",
        "diet": "Breakfast: Egg Whites + Oats | Lunch: Grilled Chicken + Brown Rice | "
                "Dinner: Fish Curry + Millet Roti | Target: ~2000 kcal",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5 | Tue: Bench 5x5 | Wed: Deadlift 4x6 | "
                   "Thu: Front Squat 4x8 | Fri: Incline Press 4x10 | Sat: Barbell Rows 4x10",
        "diet": "Breakfast: Eggs + Peanut Butter Oats | Lunch: Chicken Biryani | "
                "Dinner: Mutton Curry + Rice | Target: ~3200 kcal",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": "Full Body Circuit: Air Squats, Ring Rows, Push-ups | "
                   "Focus: Technique & Consistency",
        "diet": "Balanced Tamil Meals: Idli / Dosa / Rice + Dal | Protein Target: 120g/day",
        "calorie_factor": 26
    }
}


# ---------- DATABASE ----------
def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'trainer'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            weight REAL,
            height REAL,
            program TEXT,
            calories INTEGER,
            target_weight REAL,
            target_adherence INTEGER DEFAULT 80,
            membership_status TEXT DEFAULT 'active',
            membership_end TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            week TEXT,
            adherence INTEGER,
            logged_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            workout_date TEXT,
            workout_type TEXT,
            duration INTEGER,
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)

    # Insert default admin user if not exists
    cur.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin", "admin")
        )

    conn.commit()
    conn.close()


# ---------- AUTH DECORATOR ----------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ---------- ROUTES ----------
@app.route("/")
def index():
    """Landing page."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password required.", "danger")
            return render_template("login.html")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = username
            session["role"] = user["role"]
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """User logout."""
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Main dashboard showing all clients."""
    conn = get_db()
    clients = conn.execute("SELECT * FROM clients ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("dashboard.html", clients=clients, programs=PROGRAMS)


@app.route("/client/add", methods=["GET", "POST"])
@login_required
def add_client():
    """Add a new client."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", type=int)
        weight = request.form.get("weight", type=float)
        height = request.form.get("height", type=float)
        program = request.form.get("program", "")
        target_weight = request.form.get("target_weight", type=float)
        target_adherence = request.form.get("target_adherence", type=int, default=80)
        membership_end = request.form.get("membership_end", "")

        if not name or not program:
            flash("Name and program are required.", "danger")
            return render_template("add_client.html", programs=PROGRAMS)

        calories = int(weight * PROGRAMS[program]["calorie_factor"]) if weight and program in PROGRAMS else 0

        conn = get_db()
        try:
            conn.execute(
                """INSERT INTO clients
                   (name, age, weight, height, program, calories, target_weight,
                    target_adherence, membership_end)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, age, weight, height, program, calories,
                 target_weight, target_adherence, membership_end)
            )
            conn.commit()
            flash(f"Client '{name}' added successfully.", "success")
        except sqlite3.IntegrityError:
            flash("Error adding client.", "danger")
        finally:
            conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_client.html", programs=PROGRAMS)


@app.route("/client/<int:client_id>")
@login_required
def view_client(client_id):
    """View client profile and progress."""
    conn = get_db()
    client = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
    if not client:
        flash("Client not found.", "danger")
        conn.close()
        return redirect(url_for("dashboard"))

    progress = conn.execute(
        "SELECT * FROM progress WHERE client_id=? ORDER BY logged_at DESC",
        (client_id,)
    ).fetchall()

    workouts = conn.execute(
        "SELECT * FROM workouts WHERE client_id=? ORDER BY workout_date DESC LIMIT 10",
        (client_id,)
    ).fetchall()

    conn.close()

    program_data = PROGRAMS.get(client["program"], {})
    return render_template(
        "client.html",
        client=client,
        progress=progress,
        workouts=workouts,
        program_data=program_data
    )


@app.route("/client/<int:client_id>/progress", methods=["POST"])
@login_required
def log_progress(client_id):
    """Log weekly adherence progress."""
    adherence = request.form.get("adherence", type=int)
    week = datetime.now().strftime("Week %U - %Y")

    conn = get_db()
    conn.execute(
        "INSERT INTO progress (client_id, week, adherence) VALUES (?, ?, ?)",
        (client_id, week, adherence)
    )
    conn.commit()
    conn.close()

    flash("Progress logged.", "success")
    return redirect(url_for("view_client", client_id=client_id))


@app.route("/client/<int:client_id>/workout", methods=["POST"])
@login_required
def log_workout(client_id):
    """Log a workout session."""
    workout_date = request.form.get("workout_date", datetime.now().strftime("%Y-%m-%d"))
    workout_type = request.form.get("workout_type", "")
    duration = request.form.get("duration", type=int, default=0)
    notes = request.form.get("notes", "")

    conn = get_db()
    conn.execute(
        "INSERT INTO workouts (client_id, workout_date, workout_type, duration, notes) VALUES (?, ?, ?, ?, ?)",
        (client_id, workout_date, workout_type, duration, notes)
    )
    conn.commit()
    conn.close()

    flash("Workout logged.", "success")
    return redirect(url_for("view_client", client_id=client_id))


@app.route("/programs")
@login_required
def programs():
    """Display all fitness programs."""
    return render_template("programs.html", programs=PROGRAMS)


# ---------- API ENDPOINTS ----------
@app.route("/api/health")
def health_check():
    """Health check endpoint for Kubernetes probes."""
    return jsonify({"status": "healthy", "version": "3.2.4", "timestamp": datetime.now().isoformat()})


@app.route("/api/clients")
@login_required
def api_clients():
    """API: List all clients."""
    conn = get_db()
    clients = conn.execute("SELECT id, name, age, weight, program, calories, membership_status FROM clients").fetchall()
    conn.close()
    return jsonify([dict(c) for c in clients])


@app.route("/api/client/<int:client_id>/progress")
@login_required
def api_client_progress(client_id):
    """API: Get client progress data."""
    conn = get_db()
    progress = conn.execute(
        "SELECT week, adherence FROM progress WHERE client_id=? ORDER BY logged_at",
        (client_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(p) for p in progress])


# ---------- MAIN ----------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
