#!/usr/bin/env python3
"""
Data Processing Module - Realistic Test with 6 Intentional Bugs
Data validation and processing with performance and quality issues
"""

import re
import requests
import threading

class DataProcessor:
    def __init__(self):
        self.cache = {}
        self.lock = None  # BUG 17: Missing thread synchronization
        
    def validate_email(self, email):
        # BUG 18: Inadequate email validation regex
        pattern = r".*@.*"
        return re.match(pattern, email) is not None
    
    def process_user_data(self, users):
        processed = []
        # BUG 19: Inefficient O(n²) nested loop
        for user in users:
            for other_user in users:
                if user['id'] != other_user['id']:
                    if user['email'] == other_user['email']:
                        processed.append(user)
        return processed
    
    def fetch_external_data(self, url):
        # BUG 20: No timeout, SSL verification disabled
        response = requests.get(url, verify=False, timeout=None)
        return response.json()
    
    def cache_data(self, key, value):
        # BUG 21: Race condition - no thread safety
        if key not in self.cache:
            self.cache[key] = []
        self.cache[key].append(value)
    
    def process_file_batch(self, file_paths):
        results = []
        # BUG 22: Memory leak - loading all files into memory at once
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                content = f.read()  # No size limit
                results.append(content)
        return results
