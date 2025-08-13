# Demo Application

This is a simple demo application to test the AI Code Review Tool.

## Features

- User input handling
- Database query processing
- Fibonacci calculation
- Error handling

## Usage

```bash
python demo/test_app.py
```

## Testing with AI Review

To test the AI review tool with this demo:

```bash
# From the root directory
python ai_code_review_tool.py demo/test_app.py --output json --no-cache
```

This will analyze the demo code for:
- Security vulnerabilities (SQL injection)
- Performance issues (inefficient algorithms)
- Code quality issues
