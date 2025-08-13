#!/usr/bin/env python3
"""
Final test file for Claude 4.1 AI review validation
"""

import os
import sqlite3

def authenticate_user(username, password):
    """Function with SQL injection vulnerability for testing"""
    # SECURITY ISSUE: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return query

def process_data(data_list):
    """Function with performance issue for testing"""
    # PERFORMANCE ISSUE: Inefficient string concatenation
    result = ""
    for item in data_list:
        result += str(item) + ","  # Should use join()
    return result

def main():
    """Main function with quality issues"""
    # SECURITY ISSUE: Hardcoded credentials
    admin_password = "admin123"
    
    # QUALITY ISSUE: No error handling
    user_input = input("Enter username: ")
    password_input = input("Enter password: ")
    
    # Test the vulnerable function
    sql_query = authenticate_user(user_input, password_input)
    print(f"SQL Query: {sql_query}")
    
    # Test performance issue
    test_data = list(range(1000))
    result = process_data(test_data)
    print(f"Processed data length: {len(result)}")

if __name__ == "__main__":
    main()
