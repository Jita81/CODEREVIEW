#!/usr/bin/env python3
"""
Demo application for testing AI code review
"""

import os
import sys
from typing import List, Dict, Optional

def get_user_input() -> str:
    """Get user input without proper validation"""
    return input("Enter your name: ")

def process_data(data: str) -> str:
    """Process data with potential security issues"""
    # This is intentionally vulnerable for testing
    query = f"SELECT * FROM users WHERE name = '{data}'"
    return query

def calculate_fibonacci(n: int) -> int:
    """Calculate Fibonacci number - inefficient implementation"""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

def main():
    """Main function with some issues"""
    try:
        user_input = get_user_input()
        result = process_data(user_input)
        print(f"Result: {result}")
        
        # Inefficient calculation
        fib_result = calculate_fibonacci(40)
        print(f"Fibonacci: {fib_result}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
