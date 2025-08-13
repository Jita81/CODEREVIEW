#!/usr/bin/env python3
"""
API Handler Module - Realistic Test with 7 Intentional Bugs
RESTful API endpoints with typical web security issues
"""

import json
import subprocess
from flask import Flask, request, jsonify
from user_service import UserService

app = Flask(__name__)
user_service = UserService()

@app.route('/api/users', methods=['GET'])
def get_users():
    # BUG 9: No authentication required for sensitive endpoint
    users = user_service.get_all_users()
    return jsonify(users)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # BUG 10: No input validation
    if user_service.authenticate_user(username, password):
        # BUG 11: Session token predictable pattern
        token = f"token_{username}_{hash(password)}"
        return jsonify({"token": token, "status": "success"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/search', methods=['GET'])
def search_users():
    query = request.args.get('q')
    # BUG 12: Command injection vulnerability
    result = subprocess.run(f"grep {query} /var/log/users.log", 
                          shell=True, capture_output=True, text=True)
    return jsonify({"results": result.stdout})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        # BUG 13: No file type validation
        # BUG 14: Path traversal vulnerability
        filename = request.form.get('filename', file.filename)
        file.save(f"/uploads/{filename}")
        return jsonify({"message": "File uploaded successfully"})

@app.route('/api/eval', methods=['POST'])
def evaluate_expression():
    data = request.get_json()
    expression = data.get('expression')
    # BUG 15: Code injection via eval()
    result = eval(expression)
    return jsonify({"result": result})

if __name__ == '__main__':
    # BUG 16: Debug mode enabled in production-like code
    app.run(debug=True, host='0.0.0.0')
