# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

1. **DO NOT** create a public GitHub issue
2. Email security@jazzydog-labs.com with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes

### What to Expect

- Acknowledgment within 48 hours
- Regular updates on progress
- Credit in security advisories (unless you prefer anonymity)

## Security Measures

### Application Security

- Non-root Docker containers
- Input validation on all endpoints
- SQL injection prevention via parameterized queries
- CORS configured for production use
- Rate limiting available
- Structured logging without sensitive data

### Dependencies

- Regular dependency updates
- Automated vulnerability scanning
- Minimal runtime dependencies

### Best Practices

When deploying Haven:

1. Always use HTTPS in production
2. Enable authentication mechanisms
3. Configure proper CORS origins
4. Use strong database passwords
5. Enable rate limiting
6. Monitor logs for suspicious activity
7. Keep dependencies updated

## Security Headers

Recommended headers for production:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## Disclosure Policy

- Security issues are disclosed after a fix is available
- Users are notified via GitHub Security Advisories
- A 30-day grace period is given for updates