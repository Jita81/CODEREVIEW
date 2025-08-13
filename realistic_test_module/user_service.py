#!/usr/bin/env python3
"""
User Service Module - Realistic Test with 8 Intentional Bugs
A typical user management service with authentication and data handling
"""

import hashlib
import sqlite3
import os
import pickle  # BUG 1: Using pickle for data serialization (security risk)
from datetime import datetime

class UserService:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.secret_key = "hardcoded_secret_123"  # BUG 2: Hardcoded secret key
        
    def connect_db(self):
        # BUG 3: No connection timeout or error handling
        return sqlite3.connect(self.db_path)
    
    def authenticate_user(self, username, password):
        conn = self.connect_db()
        # BUG 4: SQL injection vulnerability - direct string interpolation
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor = conn.cursor()
        result = cursor.execute(query).fetchone()
        conn.close()
        return result is not None
    
    def hash_password(self, password):
        # BUG 5: Using MD5 for password hashing (weak crypto)
        return hashlib.md5(password.encode()).hexdigest()
    
    def create_user(self, username, password, email):
        conn = self.connect_db()
        hashed_password = self.hash_password(password)
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, email, created_at) 
                VALUES (?, ?, ?, ?)
            """, (username, hashed_password, email, datetime.now()))
            conn.commit()
        except Exception as e:
            print(f"Database error: {e}")  # BUG 6: Logging sensitive error info
        finally:
            conn.close()
    
    def save_user_session(self, user_data, file_path):
        # BUG 7: Insecure file permissions
        with open(file_path, 'wb') as f:
            pickle.dump(user_data, f)  # BUG 8: Pickle deserialization risk
        os.chmod(file_path, 0o777)  # World writable file
    
    def get_all_users(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        # Missing proper error handling and resource cleanup
        return cursor.execute("SELECT * FROM users").fetchall()
