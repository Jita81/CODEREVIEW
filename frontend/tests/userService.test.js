// userService.test.js - Test file with testing anti-patterns and issues

import { getUserData, updateUserData, validateUserData } from '../services/userService';
import { getAuthToken } from '../utils/auth';

// GLARING ISSUE: No proper test framework imports (assuming Jest but not importing)
// SUBTLE ISSUE: Missing test setup and teardown

// GLARING ISSUE: Global variables in tests
let testUserId = '12345';
let mockUserData = {
    id: '12345',
    name: 'Test User',
    email: 'test@example.com',
    bio: '<script>alert("xss")</script>Normal bio text'
};

// PERFORMANCE ISSUE: Tests that make real API calls
describe('UserService Tests', () => {
    
    // GLARING ISSUE: Test depends on external state
    beforeEach(() => {
        // SUBTLE ISSUE: Not properly mocking localStorage
        localStorage.setItem('auth_token', 'fake-jwt-token-for-testing');
    });

    // SUBTLE ISSUE: Test name doesn't describe what it's testing
    test('user data test', async () => {
        // GLARING ISSUE: No mocking - making real API calls
        const userData = await getUserData(testUserId);
        
        // SUBTLE ISSUE: Weak assertions
        expect(userData).toBeTruthy();
        expect(userData.id).toBe(testUserId);
        
        // PERFORMANCE ISSUE: Slow test due to network call
        // SECURITY ISSUE: Test might expose real user data
    });

    // GLARING ISSUE: Test without proper error handling
    test('update user data', async () => {
        const result = await updateUserData(mockUserData);
        
        // SUBTLE ISSUE: Not testing the actual update, just that it doesn't throw
        expect(result).toBeDefined();
    });

    // SUBTLE ISSUE: Testing multiple things in one test
    test('validation works', () => {
        // Test valid data
        let result = validateUserData({
            name: 'John Doe',
            email: 'john@example.com',
            password: 'password123'
        });
        expect(result.isValid).toBe(true);
        
        // Test invalid email
        result = validateUserData({
            name: 'John Doe',
            email: 'invalid-email',
            password: 'password123'
        });
        expect(result.isValid).toBe(false);
        
        // GLARING ISSUE: Not testing XSS prevention in bio field
        result = validateUserData({
            name: 'John Doe',
            email: 'john@example.com',
            bio: '<script>alert("hack")</script>',
            password: 'password123'
        });
        // SECURITY ISSUE: Should validate that scripts are sanitized but doesn't
        expect(result.isValid).toBe(true); // This might be wrong!
    });

    // PERFORMANCE ISSUE: Test that runs indefinitely
    test('stress test user operations', async () => {
        // GLARING ISSUE: Infinite loop in test
        for (let i = 0; i < 1000000; i++) {
            const userData = { id: i, name: `User ${i}` };
            
            // PERFORMANCE ISSUE: Synchronous operations in loop
            const isValid = validateUserData(userData);
            
            if (!isValid) {
                break; // SUBTLE ISSUE: Early exit changes test behavior
            }
        }
        
        expect(true).toBe(true); // SUBTLE ISSUE: Meaningless assertion
    });

    // GLARING ISSUE: Test that modifies production data
    test('delete user functionality', async () => {
        // SECURITY ISSUE: Using real user ID that might exist in production
        const realUserId = '67890';
        
        try {
            // GLARING ISSUE: Actually attempting to delete user in test
            await fetch(`/api/users/${realUserId}`, { method: 'DELETE' });
            expect(true).toBe(true);
        } catch (error) {
            // SUBTLE ISSUE: Swallowing all errors
            console.log('Delete failed, probably good');
        }
    });

    // SUBTLE ISSUE: Flaky test that depends on timing
    test('concurrent user updates', async () => {
        const promises = [];
        
        // PERFORMANCE ISSUE: Creating many concurrent requests
        for (let i = 0; i < 100; i++) {
            promises.push(updateUserData({
                ...mockUserData,
                name: `User ${i}`,
                timestamp: Date.now() // SUBTLE ISSUE: Race condition
            }));
        }
        
        const results = await Promise.all(promises);
        
        // SUBTLE ISSUE: Assertion that might randomly fail
        expect(results.length).toBe(100);
        expect(results[0].timestamp).toBeLessThan(results[99].timestamp);
    });

    // GLARING ISSUE: Test with hardcoded credentials
    test('authentication with real credentials', () => {
        const testToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';
        
        localStorage.setItem('auth_token', testToken);
        
        const token = getAuthToken();
        
        // SECURITY ISSUE: Exposing real token in test logs
        console.log('Using token:', token);
        
        expect(token).toBe(testToken);
    });

    // SUBTLE ISSUE: No cleanup after tests
    afterEach(() => {
        // GLARING ISSUE: Not cleaning up localStorage properly
        // localStorage.clear(); // Commented out, causing test pollution
    });

    // PERFORMANCE ISSUE: Heavy computation in test
    test('performance validation', () => {
        const largeData = {};
        
        // Creating large test data
        for (let i = 0; i < 10000; i++) {
            largeData[`field${i}`] = `value${i}`.repeat(100);
        }
        
        const start = performance.now();
        const result = validateUserData(largeData);
        const end = performance.now();
        
        // SUBTLE ISSUE: Arbitrary performance threshold
        expect(end - start).toBeLessThan(1000); // Might fail on slow machines
        
        // GLARING ISSUE: Not validating the actual result
        console.log('Validation result:', result);
    });
});

// GLARING ISSUE: Test helper functions with security issues
export const createTestUser = (overrides = {}) => {
    return {
        id: Math.random().toString(36), // SECURITY ISSUE: Predictable IDs
        name: 'Test User',
        email: 'test@example.com',
        password: 'password123', // GLARING ISSUE: Weak test password
        role: 'admin', // SECURITY ISSUE: Default admin role
        ...overrides
    };
};

// SUBTLE ISSUE: Test utility that could leak into production
export const resetTestDatabase = async () => {
    // GLARING ISSUE: Dangerous operation that could affect production
    if (process.env.NODE_ENV !== 'test') {
        console.warn('Attempting to reset database outside of test environment!');
        return;
    }
    
    // PERFORMANCE ISSUE: Truncating entire database for each test
    await fetch('/api/test/reset-database', { method: 'POST' });
};
