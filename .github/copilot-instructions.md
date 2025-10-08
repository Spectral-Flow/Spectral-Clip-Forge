# Copilot Instructions for Spectral Clip Forge

## Project Overview

**Spectral Clip Forge** is a legendary artifact within the Eternis-33 universe—a platform that transforms raw audio/video into social-ready clips (TikTok, YouTube Shorts, Instagram Reels) with mythic branding and Spectral Flow aesthetics.

## Architecture & Technology Stack

### Core Technologies
- **Backend**: Python (FastAPI/Flask) for API and processing pipeline
- **Video Processing**: FFmpeg for transcoding, clipping, and effects
- **Frontend**: Modern JavaScript/TypeScript (React or Vue.js)
- **Containerization**: Docker for isolated, secure processing
- **Storage**: Local filesystem with optional cloud integration (S3, etc.)

### Security Architecture
- All file uploads processed in isolated Docker containers or VMs
- Malware scanning on all uploads (ClamAV integration)
- Rate limiting on API endpoints (per-user and per-IP)
- No secrets in source code—use environment variables
- Audit logging for all user actions and processing events

## Coding Standards

### Python
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use `black` for formatting, `flake8` for linting, `mypy` for type checking
- Write docstrings for all public functions (Google style)

### JavaScript/TypeScript
- Follow ESLint standard configuration
- Use Prettier for formatting
- Prefer functional components in React
- Use async/await over raw Promises
- Maximum line length: 100 characters

### General
- Write self-documenting code with clear variable names
- Keep functions small and focused (single responsibility)
- Prefer composition over inheritance
- No magic numbers—use named constants

## Project Structure

```
spectral-clip-forge/
├── .github/                    # GitHub configuration
├── backend/                    # Python backend API
│   ├── api/                   # API routes
│   ├── processing/            # Video processing logic
│   ├── security/              # Security utilities
│   └── tests/                 # Backend tests
├── frontend/                   # Web UI
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API clients
│   │   └── styles/           # CSS/styling
│   └── public/               # Static assets
├── docker/                     # Docker configurations
├── docs/                       # Documentation
└── scripts/                    # Build/deployment scripts
```

## Branding Guidelines

### Visual Identity
- **Primary Color**: Spectral Purple (#8B5CF6, #7C3AED)
- **Secondary Colors**: Neon accents (cyan #06B6D4, magenta #EC4899)
- **Typography**: Modern, bold fonts for headers; clean sans-serif for body
- **Effects**: Tribal patterns, glowing neon overlays, mythic symbols

### Voice & Tone
- **Mythic & Immersive**: Use legendary, artifact-forging language
- **Empowering**: Users are "forgers" creating "artifacts"
- **Professional**: Clear, helpful, avoiding jargon when explaining technical concepts
- **Examples**:
  - ✅ "Forge your legendary clip"
  - ✅ "Artifact processing in progress..."
  - ✅ "Your creation is ready to share across realms"
  - ❌ "Upload file"
  - ❌ "Processing..."

### Watermarks & Overlays
- All clips include Spectral Flow watermark (bottom-right or top-right)
- Optional: Spectra artifact symbol overlay
- Subtitle styling: bold, outlined text with purple glow
- Transitions: fade, glitch effects aligned with brand

## Testing Requirements

### Unit Tests
- Minimum 80% code coverage for core business logic
- Use `pytest` for Python, `Jest` for JavaScript
- Mock external dependencies (file I/O, network calls)
- Test edge cases and error conditions

### Integration Tests
- Test full processing pipeline (upload → process → download)
- Test API endpoints with various input formats
- Verify security controls (rate limiting, file validation)

### E2E Tests
- Use Playwright or Cypress for frontend flows
- Test complete user journeys
- Verify generated clips meet platform requirements

## Video Processing Guidelines

### Output Formats
- **TikTok**: H.264/AAC, 720×1280 (9:16), 60fps max, <50MB
- **YouTube Shorts**: H.264/AAC, 1080×1920 (9:16), 60fps max
- **Instagram Reels**: H.264/AAC, 1080×1920 (9:16), 30fps, <100MB
- **Universal**: H.264/AAC with fallback settings

### Processing Pipeline
1. **Validation**: Check file type, size, duration
2. **Malware Scan**: Run ClamAV check
3. **Transcoding**: Convert to target format using FFmpeg
4. **Effects**: Apply watermark, overlays, subtitles
5. **Optimization**: Compress while maintaining quality
6. **Output**: Save to user-specific directory

### FFmpeg Best Practices
- Use hardware acceleration when available (`-hwaccel`)
- Optimize for speed: `-preset fast` or `-preset medium`
- Quality settings: `-crf 23` for H.264
- Audio: `-b:a 128k` for AAC
- Always handle errors and log FFmpeg output

## Error Handling

### Principles
- Never crash on bad input—validate early, fail gracefully
- Return meaningful error messages to users
- Log all errors with context (user ID, file name, timestamp)
- Use appropriate HTTP status codes (400 for client errors, 500 for server errors)

### User-Facing Messages
- **Validation Errors**: "This file format is not supported. Please upload MP4, MOV, or AVI."
- **Processing Errors**: "We encountered an issue forging your artifact. Please try again."
- **System Errors**: "Our systems are temporarily unavailable. Please try again in a few moments."

## Security Practices

### Input Validation
- Whitelist allowed file extensions (.mp4, .mov, .avi, .mp3, .wav)
- Check MIME types, not just extensions
- Limit file size (default: 500MB max)
- Validate duration (default: 60 minutes max)

### Rate Limiting
- Per-user: 10 uploads per hour
- Per-IP: 50 requests per hour (API endpoints)
- Failed attempts: Exponential backoff after 5 failures

### Data Handling
- Delete temporary files after processing
- Purge user uploads after 7 days (or per user preference)
- Never log sensitive data (passwords, tokens)
- Encrypt data at rest if storing user content

## Documentation Standards

### README Files
- Clear installation instructions
- Usage examples with expected output
- Troubleshooting section
- Contributing guidelines
- Link to Eternis-33 lore/universe

### Code Comments
- Explain "why," not "what" (code should be self-documenting)
- Document complex algorithms or non-obvious logic
- Include links to relevant documentation or issues
- Use TODO comments sparingly—create issues instead

### API Documentation
- Use OpenAPI/Swagger for REST APIs
- Document all endpoints, parameters, responses
- Include example requests and responses
- Note authentication requirements

## Git Workflow

### Branches
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features (e.g., `feature/subtitle-generator`)
- `fix/*`: Bug fixes (e.g., `fix/audio-sync-issue`)
- `hotfix/*`: Critical production fixes

### Commit Messages
- Follow Conventional Commits specification
- Format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples:
  - `feat(processing): add subtitle generation with AI`
  - `fix(api): handle timeout errors in video upload`
  - `docs(readme): update installation instructions`

### Pull Requests
- Reference related issues (`Closes #123`)
- Include screenshots for UI changes
- Ensure all tests pass and CI is green
- Request review from at least one maintainer
- Keep PRs focused—one feature/fix per PR

## CI/CD Pipeline

### Build Steps
1. Install dependencies
2. Run linters (black, flake8, mypy, eslint, prettier)
3. Run unit tests
4. Run integration tests
5. Build Docker images
6. Security scan (dependency vulnerabilities)

### Deployment
- Automatic deployment to staging from `develop` branch
- Manual approval for production deployment from `main`
- Rollback capability for failed deployments
- Health checks after deployment

## Environment Variables

### Required Variables
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection string (if using DB)
- `STORAGE_PATH`: Local path for file storage
- `MAX_FILE_SIZE`: Maximum upload size in bytes
- `CLAMAV_HOST`: ClamAV server address

### Optional Variables
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: For S3 storage
- `SENTRY_DSN`: Error tracking
- `REDIS_URL`: For caching and rate limiting

## Copilot Workflow Integration

### When to Use Copilot
- Generating boilerplate code (API routes, tests)
- Writing docstrings and comments
- Suggesting error handling patterns
- Creating test cases
- Refactoring repetitive code

### What to Review Carefully
- Security-sensitive code (authentication, file handling)
- Complex business logic
- Database queries and migrations
- Third-party integrations

### Best Practices with Copilot
- Always review and test generated code
- Customize suggestions to match project style
- Use specific, descriptive function names for better suggestions
- Provide context in comments for complex tasks

## Plugin & Extension Rules

### FFmpeg Plugins
- Use only open-source, well-maintained filters
- Test plugins thoroughly before production use
- Document any custom filters in processing pipeline

### Frontend Libraries
- Prefer lightweight, tree-shakeable libraries
- Avoid jQuery—use vanilla JS or framework utilities
- Check license compatibility (prefer MIT, Apache 2.0)

### Python Packages
- Pin major versions in requirements.txt
- Use virtual environments for development
- Regular security audits with `pip-audit` or `safety`

## Accessibility

- Follow WCAG 2.1 Level AA standards
- Ensure keyboard navigation for all UI elements
- Provide alt text for images and icons
- Use semantic HTML
- Support screen readers
- Maintain sufficient color contrast (4.5:1 minimum)

## Performance Targets

- API response time: <200ms for non-processing endpoints
- Video processing: <30 seconds for 1-minute clip
- Frontend load time: <3 seconds on 3G connection
- Concurrent users: Support 100+ simultaneous uploads

## Licensing

- Code licensed under AGPL-3.0 (or dual license for commercial use)
- All third-party code must be compatible with AGPL-3.0
- Document any commercial licensing exceptions
- Include proper attribution for all dependencies

## References

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Eternis-33 Universe Bible](https://github.com/Spectral-Flow/Eternis-33-Bible) (lore and branding)
- [TikTok Video Specifications](https://support.tiktok.com/en/using-tiktok/creating-videos/video-formats)
- [YouTube Shorts Requirements](https://support.google.com/youtube/answer/10059070)
- [Instagram Reels Guidelines](https://help.instagram.com/270447560766967)

---

**Remember**: You are forging legendary artifacts in the Spectral Flow universe. Every line of code, every feature, every user interaction should embody the mythic, immersive experience that defines this project. Code with precision, test with rigor, and ship with confidence.
