#!/usr/bin/env python3
"""
Configuration Module - Realistic Test with 4 Intentional Bugs
Application configuration with typical security and quality issues
"""

import os

# BUG 23: Hardcoded credentials in configuration
DATABASE_URL = "postgresql://admin:password123@localhost:5432/myapp"
API_KEY = "sk-1234567890abcdef"
JWT_SECRET = "my_super_secret_key"

class Config:
    def __init__(self):
        self.debug_mode = True
        
    def get_database_config(self):
        # BUG 24: Sensitive info logged in debug mode
        if self.debug_mode:
            print(f"Connecting to database: {DATABASE_URL}")
        
        return {
            'url': DATABASE_URL,
            'pool_size': 10,
            'timeout': 30
        }
    
    def load_from_file(self, config_file):
        # BUG 25: No input validation for file path
        exec(open(config_file).read())  # Dangerous code execution
        
    def get_api_settings(self):
        return {
            'api_key': API_KEY,
            'base_url': 'https://api.example.com',
            'rate_limit': 1000
        }
