#!/usr/bin/env python3
"""
Test file for enhanced AI feedback system - contains intentional issues across all severity levels
"""

import os
import sys
import subprocess
import hashlib
import json

# GLARING ISSUE: Hardcoded credentials
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "admin123"
SECRET_TOKEN = "super_secret_key_12345"

class SecurityVulnerableClass:
    def __init__(self):
        # SUBTLE ISSUE: Storing sensitive data in memory without encryption
        self.user_passwords = {}
        self.session_tokens = []
        
    # GLARING ISSUE: SQL injection vulnerability
    def get_user_by_id(self, user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"  # Direct injection
        return self.execute_query(query)
    
    # GLARING ISSUE: Command injection vulnerability
    def backup_user_data(self, filename):
        os.system(f"mysqldump users > {filename}")  # Shell injection
        
    # SUBTLE ISSUE: Weak password validation
    def validate_password(self, password):
        if len(password) >= 6:  # Too weak requirement
            return True
        return False
    
    # GLARING ISSUE: XSS vulnerability
    def render_user_profile(self, user_data):
        html = f"<h1>Welcome {user_data['name']}</h1>"  # No sanitization
        return html
    
    # SUBTLE ISSUE: Information disclosure in error messages
    def authenticate_user(self, username, password):
        try:
            user = self.get_user_by_username(username)
            if not user:
                raise Exception(f"User {username} not found in database")
            if user['password'] != password:
                raise Exception(f"Invalid password for user {username}")
            return user
        except Exception as e:
            print(f"Authentication error: {e}")  # Leaks info
            return None

class PerformanceIssues:
    def __init__(self):
        # PERFORMANCE ISSUE: Loading large dataset without pagination
        self.all_users = self.load_all_users()  # Could be millions
        
    # PERFORMANCE ISSUE: N+1 query problem
    def get_users_with_orders(self):
        users = self.get_all_users()
        result = []
        for user in users:  # Loop over potentially thousands
            orders = self.get_orders_for_user(user['id'])  # N queries
            user['orders'] = orders
            result.append(user)
        return result
    
    # PERFORMANCE ISSUE: Inefficient algorithm - O(n²)
    def find_duplicate_emails(self, users):
        duplicates = []
        for i, user1 in enumerate(users):
            for j, user2 in enumerate(users):
                if i != j and user1['email'] == user2['email']:
                    duplicates.append(user1)
        return duplicates
    
    # PERFORMANCE ISSUE: Memory leak - not releasing resources
    def process_large_file(self, filepath):
        data = []
        with open(filepath, 'r') as f:
            for line in f:
                # Processing large files line by line but storing all in memory
                processed = self.heavy_processing(line)
                data.append(processed)  # Memory grows indefinitely
        return data
    
    # PERFORMANCE ISSUE: Blocking synchronous operation
    def send_notifications(self, users):
        for user in users:
            self.send_email(user['email'])  # Blocking call
            self.send_sms(user['phone'])    # Blocking call
            
    # SUBTLE ISSUE: No caching for expensive operations
    def calculate_user_score(self, user_id):
        # Expensive calculation done every time
        orders = self.get_user_orders(user_id)
        reviews = self.get_user_reviews(user_id)
        interactions = self.get_user_interactions(user_id)
        
        score = 0
        for order in orders:
            score += order['value'] * 0.1
        for review in reviews:
            score += review['rating'] * 2
        for interaction in interactions:
            score += interaction['points']
            
        return score

class QualityIssues:
    # QUALITY ISSUE: Missing error handling
    def divide_numbers(self, a, b):
        return a / b  # No check for division by zero
    
    # QUALITY ISSUE: Magic numbers and hardcoded values
    def calculate_tax(self, amount):
        if amount > 10000:
            return amount * 0.25  # Magic number
        elif amount > 5000:
            return amount * 0.15  # Magic number
        else:
            return amount * 0.1   # Magic number
    
    # QUALITY ISSUE: God method - too many responsibilities
    def process_user_registration(self, user_data):
        # Validate input
        if not user_data.get('email'):
            raise ValueError("Email required")
        
        # Check if user exists
        existing = self.find_user_by_email(user_data['email'])
        if existing:
            raise ValueError("User exists")
        
        # Hash password
        password_hash = hashlib.md5(user_data['password'].encode()).hexdigest()
        
        # Create user record
        user_id = self.insert_user({
            'email': user_data['email'],
            'password': password_hash,
            'name': user_data['name'],
            'created_at': 'NOW()'
        })
        
        # Send welcome email
        self.send_welcome_email(user_data['email'])
        
        # Log registration
        self.log_user_activity(user_id, 'registration')
        
        # Update statistics
        self.increment_registration_count()
        
        # Create default preferences
        self.create_default_preferences(user_id)
        
        return user_id
    
    # QUALITY ISSUE: Inconsistent return types
    def get_user_age(self, user_id):
        user = self.find_user(user_id)
        if not user:
            return None  # Sometimes returns None
        if not user.get('birth_date'):
            return "Unknown"  # Sometimes returns string
        return 25  # Sometimes returns int
    
    # QUALITY ISSUE: Poor variable naming and no documentation
    def xyz(self, a, b, c):
        x = a + b
        y = x * c
        z = y / 2
        if z > 100:
            return True
        return False

# QUALITY ISSUE: Global variables
current_user = None
debug_mode = True
error_count = 0

# SUBTLE ISSUE: Race condition in global state
def update_user_session(user_id, session_data):
    global current_user
    current_user = user_id  # Not thread-safe
    
def get_current_user():
    global current_user
    return current_user  # Could return stale data

# GLARING ISSUE: Eval injection
def execute_user_formula(formula_string):
    # User input directly executed - CRITICAL security issue
    result = eval(formula_string)
    return result

# PERFORMANCE ISSUE: Recursive function without memoization
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # Exponential time complexity

# QUALITY ISSUE: Dead code
def unused_function():
    """This function is never called"""
    print("This is dead code")
    return "unused"

# SUBTLE ISSUE: Resource not properly closed
def read_config_file(filename):
    f = open(filename, 'r')  # File not closed
    config = json.load(f)
    return config

if __name__ == "__main__":
    # QUALITY ISSUE: No error handling in main
    security = SecurityVulnerableClass()
    performance = PerformanceIssues()
    quality = QualityIssues()
    
    # GLARING ISSUE: Using hardcoded credentials
    user = security.authenticate_user("admin", DATABASE_PASSWORD)
    
    # PERFORMANCE ISSUE: Calling expensive operations unnecessarily
    for i in range(1000):
        score = performance.calculate_user_score(1)
        fib = fibonacci(30)  # Very expensive
    
    print("Test completed")
