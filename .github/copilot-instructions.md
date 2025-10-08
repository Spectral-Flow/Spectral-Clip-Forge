# Copilot Instructions for Spectral-Clip-Forge

## Repository Overview
Spectral-Clip-Forge is a project focused on spectral analysis and clip processing. This repository contains tools and utilities for working with spectral data and media clips.

## Code Style and Conventions

### General Guidelines
- Write clean, maintainable, and well-documented code
- Follow the principle of least surprise - code should behave as expected
- Prioritize readability over cleverness
- Keep functions small and focused on a single responsibility

### Naming Conventions
- Use descriptive and meaningful names for variables, functions, and classes
- Follow language-specific naming conventions (e.g., camelCase for JavaScript, snake_case for Python)
- Constants should be in UPPER_CASE
- Private methods/properties should be prefixed with underscore where applicable

### Comments and Documentation
- Write self-documenting code where possible
- Add comments to explain "why" rather than "what"
- Document complex algorithms and business logic
- Keep documentation up-to-date with code changes
- Use docstrings for functions and classes in Python
- Use JSDoc for JavaScript/TypeScript functions

## Development Workflow

### Version Control
- Write clear, concise commit messages
- Keep commits atomic - one logical change per commit
- Reference issue numbers in commit messages when applicable
- Always create feature branches for new work

### Code Quality
- Run linters before committing code
- Ensure all tests pass before pushing changes
- Write tests for new features and bug fixes
- Maintain or improve code coverage

## Testing Practices

### Test Strategy
- Write unit tests for individual components
- Include integration tests for component interactions
- Add end-to-end tests for critical user workflows
- Use descriptive test names that explain what is being tested

### Test Coverage
- Aim for high test coverage on critical paths
- Test both happy paths and edge cases
- Test error handling and validation logic

## Documentation Standards

### Code Documentation
- Document public APIs and interfaces
- Include usage examples in documentation
- Keep README.md up-to-date with project changes
- Document configuration options and environment variables

### Project Documentation
- Maintain clear installation instructions
- Document development setup and requirements
- Include contribution guidelines
- Keep dependency documentation current

## Best Practices for AI Assistance

### When Making Changes
- Always understand the context before making modifications
- Preserve existing code style and patterns
- Make minimal, surgical changes to achieve the goal
- Test changes thoroughly before committing
- Update related documentation when changing functionality

### When Adding Features
- Discuss design approach before implementation
- Follow existing architectural patterns
- Add appropriate tests for new functionality
- Update README and other docs as needed

### When Fixing Bugs
- Reproduce the bug before fixing
- Add a test that would have caught the bug
- Ensure the fix doesn't break existing functionality
- Document the root cause if it's non-obvious
