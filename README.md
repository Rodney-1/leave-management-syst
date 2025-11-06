# Leave Management System

A sipmle full-stack web application for managing employee leave requests.

## Features

- **User Authentication**: Secure login and registration
- **Role-based Access**: Separate dashboards for employees and admins
- **Leave Requests**: Employees can submit leave requests with dates and reasons
- **Admin Approval**: Admins can approve or reject leave requests
- **Real-time Updates**: Dashboard updates after actions


## Live Demo

- **Frontend**: https://leavesyst.netlify.app/
- **Backend API**: https://leave-management-syst.onrender.com/

## Demo Credentials

- **Admin**: admin@company.com / admin123
- **Employee**: john@company.com / employee123

## Setup Instructions

### Prerequisites

- Python 3.8
- Node.js 22
- npm

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install Flask Flask_SQLAlchemy Flask-Cors Flask-JWT-Extended SQLAchemy
      #then 
   pip freeze > requirements.txt
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

3. Run the build first:
   ```bash
   npm run build
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at http://localhost:5173

## Usage

1. Open your browser and go to http://localhost:5173
2. Login with demo credentials or register a new account
3. As an employee: Submit leave requests and view your request history
4. As an admin: View all leave requests and approve/reject them

