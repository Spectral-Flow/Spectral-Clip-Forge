# Contributing to Spectral Clip Forge

🔥 Welcome, aspiring Forge Master! 🔥

Thank you for your interest in contributing to the Spectral Clip Forge. We welcome contributions from the community.

## Code of Conduct

Be respectful, collaborative, and constructive. We're building legendary artifacts together.

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - OS and Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. Check existing feature requests
2. Describe the use case
3. Explain how it fits the Spectral Flow vision
4. Consider backward compatibility

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Lint your code: `black . && flake8`
7. Commit with descriptive messages
8. Push to your fork
9. Open a Pull Request

### Code Style

- Follow PEP 8 (enforced by flake8)
- Use Black for formatting
- Write docstrings for functions/classes
- Keep the mythic/legendary tone in user-facing text

### Testing

- Add tests for new features
- Maintain test coverage above 70%
- Test both success and failure cases

### Documentation

- Update README for significant changes
- Add docstrings to new code
- Update API documentation if needed

## Development Setup

```bash
# Clone the repo
git clone https://github.com/Spectral-Flow/Spectral-Clip-Forge.git
cd Spectral-Clip-Forge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run tests
pytest

# Run the application
python app.py
```

## Commit Message Format

```
type: Brief description

Detailed explanation if needed.

Fixes #issue_number
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Questions?

Open a discussion in GitHub Discussions or reach out to the maintainers.

---

May the Spectral Flow guide your code! ⚡
