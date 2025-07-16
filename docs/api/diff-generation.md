# Diff Generation API

The diff generation API allows you to generate HTML diff files for commits in your Git repository.

## Overview

The API provides endpoints to:
- Generate diff files for commits between branches
- Check generation status
- Download generated HTML files
- Clean up generated files

## Quick Start

### 1. Using the Demo Command

```bash
# Make sure the server is running in another terminal
just run

# Run the demo
just demo-diff-generation
```

### 2. Using curl

```bash
# Generate diffs for last 10 commits
curl -X POST http://localhost:8080/api/v1/diffs/generate \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "HEAD",
    "base_branch": "main",
    "max_commits": 10
  }'

# Response: {"task_id": "abc123...", "status": "pending", ...}
```

## API Endpoints

### POST /api/v1/diffs/generate

Start a new diff generation task.

**Request Body:**
```json
{
  "branch": "HEAD",        // Branch to diff (default: "HEAD")
  "base_branch": "main",   // Base branch (default: "main")
  "max_commits": 50        // Maximum commits to process (default: 50)
}
```

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Diff generation started"
}
```

### GET /api/v1/diffs/status/{task_id}

Check the status of a diff generation task.

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",  // "pending", "processing", "completed", "failed"
  "message": "Generated 10 diff files",
  "output_dir": "diff-out-550e8400-e29b-41d4-a716-446655440000",
  "commit_count": 10
}
```

### GET /api/v1/diffs/{task_id}/index.html

Download the generated index.html file.

### GET /api/v1/diffs/{task_id}/files/{filename}

Download a specific diff HTML file.

### DELETE /api/v1/diffs/{task_id}

Clean up generated files and remove task data.

## Example Scripts

### Python Example

See `scripts/demo-diff-generation.py` for a complete Python example.

### Shell Example

See `scripts/diff-api-example.sh` for a curl-based example.

## Requirements

- `diff2html` must be installed: `npm install -g diff2html-cli`
- Git repository with commits to diff
- FastAPI server running

## Notes

- Generated files are stored temporarily on the server
- Use the DELETE endpoint to clean up when done
- The generation runs as a background task
- Large repositories may take time to process