#!/usr/bin/env python3
"""
Enhanced test file with multiple complex issues to test 60k token AI review capacity
"""

import os
import sys
import json
import sqlite3
import hashlib
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import threading
import time

class UserManager:
    """User management class with multiple security and performance issues"""
    
    def __init__(self):
        self.users = {}
        self.db_connection = None
        self.lock = threading.Lock()
    
    def connect_database(self, db_path: str):
        """Connect to database with potential security issues"""
        # SECURITY ISSUE: No input validation
        self.db_connection = sqlite3.connect(db_path)
    
    def create_user(self, username: str, password: str, email: str) -> bool:
        """Create user with multiple security vulnerabilities"""
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
        
        # SECURITY ISSUE: Plain text password storage
        hashed_password = password  # Should use proper hashing
        
        # SECURITY ISSUE: No input validation
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(query)
                self.db_connection.commit()
                return True
            except Exception as e:
                print(f"Error creating user: {e}")
                return False
        return False
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user with security issues"""
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                return result is not None
            except Exception as e:
                print(f"Authentication error: {e}")
                return False
        return False

class DataProcessor:
    """Data processing class with performance and quality issues"""
    
    def __init__(self):
        self.cache = {}
        self.data_queue = []
    
    def process_large_dataset(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process large dataset with performance issues"""
        # PERFORMANCE ISSUE: Inefficient nested loops
        processed_data = []
        for item in data:
            for field in item:
                for subfield in field:
                    # PERFORMANCE ISSUE: Expensive operation in nested loop
                    processed_value = self.expensive_operation(item[field][subfield])
                    processed_data.append({
                        'original': item,
                        'processed': processed_value,
                        'timestamp': datetime.now().isoformat()
                    })
        return processed_data
    
    def expensive_operation(self, value: Any) -> Any:
        """Expensive operation that should be optimized"""
        # PERFORMANCE ISSUE: Inefficient algorithm
        if isinstance(value, str):
            # PERFORMANCE ISSUE: Unnecessary string operations
            result = ""
            for char in value:
                result += char.upper()  # Should use join() instead
            return result
        elif isinstance(value, int):
            # PERFORMANCE ISSUE: Inefficient calculation
            return self.calculate_fibonacci(value)
        return value
    
    def calculate_fibonacci(self, n: int) -> int:
        """Calculate Fibonacci with exponential complexity"""
        # PERFORMANCE ISSUE: Exponential time complexity
        if n <= 1:
            return n
        return self.calculate_fibonacci(n - 1) + self.calculate_fibonacci(n - 2)
    
    def cache_data(self, key: str, value: Any):
        """Cache data with memory leak potential"""
        # QUALITY ISSUE: No cache size limit
        self.cache[key] = value
        # QUALITY ISSUE: No cache expiration
        # QUALITY ISSUE: No cache cleanup mechanism

class FileHandler:
    """File handling class with resource management issues"""
    
    def __init__(self):
        self.open_files = []
        self.file_handles = {}
    
    def read_file(self, filepath: str) -> str:
        """Read file with resource management issues"""
        # QUALITY ISSUE: No file existence check
        # QUALITY ISSUE: No error handling for file operations
        file_handle = open(filepath, 'r')
        self.open_files.append(filepath)
        self.file_handles[filepath] = file_handle
        
        content = file_handle.read()
        # QUALITY ISSUE: File handle not properly closed
        return content
    
    def write_file(self, filepath: str, content: str):
        """Write file with potential issues"""
        # QUALITY ISSUE: No directory existence check
        # QUALITY ISSUE: No backup mechanism
        with open(filepath, 'w') as f:
            f.write(content)
    
    def cleanup(self):
        """Cleanup method with incomplete implementation"""
        # QUALITY ISSUE: Incomplete cleanup
        for filepath in self.open_files:
            if filepath in self.file_handles:
                # QUALITY ISSUE: No error handling for close operation
                self.file_handles[filepath].close()
        # QUALITY ISSUE: Lists not cleared after cleanup

def main():
    """Main function demonstrating all the issues"""
    try:
        # Initialize components
        user_manager = UserManager()
        data_processor = DataProcessor()
        file_handler = FileHandler()
        
        # SECURITY ISSUE: Hardcoded database path
        user_manager.connect_database("users.db")
        
        # SECURITY ISSUE: Creating user with unvalidated input
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter email: ")
        
        success = user_manager.create_user(username, password, email)
        print(f"User creation: {'Success' if success else 'Failed'}")
        
        # PERFORMANCE ISSUE: Processing large dataset inefficiently
        large_dataset = [{"field1": {"subfield1": "value1"}} for _ in range(1000)]
        processed = data_processor.process_large_dataset(large_dataset)
        print(f"Processed {len(processed)} items")
        
        # QUALITY ISSUE: File operations without proper error handling
        file_handler.read_file("nonexistent_file.txt")
        file_handler.write_file("output.txt", "test content")
        
        # PERFORMANCE ISSUE: Expensive operation
        fib_result = data_processor.calculate_fibonacci(30)
        print(f"Fibonacci result: {fib_result}")
        
        # QUALITY ISSUE: No cleanup
        # file_handler.cleanup()  # Should be called
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
