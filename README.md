# Clubbers - Social Club Management App

A Flutter application with Python backend for managing social clubs and user profiles.

## Project Structure

```
clubbers/
├── frontend/           # Flutter application
│   ├── lib/           # Flutter source code
│   └── assets/        # Images, fonts, etc.
└── backend/           # Python backend
    ├── app/           # Main application code
    ├── config/        # Configuration files
    └── requirements.txt # Python dependencies
```

## Setup Instructions

### Frontend (Flutter)
1. Ensure Flutter is installed on your system
2. Navigate to the frontend directory
3. Run `flutter pub get` to install dependencies
4. Run `flutter run` to start the application

### Backend (Python)
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database:
   - Create a PostgreSQL database
   - Update database configuration in `backend/config/database.py`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## Features
- Light and Dark theme support
- User authentication (Login/Registration)
- Profile management with image upload
- Splash screen
- Home screen with user information
- Secure API endpoints
- PostgreSQL database integration 