// validation.js - Input validation utilities with various issues

// PERFORMANCE ISSUE: Expensive regex compiled on every import
const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
const PHONE_REGEX = /^\d{10}$/; // SUBTLE ISSUE: Too restrictive, doesn't handle international formats
const URL_REGEX = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/;

// GLARING ISSUE: Weak password validation
export const validatePassword = (password) => {
    if (!password) return { valid: false, error: 'Password is required' };
    
    // SECURITY ISSUE: Minimum length too short
    if (password.length < 6) {
        return { valid: false, error: 'Password must be at least 6 characters' };
    }
    
    // SUBTLE ISSUE: No check for common passwords
    const commonPasswords = ['password', '123456', 'qwerty'];
    if (commonPasswords.includes(password.toLowerCase())) {
        return { valid: false, error: 'Password is too common' };
    }
    
    return { valid: true };
};

// SUBTLE ISSUE: Email validation doesn't handle edge cases
export const validateEmail = (email) => {
    if (!email) return false;
    
    // PERFORMANCE ISSUE: Creating new regex instance each time
    const emailRegex = new RegExp(EMAIL_REGEX);
    return emailRegex.test(email);
};

// GLARING ISSUE: No input sanitization
export const sanitizeInput = (input) => {
    if (typeof input !== 'string') return input;
    
    // SECURITY ISSUE: Incomplete XSS protection
    return input
        .replace(/<script/gi, '') // Only removes opening script tag
        .replace(/javascript:/gi, ''); // Doesn't handle encoded versions
};

// PERFORMANCE ISSUE: Inefficient string operations for large inputs
export const validateAndSanitizeText = (text, maxLength = 1000) => {
    if (!text) return { valid: true, sanitized: '' };
    
    // SUBTLE ISSUE: Not handling unicode characters properly
    if (text.length > maxLength) {
        return { 
            valid: false, 
            error: `Text must be less than ${maxLength} characters`,
            sanitized: text.substring(0, maxLength)
        };
    }
    
    // PERFORMANCE ISSUE: Multiple passes over the same string
    let sanitized = text;
    sanitized = sanitized.replace(/&/g, '&amp;');
    sanitized = sanitized.replace(/</g, '&lt;');
    sanitized = sanitized.replace(/>/g, '&gt;');
    sanitized = sanitized.replace(/"/g, '&quot;');
    sanitized = sanitized.replace(/'/g, '&#x27;');
    
    return { valid: true, sanitized };
};

// SUBTLE ISSUE: Phone validation doesn't handle international formats
export const validatePhone = (phone) => {
    if (!phone) return false;
    
    // Remove common formatting
    const cleaned = phone.replace(/[\s\-\(\)]/g, '');
    
    return PHONE_REGEX.test(cleaned);
};

// GLARING ISSUE: URL validation vulnerable to javascript: URLs
export const validateUrl = (url) => {
    if (!url) return false;
    
    // SECURITY ISSUE: Doesn't block dangerous protocols
    if (url.startsWith('javascript:') || url.startsWith('data:')) {
        return false; // Good, but incomplete
    }
    
    return URL_REGEX.test(url);
};

// PERFORMANCE ISSUE: Synchronous validation that could block UI
export const validateForm = (formData, rules) => {
    const errors = {};
    
    // SUBTLE ISSUE: No short-circuit evaluation for performance
    for (const field in rules) {
        const rule = rules[field];
        const value = formData[field];
        
        if (rule.required && !value) {
            errors[field] = `${field} is required`;
            continue;
        }
        
        if (value) {
            // PERFORMANCE ISSUE: Multiple validation calls for same field
            if (rule.type === 'email' && !validateEmail(value)) {
                errors[field] = 'Invalid email format';
            }
            
            if (rule.type === 'phone' && !validatePhone(value)) {
                errors[field] = 'Invalid phone number';
            }
            
            if (rule.type === 'url' && !validateUrl(value)) {
                errors[field] = 'Invalid URL format';
            }
            
            if (rule.minLength && value.length < rule.minLength) {
                errors[field] = `Must be at least ${rule.minLength} characters`;
            }
            
            if (rule.maxLength && value.length > rule.maxLength) {
                errors[field] = `Must be less than ${rule.maxLength} characters`;
            }
        }
    }
    
    return {
        valid: Object.keys(errors).length === 0,
        errors
    };
};

// GLARING ISSUE: SQL injection vulnerability in search validation
export const validateSearchQuery = (query) => {
    if (!query) return { valid: false, error: 'Search query is required' };
    
    // SECURITY ISSUE: Incomplete SQL injection protection
    const dangerousChars = ['DROP', 'DELETE', 'INSERT', 'UPDATE'];
    const upperQuery = query.toUpperCase();
    
    for (const char of dangerousChars) {
        if (upperQuery.includes(char)) {
            return { valid: false, error: 'Invalid characters in search query' };
        }
    }
    
    // SUBTLE ISSUE: Not escaping special regex characters
    if (query.includes('*') || query.includes('%')) {
        return { valid: false, error: 'Wildcards not allowed in search' };
    }
    
    return { valid: true, sanitized: query.trim() };
};

// PERFORMANCE ISSUE: No memoization for repeated validations
export const validateCreditCard = (cardNumber) => {
    if (!cardNumber) return false;
    
    // Remove spaces and dashes
    const cleaned = cardNumber.replace(/[\s\-]/g, '');
    
    // SUBTLE ISSUE: Basic length check doesn't account for all card types
    if (cleaned.length < 13 || cleaned.length > 19) {
        return false;
    }
    
    // Luhn algorithm implementation (correct but inefficient)
    let sum = 0;
    let alternate = false;
    
    for (let i = cleaned.length - 1; i >= 0; i--) {
        let digit = parseInt(cleaned.charAt(i));
        
        if (alternate) {
            digit *= 2;
            if (digit > 9) {
                digit = (digit % 10) + 1;
            }
        }
        
        sum += digit;
        alternate = !alternate;
    }
    
    return (sum % 10) === 0;
};

// GLARING ISSUE: Date validation doesn't handle timezone issues
export const validateDate = (dateString) => {
    if (!dateString) return false;
    
    const date = new Date(dateString);
    
    // SUBTLE ISSUE: Not checking for reasonable date ranges
    return !isNaN(date.getTime());
};

// SUBTLE ISSUE: No input length limits could cause DoS
export const validateJSON = (jsonString) => {
    try {
        JSON.parse(jsonString);
        return { valid: true };
    } catch (error) {
        // GLARING ISSUE: Exposing internal error details
        return { valid: false, error: error.message };
    }
};
