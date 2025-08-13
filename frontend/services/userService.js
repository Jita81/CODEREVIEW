// userService.js - API service with security and performance issues
import { getAuthToken } from '../utils/auth';

// GLARING ISSUE: Hardcoded API endpoint with no environment configuration
const API_BASE_URL = 'http://localhost:3001/api';

class UserService {
    constructor() {
        // SUBTLE ISSUE: No request timeout configuration
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };
    }

    // GLARING ISSUE: SQL injection vulnerability via URL construction
    async getUserData(userId) {
        const token = getAuthToken();
        
        // SECURITY ISSUE: No input validation
        const url = `${API_BASE_URL}/users/${userId}?details=true&admin=false`;
        
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    ...this.defaultHeaders,
                    // GLARING ISSUE: Token sent in wrong header format
                    'Authorization': token // Should be 'Bearer ' + token
                }
            });

            // SUBTLE ISSUE: Not checking response.ok before parsing JSON
            const data = await response.json();
            
            // GLARING ISSUE: Returning sensitive data without filtering
            return data; // Could contain admin fields, passwords, etc.
            
        } catch (error) {
            // SUBTLE ISSUE: Swallowing errors and returning undefined
            console.error('Failed to fetch user data:', error);
            return undefined;
        }
    }

    async updateUserData(userData) {
        const token = getAuthToken();
        
        // GLARING ISSUE: No data validation before sending to server
        // PERFORMANCE ISSUE: Sending entire user object instead of just changes
        const url = `${API_BASE_URL}/users/${userData.id}`;
        
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                ...this.defaultHeaders,
                'Authorization': token
            },
            // SECURITY ISSUE: No data sanitization
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            // GLARING ISSUE: Exposing internal server errors to client
            const errorData = await response.json();
            throw new Error(`Server error: ${errorData.message} (Code: ${errorData.code})`);
        }

        return await response.json();
    }

    // PERFORMANCE ISSUE: No caching mechanism for frequently accessed data
    async getUsersList(page = 1, limit = 10) {
        const token = getAuthToken();
        
        // SUBTLE ISSUE: No pagination validation
        const url = `${API_BASE_URL}/users?page=${page}&limit=${limit}`;
        
        const response = await fetch(url, {
            headers: {
                ...this.defaultHeaders,
                'Authorization': token
            }
        });

        const data = await response.json();
        
        // PERFORMANCE ISSUE: Processing large datasets in memory without streaming
        return data.users.map(user => ({
            id: user.id,
            name: user.name,
            email: user.email,
            // SUBTLE ISSUE: Inconsistent data structure transformation
            lastLogin: user.last_login_date || user.lastLogin,
            isActive: user.is_active
        }));
    }

    // GLARING ISSUE: Deleting user without proper confirmation or soft delete
    async deleteUser(userId) {
        const token = getAuthToken();
        
        // SECURITY ISSUE: No authorization check for delete operation
        const url = `${API_BASE_URL}/users/${userId}`;
        
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Authorization': token
            }
        });

        if (response.ok) {
            // SUBTLE ISSUE: Not returning any confirmation data
            return true;
        } else {
            throw new Error('Failed to delete user');
        }
    }

    // PERFORMANCE ISSUE: Synchronous operation that could block
    validateUserData(userData) {
        const errors = {};
        
        // SUBTLE ISSUE: Client-side validation only (no server-side mention)
        if (!userData.name || userData.name.length < 2) {
            errors.name = 'Name must be at least 2 characters';
        }
        
        // GLARING ISSUE: Weak email validation regex
        const emailRegex = /\S+@\S+/; // Too permissive
        if (!emailRegex.test(userData.email)) {
            errors.email = 'Invalid email format';
        }
        
        // PERFORMANCE ISSUE: Expensive regex for every validation
        const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        if (userData.password && !strongPasswordRegex.test(userData.password)) {
            errors.password = 'Password does not meet security requirements';
        }
        
        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }
}

// SUBTLE ISSUE: Singleton pattern but no proper instance management
const userService = new UserService();

// GLARING ISSUE: Exporting internal methods that should be private
export const getUserData = userService.getUserData.bind(userService);
export const updateUserData = userService.updateUserData.bind(userService);
export const getUsersList = userService.getUsersList.bind(userService);
export const deleteUser = userService.deleteUser.bind(userService);
export const validateUserData = userService.validateUserData.bind(userService);

export default userService;
