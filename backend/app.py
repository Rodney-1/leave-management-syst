from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leave_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='employee')
    leave_requests = db.relationship('LeaveRequest', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'employee_name': self.user.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
    
# Routes
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validation
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'All fields are required'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data.get('role', 'employee')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'Registration successful',
        'user': new_user.to_dict()
    }), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'token': access_token,
        'user': user.to_dict()
    }), 200

@app.route('/leaves', methods=['GET'])
@jwt_required()
def get_leaves():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.role == 'admin':
        # Admin sees all requests
        leaves = LeaveRequest.query.all()
    else:
        # Employee sees only their requests
        leaves = LeaveRequest.query.filter_by(user_id=current_user_id).all()
    
    return jsonify([leave.to_dict() for leave in leaves]), 200

@app.route('/leaves', methods=['POST'])
@jwt_required()
def create_leave():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validation
    if not data.get('start_date') or not data.get('end_date') or not data.get('reason'):
        return jsonify({'error': 'All fields are required'}), 400
    
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    if end_date < start_date:
        return jsonify({'error': 'End date must be after start date'}), 400
    
    if not data['reason'].strip():
        return jsonify({'error': 'Reason cannot be empty'}), 400
    
    # Create leave request
    new_leave = LeaveRequest(
        user_id=current_user_id,
        start_date=start_date,
        end_date=end_date,
        reason=data['reason']
    )
    
    db.session.add(new_leave)
    db.session.commit()
    
    return jsonify({
        'message': 'Leave request created',
        'leave': new_leave.to_dict()
    }), 201

@app.route('/leaves/<int:leave_id>/status', methods=['PATCH'])
@jwt_required()
def update_leave_status(leave_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['approved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    leave = LeaveRequest.query.get(leave_id)
    if not leave:
        return jsonify({'error': 'Leave request not found'}), 404
    
    leave.status = new_status
    db.session.commit()
    
    return jsonify({
        'message': f'Leave request {new_status}',
        'leave': leave.to_dict()
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200
# Initialize database and create admin user
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        admin = User.query.filter_by(email='admin@company.com').first()
        if not admin:
            admin = User(
                name='Admin User',
                email='admin@company.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
        
        # Create default employee if not exists
        employee = User.query.filter_by(email='john@company.com').first()
        if not employee:
            employee = User(
                name='John Doe',
                email='john@company.com',
                password=generate_password_hash('employee123'),
                role='employee'
            )
            db.session.add(employee)
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)