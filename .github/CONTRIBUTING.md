# Contributing to Spectral Clip Forge

Thank you for your interest in contributing to Spectral Clip Forge! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Working with Copilot Agents](#working-with-copilot-agents)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members
- Gracefully accept constructive criticism

## Getting Started

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Spectral-Clip-Forge.git
   cd Spectral-Clip-Forge
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/Spectral-Flow/Spectral-Clip-Forge.git
   ```
4. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

The project uses `.github/copilot-setup-steps.yaml` to define the setup process. Follow these steps:

### Prerequisites

- Git
- Node.js 18+ (for JavaScript/TypeScript projects)
- Python 3.9+ (for Python projects)
- Your preferred code editor (VS Code recommended for Copilot integration)

### Installation

1. **Install dependencies**:
   ```bash
   # For Node.js projects
   npm install
   
   # For Python projects
   pip install -r requirements.txt
   # or
   poetry install
   ```

2. **Verify installation**:
   ```bash
   # Run tests
   npm test  # or pytest
   
   # Run linters
   npm run lint  # or black . && flake8 .
   ```

### IDE Setup

For the best experience with GitHub Copilot:

1. Install [VS Code](https://code.visualstudio.com/)
2. Install the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
3. Sign in with your GitHub account
4. The repository's `.github/copilot-instructions.md` will automatically guide Copilot

## How to Contribute

### Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) when creating an issue:

1. Search existing issues to avoid duplicates
2. Provide detailed reproduction steps
3. Include environment information
4. Add relevant logs and error messages

### Suggesting Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml):

1. Clearly describe the problem you're trying to solve
2. Explain your proposed solution
3. Consider alternatives
4. Indicate if you're willing to implement it

### Creating Agent Tasks

For tasks suitable for AI agents, use the [Agent Task template](.github/ISSUE_TEMPLATE/agent_task.yml):

1. Define clear, specific objectives
2. Provide relevant context and files
3. List requirements and acceptance criteria
4. Specify constraints and guidelines

## Coding Guidelines

Follow the guidelines in `.github/copilot-instructions.md`. Key points:

### Style

- **JavaScript/TypeScript**: Follow Airbnb style guide, use ES6+, 2-space indentation
- **Python**: Follow PEP 8, use type hints, 4-space indentation
- **YAML**: 2-space indentation, lowercase with hyphens

### Best Practices

- Write self-documenting code with meaningful names
- Keep functions small and focused
- Add comments to explain "why", not "what"
- Handle errors gracefully
- Validate inputs at boundaries
- Write tests for new functionality

### Testing

- Aim for 80%+ code coverage
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests independent and idempotent

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(auth): add JWT authentication middleware

Implements token-based authentication for protected routes.
Includes refresh token support.

Closes #123
```

```
fix(api): handle null response in user service

Adds null check before accessing response.data to prevent
TypeError when API returns empty response.

Fixes #456
```

## Pull Request Process

1. **Update your branch** with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests and linting**:
   ```bash
   npm test && npm run lint  # or equivalent for your stack
   ```

3. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**:
   - Use the [PR template](.github/PULL_REQUEST_TEMPLATE/pull_request_template.md)
   - Link related issues
   - Provide clear description of changes
   - Include test evidence
   - Add screenshots for UI changes

5. **Respond to feedback**:
   - Address review comments promptly
   - Push updates to the same branch
   - Request re-review when ready

6. **Merge**:
   - Ensure CI passes
   - Obtain required approvals
   - Squash commits if history is messy
   - Delete branch after merge

## Working with Copilot Agents

This project is designed to work seamlessly with GitHub Copilot and AI coding agents.

### For Contributors Using Copilot

- Copilot will automatically reference `.github/copilot-instructions.md`
- Follow the suggestions but review them critically
- Copilot helps with boilerplate, patterns, and consistency

### For Agent-Driven Development

When creating tasks for agents:

1. **Be specific**: Clear objectives lead to better results
2. **Provide context**: Reference relevant files and patterns
3. **Set constraints**: Specify what to avoid or preserve
4. **Define success**: Clear acceptance criteria
5. **Review output**: Always review and test agent-generated code

### Agent Setup

Agents should follow `.github/copilot-setup-steps.yaml` to:
- Install dependencies
- Configure development environment
- Run initial tests and builds
- Verify environment readiness

## Questions?

- Check the [documentation](docs/)
- Search [existing issues](https://github.com/Spectral-Flow/Spectral-Clip-Forge/issues)
- Ask in [discussions](https://github.com/Spectral-Flow/Spectral-Clip-Forge/discussions)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Spectral Clip Forge! 🚀
