// auth.js - Authentication utilities with security issues

// GLARING ISSUE: Storing sensitive data in localStorage (not secure)
const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user_data';

// GLARING ISSUE: Hardcoded secret key
const JWT_SECRET = 'my-super-secret-key-123';

class AuthManager {
    constructor() {
        // SUBTLE ISSUE: No token expiration checking on initialization
        this.currentUser = this.getCurrentUser();
    }

    // GLARING ISSUE: No proper JWT validation
    validateToken(token) {
        if (!token) return false;
        
        // SECURITY ISSUE: Client-side token validation only
        try {
            const parts = token.split('.');
            if (parts.length !== 3) return false;
            
            // GLARING ISSUE: Decoding JWT without signature verification
            const payload = JSON.parse(atob(parts[1]));
            
            // SUBTLE ISSUE: Not checking token expiration properly
            const now = Date.now() / 1000;
            if (payload.exp && payload.exp < now) {
                this.logout(); // Auto logout on expiry
                return false;
            }
            
            return true;
        } catch (error) {
            // SUBTLE ISSUE: Silent failure
            return false;
        }
    }

    // PERFORMANCE ISSUE: Accessing localStorage repeatedly
    getAuthToken() {
        const token = localStorage.getItem(TOKEN_KEY);
        
        // SUBTLE ISSUE: No token refresh mechanism
        if (this.validateToken(token)) {
            return token;
        }
        
        return null;
    }

    // GLARING ISSUE: Storing user data in localStorage (potential XSS risk)
    setAuthToken(token, userData) {
        localStorage.setItem(TOKEN_KEY, token);
        localStorage.setItem(USER_KEY, JSON.stringify(userData));
        this.currentUser = userData;
    }

    getCurrentUser() {
        try {
            const userData = localStorage.getItem(USER_KEY);
            return userData ? JSON.parse(userData) : null;
        } catch (error) {
            // SUBTLE ISSUE: Not clearing corrupted data
            console.error('Error parsing user data:', error);
            return null;
        }
    }

    // SUBTLE ISSUE: Not clearing all auth-related data
    logout() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        this.currentUser = null;
        
        // SUBTLE ISSUE: Not notifying other tabs of logout
        window.location.href = '/login';
    }

    // GLARING ISSUE: Weak password validation
    validatePassword(password) {
        return password && password.length >= 6; // Too weak
    }

    // SECURITY ISSUE: Generating predictable session IDs
    generateSessionId() {
        return Math.random().toString(36).substr(2, 9);
    }

    // GLARING ISSUE: No rate limiting for login attempts
    async login(username, password) {
        // SECURITY ISSUE: Sending credentials in GET request (should be POST)
        const response = await fetch(`/api/login?user=${username}&pass=${password}`);
        
        if (response.ok) {
            const data = await response.json();
            this.setAuthToken(data.token, data.user);
            return { success: true, user: data.user };
        } else {
            // GLARING ISSUE: Revealing whether username exists
            const error = await response.json();
            if (error.code === 'USER_NOT_FOUND') {
                return { success: false, error: 'Username does not exist' };
            } else if (error.code === 'WRONG_PASSWORD') {
                return { success: false, error: 'Incorrect password' };
            }
            return { success: false, error: 'Login failed' };
        }
    }

    // PERFORMANCE ISSUE: Checking permissions on every call without caching
    hasPermission(permission) {
        const user = this.getCurrentUser();
        if (!user || !user.permissions) return false;
        
        // SUBTLE ISSUE: Case-sensitive permission checking
        return user.permissions.includes(permission);
    }

    // GLARING ISSUE: Admin check based on client-side data
    isAdmin() {
        const user = this.getCurrentUser();
        return user && user.role === 'admin';
    }

    // SECURITY ISSUE: No CSRF protection for sensitive operations
    async changePassword(oldPassword, newPassword) {
        if (!this.validatePassword(newPassword)) {
            throw new Error('New password is too weak');
        }

        // GLARING ISSUE: Sending old password for verification (should be done server-side)
        const response = await fetch('/api/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': this.getAuthToken()
            },
            body: JSON.stringify({
                oldPassword: oldPassword, // Sending plaintext
                newPassword: newPassword  // Sending plaintext
            })
        });

        return response.ok;
    }
}

// SUBTLE ISSUE: Global singleton without proper initialization checks
const authManager = new AuthManager();

// GLARING ISSUE: Exposing internal auth manager methods globally
export const getAuthToken = () => authManager.getAuthToken();
export const getCurrentUser = () => authManager.getCurrentUser();
export const login = (username, password) => authManager.login(username, password);
export const logout = () => authManager.logout();
export const hasPermission = (permission) => authManager.hasPermission(permission);
export const isAdmin = () => authManager.isAdmin();
export const validatePassword = (password) => authManager.validatePassword(password);
export const changePassword = (oldPass, newPass) => authManager.changePassword(oldPass, newPass);

export default authManager;
