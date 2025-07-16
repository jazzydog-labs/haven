# Haven CLI Tool

The Haven CLI provides command-line access to git diff generation and analysis features.

## Installation

The CLI is automatically installed when you install the Haven API package:

```bash
cd apps/api
pip install -e ".[dev]"
```

This installs the `haven-cli` command globally.

## Commands

### `haven-cli list-commits`

List commits that would be included in diff generation.

```bash
# List commits on current branch vs main
haven-cli list-commits

# List commits in specific repository
haven-cli list-commits --repo-path /path/to/repo

# List commits vs different base branch
haven-cli list-commits --base-branch develop
```

**Options:**
- `--repo-path, -r`: Path to git repository (default: current directory)
- `--base-branch, -b`: Base branch for comparison (default: main)

### `haven-cli generate`

Generate diff files for all commits in the repository.

```bash
# Generate diffs with default settings
haven-cli generate

# Generate with verbose output
haven-cli generate --verbose

# Specify output directory
haven-cli generate --output-dir my-diffs

# Generate for specific repository and base branch
haven-cli generate --repo-path /path/to/repo --base-branch develop
```

**Options:**
- `--repo-path, -r`: Path to git repository (default: current directory)
- `--base-branch, -b`: Base branch for comparison (default: main)
- `--output-dir, -o`: Output directory for diff files (default: diff-output)
- `--verbose, -v`: Verbose output

**Output:**
- Individual `.diff` files for each commit
- `index.md` file with summary and links to all diffs

## Examples

### Basic Usage

```bash
# List what commits would be processed
haven-cli list-commits

# Generate diffs for current repository
haven-cli generate --verbose

# View results
cat diff-output/index.md
```

### Advanced Usage

```bash
# Generate diffs for feature branch vs develop
haven-cli generate \
  --repo-path ~/projects/my-app \
  --base-branch develop \
  --output-dir feature-diffs \
  --verbose
```

### Integration with Just Commands

The Haven project includes integration with Just commands:

```bash
# Alternative ways to generate diffs
just demo-diff-generation  # Uses API server
haven-cli generate         # Direct CLI tool
```

## Output Format

The CLI generates:

1. **Individual diff files**: `01-abc12345-commit-message.diff`
   - Numbered sequentially
   - Include short commit hash
   - Sanitized commit message in filename

2. **Index file**: `index.md`
   - Markdown summary of all commits
   - Links to individual diff files
   - Commit metadata (hash, author, date)

## Error Handling

The CLI provides clear error messages for common issues:

- **Not a git repository**: Ensure you're in a git repository
- **Base branch not found**: Check that the base branch exists
- **No commits found**: May indicate you're already on the base branch

## Performance

- Uses async operations for better performance
- Processes commits sequentially to maintain order
- Minimal memory usage for large repositories
- Progress indicators with `--verbose` flag

## See Also

- [API Documentation](api/diff-generation.md) - Web API for diff generation
- [Demo Scripts](../scripts/) - Automated demo workflows
- [Architecture](architecture.md) - System design and patterns