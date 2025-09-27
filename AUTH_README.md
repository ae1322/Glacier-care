# Authentication System

This document explains the authentication system that has been added to your HealthTranslate application.

## Features

### 🔐 Authentication Pages
- **Login Page** (`/login`) - User sign-in with email and password
- **Signup Page** (`/signup`) - User registration with form validation
- **Protected Routes** - Main application requires authentication

### 🛡️ Security Features
- Form validation using Zod schema
- Password strength requirements
- Protected route wrapper
- Session management with localStorage
- Automatic redirects for unauthenticated users

### 🎨 UI Components
- Modern, responsive design using shadcn/ui components
- Consistent styling with your existing medical theme
- Loading states and error handling
- Success feedback for user actions

## File Structure

```
src/
├── contexts/
│   └── AuthContext.tsx          # Authentication state management
├── components/
│   ├── ProtectedRoute.tsx       # Route protection wrapper
│   └── AuthNavigation.tsx       # Navigation between auth pages
└── pages/
    ├── Login.tsx                # Login page component
    ├── Signup.tsx               # Signup page component
    └── Index.tsx                # Updated with auth header
```

## How It Works

### 1. Authentication Flow
1. User visits the app → Redirected to `/login` if not authenticated
2. User can sign up or log in
3. After successful authentication → Redirected to main app
4. User can logout from the header

### 2. Route Protection
- Main application (`/`) is wrapped with `ProtectedRoute`
- Unauthenticated users are automatically redirected to login
- Login page remembers where user was trying to go

### 3. State Management
- `AuthContext` provides authentication state throughout the app
- User session is persisted in localStorage
- Context includes: `user`, `isAuthenticated`, `login()`, `signup()`, `logout()`

## Demo Credentials

For testing purposes, you can use any email/password combination:
- **Email**: `demo@healthtranslate.com`
- **Password**: `demo123`

Or any valid email format with any password (minimum 6 characters for login, 8 characters for signup).

## Customization

### Adding Real Authentication
To connect to a real backend:

1. **Update AuthContext.tsx**:
   ```typescript
   const login = async (email: string, password: string) => {
     const response = await fetch('/api/auth/login', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ email, password })
     });
     const data = await response.json();
     // Handle response and set user state
   };
   ```

2. **Add JWT Token Management**:
   ```typescript
   // Store token in localStorage
   localStorage.setItem('token', data.token);
   
   // Add to API requests
   headers: { 'Authorization': `Bearer ${token}` }
   ```

### Styling Customization
- Colors and themes are defined in `src/index.css`
- Components use Tailwind CSS classes
- Medical theme colors are already applied

## Usage Examples

### Using Authentication in Components
```typescript
import { useAuth } from '@/contexts/AuthContext';

const MyComponent = () => {
  const { user, isAuthenticated, logout } = useAuth();
  
  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }
  
  return (
    <div>
      Welcome, {user?.email}!
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

### Adding New Protected Routes
```typescript
<Route 
  path="/dashboard" 
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  } 
/>
```

## Next Steps

1. **Backend Integration**: Connect to your authentication API
2. **Password Reset**: Add forgot password functionality
3. **Email Verification**: Add email confirmation for signups
4. **User Profile**: Add user profile management
5. **Role-based Access**: Add different user roles if needed

The authentication system is now fully integrated and ready to use! 🚀
