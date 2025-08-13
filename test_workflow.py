#!/usr/bin/env python3
"""
Test file to validate AI review workflow
"""

import os
import sqlite3

def login_user(username, password):
    """Login function with SQL injection vulnerability"""
    # SECURITY ISSUE: SQL injection - should use parameterized queries
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    # SECURITY ISSUE: Hardcoded database path
    conn = sqlite3.connect("/tmp/users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    
    # QUALITY ISSUE: Connection not properly closed
    return result is not None

def fibonacci(n):
    """Calculate Fibonacci number with poor performance"""
    # PERFORMANCE ISSUE: Exponential time complexity
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def process_data(data_list):
    """Process data with inefficient operations"""
    # PERFORMANCE ISSUE: Inefficient string concatenation in loop
    result = ""
    for item in data_list:
        result += str(item) + ","
    
    # QUALITY ISSUE: No input validation
    return result[:-1]  # Remove trailing comma

def main():
    """Main function with various issues"""
    # SECURITY ISSUE: Hardcoded credentials
    admin_user = "admin"
    admin_pass = "password123"
    
    # QUALITY ISSUE: No error handling
    user_input = input("Enter username: ")
    pass_input = input("Enter password: ")
    
    if login_user(user_input, pass_input):
        print("Login successful!")
        
        # PERFORMANCE ISSUE: Expensive calculation
        fib_result = fibonacci(30)
        print(f"Fibonacci(30) = {fib_result}")
        
        # Test data processing
        test_data = list(range(100))
        processed = process_data(test_data)
        print(f"Processed: {processed[:50]}...")
    else:
        print("Login failed!")

if __name__ == "__main__":
    main()
