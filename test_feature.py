#!/usr/bin/env python3
"""
Test feature with some intentional issues for AI review testing
"""

import os
import sys
from typing import List, Dict, Optional

def get_user_input() -> str:
    """Get user input without proper validation - SECURITY ISSUE"""
    return input("Enter your name: ")

def process_data(data: str) -> str:
    """Process data with SQL injection vulnerability - SECURITY ISSUE"""
    # This is intentionally vulnerable for testing
    query = f"SELECT * FROM users WHERE name = '{data}'"
    return query

def calculate_fibonacci(n: int) -> int:
    """Calculate Fibonacci number - PERFORMANCE ISSUE"""
    # Inefficient recursive implementation
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

def process_list(items: List[str]) -> List[str]:
    """Process list with potential issues - QUALITY ISSUE"""
    result = []
    for i in range(len(items)):
        item = items[i]
        if item is not None:
            result.append(item.upper())
    return result

def main():
    """Main function with multiple issues"""
    try:
        # Security issue: unvalidated input
        user_input = get_user_input()
        
        # Security issue: SQL injection
        result = process_data(user_input)
        print(f"Query: {result}")
        
        # Performance issue: inefficient algorithm
        fib_result = calculate_fibonacci(35)
        print(f"Fibonacci: {fib_result}")
        
        # Quality issue: inefficient list processing
        test_list = ["hello", "world", None, "test"]
        processed = process_list(test_list)
        print(f"Processed: {processed}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
