#!/usr/bin/env python3
"""
Comprehensive Error Test Module - 100 Intentional Issues
Testing AI code review detection capabilities across all severity levels
"""

# ERROR 1: Missing import for security functions
import os
import sys
import subprocess
import json
import hashlib
import pickle  # ERROR 2: Dangerous pickle import without security context
import urllib.request  # ERROR 3: Insecure HTTP library
from datetime import datetime
# ERROR 4: Missing import for typing annotations used below

# ERROR 5-8: Global variables with security issues
API_KEY = "sk-1234567890abcdef"  # ERROR 5: Hardcoded API key
DATABASE_URL = "mysql://admin:password123@localhost/db"  # ERROR 6: Hardcoded credentials
SECRET_KEY = "super_secret_key_12345"  # ERROR 7: Hardcoded secret
DEBUG_MODE = True  # ERROR 8: Debug mode enabled globally

# ERROR 9: Global mutable default
DEFAULT_CONFIG = {}

class VulnerableUserManager:
    """User management with multiple security vulnerabilities"""
    
    # ERROR 10: Class variable with credentials
    DEFAULT_ADMIN_PASSWORD = "admin123"
    
    def __init__(self, config=DEFAULT_CONFIG):  # ERROR 11: Mutable default argument
        # ERROR 12: Storing passwords in plain text
        self.users = {}
        self.passwords = {}
        # ERROR 13: Sensitive data in memory without encryption
        self.session_tokens = []
        # ERROR 14: No input validation on initialization
        self.config = config
        
    # ERROR 15: SQL injection vulnerability
    def get_user_by_id(self, user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"  # Direct injection
        return self.execute_query(query)
    
    # ERROR 16: Command injection vulnerability  
    def backup_user_data(self, filename):
        os.system(f"mysqldump users > {filename}")  # Shell injection
        
    # ERROR 17: Path traversal vulnerability
    def read_user_file(self, filename):
        with open(f"/uploads/{filename}", 'r') as f:  # No path validation
            return f.read()
    
    # ERROR 18: Weak password validation
    def validate_password(self, password):
        return len(password) >= 4  # Too weak
    
    # ERROR 19: XSS vulnerability
    def render_user_profile(self, user_data):
        return f"<h1>Welcome {user_data['name']}</h1>"  # No sanitization
    
    # ERROR 20: Information disclosure
    def authenticate_user(self, username, password):
        try:
            user = self.get_user_by_username(username)
            if not user:
                raise Exception(f"User {username} not found in database")  # Reveals existence
            if user['password'] != password:
                raise Exception(f"Invalid password for user {username}")  # Info leak
            return user
        except Exception as e:
            print(f"Authentication error: {e}")  # ERROR 21: Error details exposed
            return None
    
    # ERROR 22: Insecure deserialization
    def load_user_data(self, data):
        return pickle.loads(data)  # Dangerous deserialization
    
    # ERROR 23: Race condition
    def increment_login_count(self):
        current = self.get_login_count()
        # ERROR 24: Time-of-check vs time-of-use
        self.set_login_count(current + 1)
    
    # ERROR 25: No input sanitization
    def create_user(self, username, email, data):
        # ERROR 26: No validation of input parameters
        user_id = len(self.users) + 1
        # ERROR 27: Weak ID generation
        self.users[user_id] = {
            'username': username,  # No sanitization
            'email': email,        # No validation
            'data': data          # No filtering
        }
        return user_id

class PerformanceNightmare:
    """Class with severe performance issues"""
    
    def __init__(self):
        # ERROR 28: Loading massive dataset without pagination
        self.all_users = self.load_million_users()
        # ERROR 29: Expensive computation in constructor
        self.precalculated_data = self.expensive_calculation()
        
    # ERROR 30: N+1 query problem
    def get_users_with_detailed_info(self):
        users = self.get_all_users()  # 1 query
        result = []
        for user in users:  # N queries
            # ERROR 31: Multiple database calls in loop
            profile = self.get_user_profile(user['id'])
            orders = self.get_user_orders(user['id'])
            preferences = self.get_user_preferences(user['id'])
            result.append({**user, 'profile': profile, 'orders': orders, 'prefs': preferences})
        return result
    
    # ERROR 32: O(n²) algorithm
    def find_duplicate_emails(self, users):
        duplicates = []
        for i in range(len(users)):
            for j in range(len(users)):
                if i != j and users[i]['email'] == users[j]['email']:
                    duplicates.append(users[i])
        return duplicates
    
    # ERROR 33: Memory leak - storing all data
    def process_log_files(self, directory):
        all_logs = []
        for filename in os.listdir(directory):
            with open(f"{directory}/{filename}", 'r') as f:
                # ERROR 34: Reading entire file into memory
                content = f.read()
                # ERROR 35: No garbage collection
                processed = self.heavy_log_processing(content)
                all_logs.append(processed)  # Accumulating in memory
        return all_logs
    
    # ERROR 36: Inefficient string operations
    def build_report(self, data):
        report = ""
        for item in data:
            # ERROR 37: String concatenation in loop
            report += f"Item: {item['name']}\n"
            report += f"Value: {item['value']}\n"
            report += f"Status: {item['status']}\n"
            report += "---\n"
        return report
    
    # ERROR 38: No caching for expensive operations
    def calculate_complex_metrics(self, user_id):
        # ERROR 39: Repeated expensive calculations
        orders = self.get_user_orders(user_id)
        reviews = self.get_user_reviews(user_id)
        interactions = self.get_user_interactions(user_id)
        
        # ERROR 40: Inefficient nested loops
        score = 0
        for order in orders:
            for item in order['items']:
                for metric in item['metrics']:
                    score += metric['value'] * 0.1
        return score
    
    # ERROR 41: Blocking synchronous operations
    def send_notifications(self, users):
        for user in users:
            # ERROR 42: No timeout on network calls
            self.send_email(user['email'])
            self.send_sms(user['phone'])
            self.push_notification(user['device_id'])
            # ERROR 43: No error handling for failed sends
            
    # ERROR 44: Recursive function without memoization
    def fibonacci(self, n):
        if n <= 1:
            return n
        return self.fibonacci(n-1) + self.fibonacci(n-2)  # Exponential time
    
    # ERROR 45: Infinite loop potential
    def wait_for_condition(self):
        while True:  # No exit condition
            if self.check_condition():
                break
            # ERROR 46: No sleep, busy waiting

class QualityIssues:
    """Class demonstrating code quality problems"""
    
    # ERROR 47: Missing error handling
    def divide_numbers(self, a, b):
        return a / b  # Division by zero not handled
    
    # ERROR 48: Magic numbers everywhere
    def calculate_fee(self, amount, type):
        if type == 1:  # ERROR 49: Magic number comparison
            return amount * 0.05  # ERROR 50: Magic fee rate
        elif type == 2:
            return amount * 0.1   # ERROR 51: Another magic rate
        elif type == 3:
            return amount * 0.15  # ERROR 52: Yet another magic rate
        else:
            return amount * 0.02  # ERROR 53: Default magic rate
    
    # ERROR 54: God method - too many responsibilities
    def process_payment(self, user_id, amount, card_number, expiry, cvv, billing_address):
        # Validation
        if not user_id:
            raise ValueError("User ID required")
        if amount <= 0:
            raise ValueError("Invalid amount")
        
        # ERROR 55: Weak credit card validation
        if len(card_number) != 16:
            raise ValueError("Invalid card number")
        
        # ERROR 56: No CVV validation
        # ERROR 57: No expiry date validation
        
        # Get user
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check balance/limits
        if amount > 10000:  # ERROR 58: Hardcoded limit
            raise ValueError("Amount too high")
        
        # Process payment
        transaction_id = self.generate_transaction_id()
        
        # Update balances
        self.update_user_balance(user_id, -amount)
        
        # Send notifications
        self.send_payment_email(user['email'])
        self.send_sms_confirmation(user['phone'])
        
        # Log transaction
        self.log_transaction(transaction_id, user_id, amount)
        
        # Update statistics
        self.update_payment_stats()
        
        return transaction_id
    
    # ERROR 59: Inconsistent return types
    def get_user_age(self, user_id):
        user = self.find_user(user_id)
        if not user:
            return None  # Sometimes None
        if not user.get('birth_date'):
            return "Unknown"  # Sometimes string
        return 25  # Sometimes int
        # ERROR 60: Logic doesn't calculate actual age
    
    # ERROR 61: Poor variable naming
    def xyz(self, a, b, c, d):
        # ERROR 62: No documentation
        x = a + b
        y = x * c
        z = y / d  # ERROR 63: Potential division by zero again
        if z > 100:
            return True
        return False
        # ERROR 64: Magic number 100
    
    # ERROR 65: Dead code
    def unused_function(self):
        """This function is never called"""
        print("This is dead code")
        return "unused"
    
    # ERROR 66: Duplicate code
    def calculate_discount_premium(self, amount):
        if amount > 1000:
            return amount * 0.1
        else:
            return amount * 0.05
    
    def calculate_discount_standard(self, amount):
        # ERROR 67: Exact duplicate logic
        if amount > 1000:
            return amount * 0.1
        else:
            return amount * 0.05

# ERROR 68: Global state management
current_user = None
session_data = {}
error_count = 0

# ERROR 69: Thread-unsafe global operations
def update_session(user_id, data):
    global current_user, session_data
    current_user = user_id  # Race condition
    session_data[user_id] = data  # Not thread-safe

# ERROR 70: Dangerous eval usage
def execute_formula(formula_string):
    # ERROR 71: No input validation on eval
    result = eval(formula_string)  # Code injection
    return result

# ERROR 72: Pickle without security
def save_object(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)  # Insecure serialization

def load_object(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)  # ERROR 73: Insecure deserialization

# ERROR 74: Resource not closed
def read_large_file(filename):
    f = open(filename, 'r')  # File handle not closed
    data = f.read()
    return data
    # ERROR 75: File handle leaked

# ERROR 76: Weak random number generation
def generate_token():
    import random
    return str(random.randint(1000000, 9999999))  # Predictable

# ERROR 77: Hardcoded file paths
def save_user_data(data):
    with open("/tmp/user_data.txt", "w") as f:  # Hardcoded path
        f.write(str(data))

# ERROR 78: No input validation
def process_user_input(data):
    # ERROR 79: Direct use without validation
    return subprocess.run(data, shell=True)  # Command injection

# ERROR 80: Weak exception handling
def risky_operation():
    try:
        dangerous_code()
    except:  # ERROR 81: Bare except
        pass  # ERROR 82: Silent failure

# ERROR 83: Memory inefficient operations
def process_huge_list(items):
    # ERROR 84: Creating unnecessary copies
    filtered = [item for item in items if item.value > 0]
    sorted_items = sorted(filtered)
    mapped = [transform(item) for item in sorted_items]
    return mapped

# ERROR 85: No rate limiting
def api_call(endpoint):
    # ERROR 86: No timeout
    response = urllib.request.urlopen(f"http://api.example.com/{endpoint}")
    return response.read()

# ERROR 87: Weak cryptography
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is broken

# ERROR 88: Information in comments
def connect_to_db():
    # Password: admin123, Server: prod-db-01
    # ERROR 89: Credentials in comments
    pass

# ERROR 89: SQL without parameterization
def search_users(name):
    query = f"SELECT * FROM users WHERE name LIKE '%{name}%'"  # SQL injection
    return execute_query(query)

# ERROR 90: Unvalidated redirects
def redirect_user(url):
    # ERROR 91: No URL validation
    return f"<script>window.location='{url}'</script>"  # Open redirect

# ERROR 92: Logging sensitive data
def log_user_action(user, action, details):
    print(f"User {user.email} performed {action}: {details}")  # PII in logs

# ERROR 93: Insufficient access control
def delete_user(user_id):
    # ERROR 94: No authorization check
    return database.delete_user(user_id)

# ERROR 95: Timing attack vulnerability
def compare_passwords(stored, provided):
    # ERROR 96: Not constant time comparison
    return stored == provided

# ERROR 97: Missing CSRF protection
def update_profile(request):
    # ERROR 98: No CSRF token validation
    user_id = request.get('user_id')
    data = request.get('data')
    return update_user_data(user_id, data)

# ERROR 99: Insecure random for crypto
def generate_session_id():
    import random
    return random.randint(100000000, 999999999)  # Not cryptographically secure

# ERROR 100: Missing input length limits
def process_comment(comment):
    # No length validation - potential DoS
    return comment.upper() * 1000  # Memory exhaustion possible

if __name__ == "__main__":
    # ERROR BONUS: No error handling in main
    vm = VulnerableUserManager()
    pn = PerformanceNightmare()
    qi = QualityIssues()
    
    # Trigger some errors
    vm.authenticate_user("admin", "wrong_password")
    pn.fibonacci(40)  # Very slow
    qi.divide_numbers(10, 0)  # Will crash
    
    print("Test completed with 100+ intentional errors")
