# Leave Management System

A full-stack web application for managing employee leave requests. Built with Flask (backend) and React (frontend).

## Features

- **User Authentication**: Secure login and registration
- **Role-based Access**: Separate dashboards for employees and admins
- **Leave Requests**: Employees can submit leave requests with dates and reasons
- **Admin Approval**: Admins can approve or reject leave requests
- **Real-time Updates**: Dashboard updates after actions

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended, Flask-CORS
- **Frontend**: React, React Router, Axios, Vite
- **Database**: SQLite

## Demo Credentials

- **Admin**: admin@company.com / admin123
- **Employee**: john@company.com / employee123

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python app.py
   ```
   The server will start on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at http://localhost:5173

## Usage

1. Open your browser and go to http://localhost:5173
2. Login with demo credentials or register a new account
3. As an employee: Submit leave requests and view your request history
4. As an admin: View all leave requests and approve/reject them

## API Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /leaves` - Get leave requests (filtered by role)
- `POST /leaves` - Create new leave request
- `PATCH /leaves/<id>/status` - Update leave status (admin only)
