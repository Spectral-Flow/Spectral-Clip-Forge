# Copilot Instructions for Spectral Clip Forge

This file provides custom instructions for GitHub Copilot to follow when assisting with code in this repository. These guidelines ensure consistency, quality, and alignment with project architecture.

## Project Overview

**Spectral Clip Forge** is a workspace designed for collaborative development with AI coding agents. The project emphasizes clean architecture, automated workflows, and intelligent tooling integration.

## Code Style & Formatting

### General Principles
- Write clear, self-documenting code with meaningful variable and function names
- Prefer composition over inheritance
- Keep functions small and focused on a single responsibility
- Use defensive programming: validate inputs, handle errors gracefully
- Avoid magic numbers and strings; use named constants

### Language-Specific Guidelines

#### JavaScript/TypeScript
- Use ES6+ syntax (const/let, arrow functions, destructuring, template literals)
- Prefer async/await over raw promises
- Use TypeScript for type safety when possible
- Follow Airbnb style guide conventions
- Use 2 spaces for indentation
- Maximum line length: 100 characters
- Use semicolons consistently
- Quote style: single quotes for strings, backticks for templates

#### Python
- Follow PEP 8 style guide
- Use type hints for function signatures
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter standard)
- Use docstrings for all public modules, functions, classes, and methods
- Prefer f-strings for string formatting

#### YAML
- Use 2 spaces for indentation
- Use lowercase with hyphens for keys
- Quote strings that contain special characters
- Add comments to explain complex configurations

## Documentation Requirements

### Code Comments
- Add comments to explain WHY, not WHAT (code should be self-explanatory)
- Document complex algorithms or business logic
- Use TODO/FIXME/NOTE comments with context
- Keep comments up-to-date with code changes

### README Files
- Every major component should have a README.md
- Include: purpose, usage examples, API reference, dependencies
- Update documentation when adding or changing features

### Commit Messages
- Use conventional commit format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep first line under 72 characters
- Add body for complex changes explaining why and what

## Architecture & Design Patterns

### Project Structure
```
.github/              # GitHub-specific configurations
  workflows/          # CI/CD workflows
  ISSUE_TEMPLATE/     # Issue templates
  copilot-instructions.md
  copilot-setup-steps.yaml
src/                  # Source code
tests/                # Test files
docs/                 # Documentation
```

### Design Principles
- **Separation of Concerns**: Keep business logic, presentation, and data access separate
- **DRY (Don't Repeat Yourself)**: Extract common patterns into reusable components
- **YAGNI (You Aren't Gonna Need It)**: Don't add functionality until it's needed
- **Single Source of Truth**: Configuration, constants, and documentation should have one authoritative source

### Error Handling
- Never swallow exceptions silently
- Provide meaningful error messages
- Log errors with appropriate context
- Use custom error types for domain-specific errors
- Validate inputs at system boundaries

## Testing Guidelines

### Test Coverage
- Aim for 80%+ code coverage
- Focus on critical paths and edge cases
- Test error conditions and invalid inputs
- Include integration tests for key workflows

### Test Structure
- Use Arrange-Act-Assert pattern
- One assertion per test when possible
- Clear, descriptive test names that explain what is being tested
- Mock external dependencies
- Keep tests independent and idempotent

### Test File Organization
- Name test files: `<module>.test.js`, `test_<module>.py`
- Mirror source directory structure in test directory
- Group related tests using describe/context blocks

## Dependencies & Security

### Dependency Management
- Pin exact versions in production
- Keep dependencies up-to-date
- Audit dependencies regularly for security vulnerabilities
- Minimize dependency count; evaluate necessity before adding
- Use Dependabot for automated updates

### Security Best Practices
- Never commit secrets, API keys, or credentials
- Use environment variables for configuration
- Validate and sanitize all user inputs
- Use parameterized queries to prevent injection attacks
- Keep security-sensitive dependencies updated

## CI/CD Guidelines

### Continuous Integration
- All code must pass CI checks before merging
- CI runs: linting, type checking, tests, security scans
- Fix failing tests immediately; don't disable or skip tests
- Keep CI builds fast (under 10 minutes when possible)

### Code Review
- All changes require review before merging
- Review for: correctness, clarity, maintainability, security
- Test the changes locally when applicable
- Check for proper error handling and edge cases

## Git Workflow

### Branching Strategy
- `main` branch is always deployable
- Feature branches: `feature/description`
- Bug fix branches: `fix/description`
- Agent branches: `copilot/description` or `agent/description`

### Pull Requests
- Keep PRs focused and reasonably sized
- Fill out PR template completely
- Link related issues
- Ensure CI passes before requesting review
- Squash commits when merging if history is messy

## Copilot-Specific Instructions

### When Generating Code
- Always check for existing patterns in the codebase and follow them
- Import and reuse existing utilities rather than creating duplicates
- Respect the project's file organization structure
- Add appropriate error handling and validation
- Include inline comments for complex logic

### When Refactoring
- Maintain backward compatibility unless explicitly asked to break it
- Update related tests and documentation
- Keep refactoring commits separate from feature changes
- Run the full test suite after refactoring

### When Fixing Bugs
- Understand the root cause before proposing a fix
- Add test cases that reproduce the bug
- Consider edge cases that might trigger similar bugs
- Document the fix in commit message and code comments if appropriate

### Agent Environment Setup
- Before starting work, refer to `.github/copilot-setup-steps.yaml`
- Ensure all dependencies are installed
- Run linting and tests to verify environment
- Cache dependencies when possible for faster iterations

## Plugin & Extension Rules

### GitHub Actions
- Use official actions from GitHub marketplace when possible
- Pin actions to specific versions (not @main or @latest)
- Add timeout limits to prevent runaway jobs
- Use matrix strategy for testing across multiple environments

### Development Tools
- Use `.editorconfig` for consistent formatting across IDEs
- Configure linters and formatters to run on save
- Use pre-commit hooks for automated quality checks

## Context for AI Agents

When working on issues or pull requests:
1. **Scope the work**: Understand requirements fully before coding
2. **Plan the approach**: Break down into logical steps
3. **Reference files**: Look at existing code for patterns and conventions
4. **Iterate**: Test, get feedback, refine
5. **Document**: Update docs, add comments, write clear commit messages

### Providing Context
- Include relevant file paths when discussing changes
- Reference related issues or PRs
- Explain architectural decisions
- Highlight dependencies between components

## Constraints & Limitations

### Security
- No secrets in code or commits
- No hardcoded credentials
- No committing of sensitive data
- Environment variables for all configuration

### Performance
- Optimize for readability first, performance second
- Profile before optimizing
- Document performance-critical sections
- Consider resource limits in cloud environments

### Compatibility
- Support modern browsers (last 2 versions)
- Use polyfills for older environments if needed
- Test cross-platform compatibility
- Document minimum version requirements

## Summary

These instructions ensure that GitHub Copilot and other AI coding agents work effectively within the Spectral Clip Forge project. By following these guidelines, all generated code will:
- Match the project's style and architecture
- Include proper error handling and tests
- Be well-documented and maintainable
- Pass CI/CD checks
- Integrate seamlessly with existing code

Always refer to these instructions when generating, reviewing, or refactoring code in this repository.
