# Contributing to AI Code Review Tool

Thank you for your interest in contributing to the AI Code Review Tool! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating a new issue, please:

1. Check if the issue has already been reported
2. Use the appropriate issue template
3. Provide detailed information including:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages or logs

### Suggesting Features

We welcome feature suggestions! Please:

1. Check if the feature has already been requested
2. Explain the use case and benefits
3. Consider implementation complexity
4. Be open to discussion and iteration

### Code Contributions

#### Development Setup

1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/ai-code-review.git
   cd ai-code-review
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

#### Making Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below

3. Test your changes:
   ```bash
   # Run tests
   python -m pytest
   
   # Run linting
   python -m flake8 ai_code_review_tool.py
   
   # Test the tool locally
   python ai_code_review_tool.py --help
   ```

4. Commit your changes with a clear message:
   ```bash
   git commit -m "feat: add new perspective for API security"
   ```

5. Push to your fork and create a pull request

#### Pull Request Guidelines

- Use descriptive titles
- Include a summary of changes
- Reference related issues
- Ensure all tests pass
- Update documentation if needed
- Follow the commit message format below

## 📝 Code Standards

### Python Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and under 50 lines
- Use meaningful variable names

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```
feat(review): add new security perspective
fix(cache): handle cache corruption gracefully
docs(readme): update installation instructions
```

### Testing

- Write tests for new features
- Ensure existing tests pass
- Use descriptive test names
- Mock external dependencies
- Test edge cases and error conditions

## 🏗️ Project Structure

```
ai-code-review/
├── .github/
│   └── workflows/
│       └── ai-code-review.yml
├── ai_code_review_tool.py      # Main tool
├── ai_code_review_documentation.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements-dev.txt
└── tests/
    └── test_ai_review.py
```

## 🔧 Development Tools

### Required Tools

- Python 3.11+
- Git
- A text editor or IDE

### Recommended Tools

- VS Code with Python extension
- Pre-commit hooks for code quality
- Docker for testing in different environments

### Development Dependencies

Create `requirements-dev.txt`:

```
pytest>=7.0.0
flake8>=6.0.0
black>=23.0.0
mypy>=1.0.0
pre-commit>=3.0.0
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=ai_code_review_tool

# Run specific test file
python -m pytest tests/test_ai_review.py

# Run with verbose output
python -m pytest -v
```

### Test Structure

- Unit tests for individual functions
- Integration tests for the full workflow
- Mock external API calls
- Test error conditions and edge cases

## 📚 Documentation

### Code Documentation

- Use docstrings for all public functions
- Include type hints
- Provide usage examples
- Document exceptions and error conditions

### User Documentation

- Keep README.md up to date
- Update documentation for new features
- Include examples and use cases
- Maintain troubleshooting guides

## 🔒 Security

### Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do not** create a public issue
2. Email security@your-domain.com
3. Include detailed information about the vulnerability
4. Allow time for assessment and response

### Security Guidelines

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all inputs
- Follow secure coding practices
- Keep dependencies updated

## 🎯 Areas for Contribution

### High Priority

- [ ] Add support for more programming languages
- [ ] Improve error handling and recovery
- [ ] Add configuration file support
- [ ] Enhance caching mechanisms
- [ ] Add more review perspectives

### Medium Priority

- [ ] Create a web interface
- [ ] Add integration with other CI/CD platforms
- [ ] Improve performance for large codebases
- [ ] Add custom perspective templates
- [ ] Create a plugin system

### Low Priority

- [ ] Add support for different LLM providers
- [ ] Create IDE extensions
- [ ] Add historical analysis and trends
- [ ] Create a dashboard for metrics
- [ ] Add team collaboration features

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the project's coding standards
- Be patient with newcomers

### Communication

- Use clear and concise language
- Ask questions when unsure
- Provide context for suggestions
- Be open to different approaches
- Celebrate contributions and successes

## 📞 Getting Help

- Check the documentation first
- Search existing issues and discussions
- Ask questions in GitHub Discussions
- Join our community chat (if available)
- Email maintainers for private concerns

## 🙏 Recognition

Contributors will be recognized in:

- The project README
- Release notes
- Contributor hall of fame
- GitHub contributors page

Thank you for contributing to making AI Code Review Tool better! 🚀
