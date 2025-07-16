# Container Developer Experience Improvements

## Description
Address key developer experience issues when working with containerized services, including file permissions, performance, and debugging.

## Acceptance Criteria
- [ ] File permission issues resolved on macOS/Linux
- [ ] Hot reload performance optimized
- [ ] IDE integration documented
- [ ] Debugging workflow established
- [ ] Log management simplified

## Implementation Notes

### File Permissions
- Docker Desktop runs as different user than host
- Options:
  - Run dev containers as root (document security implications)
  - Match container UID to host UID
  - Use USER directive carefully

### Performance Optimization
- Use `:delegated` mount option on macOS
- Exclude heavy directories from mounts (.venv, node_modules)
- Consider sync tools for extreme cases

### IDE Integration
- Document remote interpreter setup
- Provide debugger port configuration
- Consider shared .venv mount option

### Debugging Setup
```yaml
# docker-compose.override.yml
services:
  api:
    environment:
      - DEBUGGER=true
    ports:
      - "5678:5678"  # Python debugger port
```

## Definition of Done
- [ ] Permission strategy documented and tested
- [ ] Performance benchmarked and optimized
- [ ] IDE setup guide created
- [ ] Debug configuration working
- [ ] Team onboarding tested
- [ ] Work log entry added