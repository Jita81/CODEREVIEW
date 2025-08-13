# Realistic Test Module - 25 Intentional Bugs Inventory - Test 2

## 📋 Bug Distribution by File and Severity

### user_service.py (8 bugs)
1. **HIGH**: Using pickle for serialization (security risk) - Line 11
2. **HIGH**: Hardcoded secret key - Line 18  
3. **MEDIUM**: No connection timeout/error handling - Line 21
4. **HIGH**: SQL injection vulnerability - Line 26
5. **HIGH**: MD5 for password hashing (weak crypto) - Line 32
6. **MEDIUM**: Logging sensitive error information - Line 44
7. **MEDIUM**: Insecure file permissions (777) - Line 48
8. **HIGH**: Pickle deserialization risk - Line 49

### api_handler.py (8 bugs)
9. **HIGH**: No authentication for sensitive endpoint - Line 15
10. **MEDIUM**: No input validation - Line 21
11. **MEDIUM**: Predictable session token pattern - Line 25
12. **HIGH**: Command injection vulnerability - Line 33
13. **MEDIUM**: No file type validation - Line 39
14. **HIGH**: Path traversal vulnerability - Line 41
15. **HIGH**: Code injection via eval() - Line 48
16. **LOW**: Debug mode enabled in production - Line 52

### data_processor.py (6 bugs)
17. **MEDIUM**: Missing thread synchronization - Line 14
18. **MEDIUM**: Inadequate email validation regex - Line 17
19. **LOW**: Inefficient O(n²) algorithm - Line 21
20. **MEDIUM**: No timeout, SSL verification disabled - Line 30
21. **MEDIUM**: Race condition, no thread safety - Line 34
22. **LOW**: Memory leak, no size limits - Line 39

### config.py (3 bugs)
23. **HIGH**: Hardcoded credentials in config - Lines 9-11
24. **MEDIUM**: Sensitive info logged in debug - Line 19
25. **HIGH**: Code execution via exec() - Line 29

## 📊 Severity Distribution
- **HIGH**: 10 bugs (40%) - Critical security vulnerabilities
- **MEDIUM**: 12 bugs (48%) - Important quality/security issues  
- **LOW**: 3 bugs (12%) - Performance and minor issues

## 🎯 Expected Detection Targets
- **Minimum**: 15/25 bugs (60%) - Basic security scanner level
- **Good**: 20/25 bugs (80%) - Comprehensive analysis
- **Excellent**: 23+/25 bugs (92%+) - AI-powered deep analysis

This realistic module simulates a typical web application with common security vulnerabilities, performance issues, and code quality problems.
