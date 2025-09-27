import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User,
  UserCredential,
  AuthError,
} from 'firebase/auth';
import { auth } from './firebase';

export interface AuthUser {
  uid: string;
  email: string | null;
  displayName?: string | null;
  firstName?: string;
  lastName?: string;
}

export interface SignupData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

// Convert Firebase User to our AuthUser interface
const mapFirebaseUser = (user: User): AuthUser => {
  return {
    uid: user.uid,
    email: user.email,
    displayName: user.displayName,
  };
};

// Firebase Authentication Service
export class FirebaseAuthService {
  // Sign up a new user
  static async signup(data: SignupData): Promise<{ user: AuthUser; error: null } | { user: null; error: string }> {
    try {
      const userCredential: UserCredential = await createUserWithEmailAndPassword(
        auth,
        data.email,
        data.password
      );

      // Update the user's display name
      await userCredential.user.updateProfile({
        displayName: `${data.firstName} ${data.lastName}`,
      });

      const authUser = mapFirebaseUser(userCredential.user);
      authUser.firstName = data.firstName;
      authUser.lastName = data.lastName;

      return { user: authUser, error: null };
    } catch (error) {
      const authError = error as AuthError;
      return { user: null, error: this.getErrorMessage(authError) };
    }
  }

  // Sign in an existing user
  static async login(data: LoginData): Promise<{ user: AuthUser; error: null } | { user: null; error: string }> {
    try {
      const userCredential: UserCredential = await signInWithEmailAndPassword(
        auth,
        data.email,
        data.password
      );

      const authUser = mapFirebaseUser(userCredential.user);
      
      // Extract first and last name from displayName if available
      if (authUser.displayName) {
        const nameParts = authUser.displayName.split(' ');
        authUser.firstName = nameParts[0] || '';
        authUser.lastName = nameParts.slice(1).join(' ') || '';
      }

      return { user: authUser, error: null };
    } catch (error) {
      const authError = error as AuthError;
      return { user: null, error: this.getErrorMessage(authError) };
    }
  }

  // Sign out the current user
  static async logout(): Promise<{ error: null } | { error: string }> {
    try {
      await signOut(auth);
      return { error: null };
    } catch (error) {
      const authError = error as AuthError;
      return { error: this.getErrorMessage(authError) };
    }
  }

  // Get the current user
  static getCurrentUser(): AuthUser | null {
    const user = auth.currentUser;
    return user ? mapFirebaseUser(user) : null;
  }

  // Listen to authentication state changes
  static onAuthStateChange(callback: (user: AuthUser | null) => void): () => void {
    return onAuthStateChanged(auth, (user) => {
      callback(user ? mapFirebaseUser(user) : null);
    });
  }

  // Get user-friendly error messages
  private static getErrorMessage(error: AuthError): string {
    switch (error.code) {
      case 'auth/user-not-found':
        return 'No account found with this email address.';
      case 'auth/wrong-password':
        return 'Incorrect password. Please try again.';
      case 'auth/email-already-in-use':
        return 'An account with this email already exists.';
      case 'auth/weak-password':
        return 'Password should be at least 6 characters long.';
      case 'auth/invalid-email':
        return 'Please enter a valid email address.';
      case 'auth/user-disabled':
        return 'This account has been disabled. Please contact support.';
      case 'auth/too-many-requests':
        return 'Too many failed attempts. Please try again later.';
      case 'auth/network-request-failed':
        return 'Network error. Please check your connection and try again.';
      case 'auth/invalid-credential':
        return 'Invalid email or password. Please check your credentials.';
      default:
        return 'An error occurred during authentication. Please try again.';
    }
  }
}
