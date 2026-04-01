"""
ACEest Fitness Application - DevOps Implementation
A Flask-based web service for fitness program management
"""

from flask import Flask, jsonify, request
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Configuration
DATABASE = os.getenv('DB_PATH', 'data/aceest_fitness.db')

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with sample data"""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            age INTEGER,
            goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if table is empty and add sample data
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        sample_clients = [
            ('Ravi Kumar', 'Fat Loss', 32, 'Lose 10kg'),
            ('Anita Sharma', 'Muscle Gain', 28, 'Build strength'),
            ('John Doe', 'Beginner', 25, 'General fitness'),
            ('Priya Patel', 'Fat Loss', 35, 'Tone and lose weight'),
            ('Mike Johnson', 'Athletic Performance', 30, 'Improve endurance')
        ]
        cursor.executemany(
            'INSERT INTO clients (name, program, age, goal) VALUES (?, ?, ?, ?)',
            sample_clients
        )
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """Root endpoint - Application status"""
    return jsonify({
        'application': 'ACEest Fitness DevOps Application',
        'status': 'Running',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint for monitoring and load balancers"""
    try:
        # Check database connectivity
        conn = get_db_connection()
        conn.execute('SELECT 1')
        conn.close()
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/clients', methods=['GET'])
def get_clients():
    """Get all clients with their fitness programs"""
    try:
        conn = get_db_connection()
        clients = conn.execute('SELECT * FROM clients').fetchall()
        conn.close()
        
        clients_list = [
            {
                'id': client['id'],
                'name': client['name'],
                'program': client['program'],
                'age': client['age'],
                'goal': client['goal'],
                'created_at': client['created_at']
            }
            for client in clients
        ]
        
        return jsonify({
            'count': len(clients_list),
            'clients': clients_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Get specific client by ID"""
    try:
        conn = get_db_connection()
        client = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,)).fetchone()
        conn.close()
        
        if client is None:
            return jsonify({'error': 'Client not found'}), 404
        
        return jsonify({
            'id': client['id'],
            'name': client['name'],
            'program': client['program'],
            'age': client['age'],
            'goal': client['goal'],
            'created_at': client['created_at']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clients', methods=['POST'])
def create_client():
    """Create a new client"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'program' not in data:
            return jsonify({'error': 'Missing required fields: name, program'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO clients (name, program, age, goal) VALUES (?, ?, ?, ?)',
            (data['name'], data['program'], data.get('age'), data.get('goal'))
        )
        conn.commit()
        client_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'message': 'Client created successfully',
            'client_id': client_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/programs', methods=['GET'])
def get_programs():
    """Get available fitness programs"""
    programs = [
        {
            'name': 'Fat Loss',
            'description': 'Weight loss and body composition improvement',
            'duration': '12 weeks',
            'difficulty': 'Intermediate'
        },
        {
            'name': 'Muscle Gain',
            'description': 'Strength building and muscle hypertrophy',
            'duration': '16 weeks',
            'difficulty': 'Advanced'
        },
        {
            'name': 'Beginner',
            'description': 'Introduction to fitness and basic exercises',
            'duration': '8 weeks',
            'difficulty': 'Beginner'
        },
        {
            'name': 'Athletic Performance',
            'description': 'Sports-specific training and conditioning',
            'duration': '12 weeks',
            'difficulty': 'Advanced'
        }
    ]
    
    return jsonify({
        'count': len(programs),
        'programs': programs
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    try:
        conn = get_db_connection()
        
        total_clients = conn.execute('SELECT COUNT(*) FROM clients').fetchone()[0]
        
        programs_breakdown = conn.execute('''
            SELECT program, COUNT(*) as count 
            FROM clients 
            GROUP BY program
        ''').fetchall()
        
        conn.close()
        
        return jsonify({
            'total_clients': total_clients,
            'programs_breakdown': [
                {'program': row['program'], 'count': row['count']}
                for row in programs_breakdown
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting ACEest Fitness Application on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
