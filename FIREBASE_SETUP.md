# Firebase Authentication Setup Guide

This guide will help you set up Firebase Authentication for the Medical Report Analyzer application.

## Prerequisites

1. A Google account
2. Node.js and npm installed
3. Python and pip installed

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter a project name (e.g., "medical-report-analyzer")
4. Choose whether to enable Google Analytics (optional)
5. Click "Create project"

## Step 2: Enable Authentication

1. In your Firebase project, go to the "Authentication" section
2. Click "Get started"
3. Go to the "Sign-in method" tab
4. Enable "Email/Password" authentication
5. Click "Save"

## Step 3: Get Firebase Configuration

1. In your Firebase project, go to "Project settings" (gear icon)
2. Scroll down to "Your apps" section
3. Click "Add app" and select the web icon (</>)
4. Register your app with a nickname (e.g., "Medical Analyzer Web")
5. Copy the Firebase configuration object

## Step 4: Configure Environment Variables

1. Copy `env.example` to `.env` in the project root
2. Fill in your Firebase configuration:

```env
# Frontend Configuration
VITE_API_BASE_URL=http://localhost:5000

# Firebase Configuration
VITE_FIREBASE_API_KEY=your_api_key_here
VITE_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

## Step 5: Backend Configuration (Optional for Production)

For production deployment, you may want to configure Firebase Admin SDK on the backend:

1. In Firebase Console, go to "Project settings" > "Service accounts"
2. Click "Generate new private key"
3. Download the JSON file
4. Set the environment variable:

```env
FIREBASE_SERVICE_ACCOUNT_PATH=path/to/your/service-account-key.json
```

Or set the JSON content directly:

```env
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

## Step 6: Install Dependencies

The Firebase dependencies are already installed:

- Frontend: `firebase` package
- Backend: `firebase-admin` package

## Step 7: Test the Integration

1. Start the development servers:
   ```bash
   # Terminal 1 - Backend
   python app.py
   
   # Terminal 2 - Frontend
   npm run dev
   ```

2. Navigate to `http://localhost:5173`
3. Try to sign up with a new account
4. Try to log in with the created account
5. Test the medical report analysis (requires authentication)

## Features Implemented

### Frontend
- ✅ Firebase Authentication integration
- ✅ Login page with Firebase auth
- ✅ Signup page with Firebase auth
- ✅ Protected routes
- ✅ User context management
- ✅ Automatic token refresh
- ✅ Error handling for auth failures

### Backend
- ✅ Firebase token verification
- ✅ Protected API endpoints
- ✅ User information extraction
- ✅ Graceful fallback for development

## API Endpoints

### Public Endpoints
- `GET /health` - Health check (no auth required)

### Protected Endpoints (require Firebase token)
- `GET /user` - Get current user information
- `POST /analyze` - Analyze medical report text
- `POST /analyze/file` - Analyze uploaded medical file

## Authentication Flow

1. User signs up/logs in through Firebase Auth
2. Frontend receives Firebase ID token
3. Frontend includes token in API requests as `Authorization: Bearer <token>`
4. Backend verifies token with Firebase Admin SDK
5. Backend processes request with user context

## Security Features

- JWT token verification
- Automatic token expiration handling
- User context isolation
- Secure API endpoints
- CORS configuration

## Troubleshooting

### Common Issues

1. **"Firebase not initialized" error**
   - Check your environment variables
   - Ensure Firebase project is properly configured

2. **"Invalid token" error**
   - Check if user is logged in
   - Verify Firebase configuration
   - Check network connectivity

3. **CORS errors**
   - Ensure backend is running on correct port
   - Check CORS configuration in Flask app

### Development vs Production

- **Development**: Backend can run without Firebase Admin SDK (with warnings)
- **Production**: Firebase Admin SDK should be properly configured for security

## Next Steps

1. Set up Firebase Security Rules for Firestore (if using database)
2. Configure Firebase Hosting for production deployment
3. Set up Firebase Cloud Functions for advanced features
4. Implement user role-based access control
5. Add email verification flow
6. Implement password reset functionality

## Support

If you encounter issues:

1. Check the browser console for errors
2. Check the backend logs for authentication errors
3. Verify Firebase project configuration
4. Ensure all environment variables are set correctly
