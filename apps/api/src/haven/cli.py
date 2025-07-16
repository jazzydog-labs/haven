#!/usr/bin/env python3
"""Haven CLI tool for git diff generation and analysis."""

import asyncio
import re
import sys
from pathlib import Path
from typing import NamedTuple

import click
from rich.console import Console
from rich.table import Table

console = Console()


class GitCommit(NamedTuple):
    """Represents a git commit."""
    hash: str
    message: str
    author: str
    date: str


async def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[str, str, int]:
    """Run a shell command asynchronously."""
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode(), process.returncode or 0


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Sanitize text for use in filenames."""
    sanitized = re.sub(r"[^a-zA-Z0-9]", "-", text)
    return sanitized[:max_length]


async def check_diff2html() -> None:
    """Check if diff2html is installed."""
    _, _, returncode = await run_command(["which", "diff2html"])
    if returncode != 0:
        # Try to install it
        _, stderr, returncode = await run_command(["npm", "install", "-g", "diff2html-cli"])
        if returncode != 0:
            raise RuntimeError(f"Failed to install diff2html: {stderr}")


async def get_git_commits(repo_path: Path, base_branch: str = "main", max_commits: int = 50) -> list[GitCommit]:
    """Get list of commits from git repository."""
    # Check if we're in a git repository
    stdout, stderr, returncode = await run_command(
        ["git", "rev-parse", "--git-dir"], cwd=repo_path
    )
    if returncode != 0:
        raise RuntimeError(f"Not a git repository: {repo_path}")

    # Get commits from the specified branch (or current branch if base_branch is HEAD)
    if base_branch == "HEAD":
        # Use current branch
        stdout, stderr, returncode = await run_command(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path
        )
        if returncode != 0:
            raise RuntimeError(f"Failed to get current branch: {stderr}")
        target_branch = stdout.strip()
    else:
        target_branch = base_branch

    # Get recent commits on the target branch in reverse chronological order (oldest first)
    cmd = [
        "git",
        "log",
        "--reverse",
        f"--max-count={max_commits}",
        "--pretty=format:%H|%s|%an|%ad",
        "--date=short",
        target_branch,
    ]

    stdout, stderr, returncode = await run_command(cmd, cwd=repo_path)
    if returncode != 0:
        raise RuntimeError(f"Failed to get commits: {stderr}")

    commits: list[GitCommit] = []
    for line in stdout.strip().split("\n"):
        if line:
            parts = line.split("|", 3)
            if len(parts) == 4:
                commits.append(GitCommit(
                    hash=parts[0],
                    message=parts[1],
                    author=parts[2],
                    date=parts[3],
                ))

    return commits


async def generate_diff_for_commit(
    commit: GitCommit,
    output_dir: Path,
    repo_path: Path,
    commit_number: int
) -> str:
    """Generate HTML diff file for a single commit using diff2html."""
    # Generate filename
    safe_message = sanitize_filename(commit.message)
    filename = f"{commit_number:02d}-{commit.hash[:8]}-{safe_message}.html"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate diff HTML using diff2html (commit vs its parent)
    diff_cmd = [
        "diff2html",
        "-s", "side",
        "-f", "html",
        "-F", str(output_dir / filename),
        "-t", f"{commit.hash[:8]}: {commit.message}",
        "--summary", "open",
        "--highlightCode",
        "--", f"{commit.hash}^..{commit.hash}",
    ]

    _, stderr, returncode = await run_command(diff_cmd, cwd=repo_path)
    if returncode != 0:
        console.print(f"[yellow]Warning: Could not generate diff for {commit.hash[:8]}: {stderr}[/yellow]")
        return ""

    return filename


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Haven CLI - Git diff generation and analysis tool."""
    pass


@cli.command()
@click.option(
    "--repo-path",
    "-r",
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help="Path to git repository (default: current directory)",
)
@click.option(
    "--base-branch",
    "-b",
    default="main",
    help="Branch to generate diffs from (default: main)",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("diff-output"),
    help="Output directory for diff files (default: diff-output)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
@click.option(
    "--max-commits",
    "-n",
    default=50,
    help="Maximum number of commits to process (default: 50)",
)
def generate(
    repo_path: Path,
    base_branch: str,
    output_dir: Path,
    verbose: bool,
    max_commits: int,
):
    """Generate diff files for all commits from the specified branch (each commit vs its parent)."""
    if verbose:
        console.print(f"[blue]Repository:[/blue] {repo_path}")
        console.print(f"[blue]Base branch:[/blue] {base_branch}")
        console.print(f"[blue]Output directory:[/blue] {output_dir}")

    try:
        # Ensure output directory exists with parents
        output_dir.mkdir(parents=True, exist_ok=True)

        # Run the async diff generation
        asyncio.run(
            _generate_diffs_async(
                repo_path=repo_path,
                base_branch=base_branch,
                output_dir=output_dir,
                verbose=verbose,
                max_commits=max_commits,
            )
        )

        console.print("\n[green]✅ Diff generation complete![/green]")
        console.print(f"[dim]Output saved to: {output_dir}[/dim]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


async def _generate_diffs_async(
    repo_path: Path,
    base_branch: str,
    output_dir: Path,
    verbose: bool,
    max_commits: int = 50,
):
    """Async helper for diff generation."""
    # Ensure we have absolute paths
    repo_path = repo_path.resolve()
    output_dir = output_dir.resolve()

    # Get commits
    if verbose:
        console.print("\n[yellow]📋 Getting commit list...[/yellow]")

    commits = await get_git_commits(repo_path, base_branch, max_commits=max_commits)

    if not commits:
        console.print("[yellow]⚠️ No commits found[/yellow]")
        console.print(f"[dim]Tip: Branch '{base_branch}' may not exist or have no commits. Try:[/dim]")
        console.print("[dim]  haven-cli generate --base-branch HEAD  # Use current branch[/dim]")
        console.print("[dim]  haven-cli list-commits --base-branch HEAD  # List commits on current branch[/dim]")
        # Still create an index file for empty state
        create_index_file(output_dir, [], [])
        index_path = output_dir / "index.html"
        console.print(f"[blue]📄 Empty index created: file://{index_path.absolute()}[/blue]")
        return

    if verbose:
        console.print(f"[green]Found {len(commits)} commits[/green]")

    # Check diff2html availability
    if verbose:
        console.print("\n[yellow]🔧 Checking diff2html...[/yellow]")

    try:
        await check_diff2html()
        if verbose:
            console.print("[green]✅ diff2html is available[/green]")
    except RuntimeError as e:
        console.print(f"[red]❌ diff2html setup failed: {e}[/red]")
        return

    # Generate diffs
    if verbose:
        console.print("\n[yellow]🔄 Generating HTML diffs...[/yellow]")

    generated_files: list[str] = []
    for i, commit in enumerate(commits, 1):
        if verbose:
            console.print(f"[dim]Processing commit {i}/{len(commits)}: {commit.hash[:8]}[/dim]")

        filename = await generate_diff_for_commit(commit, output_dir, repo_path, i)
        if filename:
            generated_files.append(filename)

    # Generate summary
    if verbose:
        console.print(f"\n[green]Generated {len(generated_files)} HTML diff files[/green]")

    # Create index file
    create_index_file(output_dir, commits, generated_files)

    # Output clickable link to index
    index_path = output_dir / "index.html"
    console.print(f"[blue]📄 View results: file://{index_path.absolute()}[/blue]")


def create_index_file(output_dir: Path, commits: list[GitCommit], diff_files: list[str]):
    """Create an index.html file listing all commits and diffs."""
    from datetime import datetime

    # Calculate stats
    unique_authors = len({c.author for c in commits})
    date_range = f"{commits[0].date} - {commits[-1].date}" if commits else "No date range"

    # Generate JavaScript array
    commit_data_lines: list[str] = []
    for i, (commit, diff_file) in enumerate(zip(commits, diff_files), 1):
        if diff_file:  # Only include files that were successfully generated
            escaped_message = commit.message.replace('"', '\\"')
            commit_data_lines.append(
                f"{{number: {i}, hash: '{commit.hash[:8]}', "
                f"message: \"{escaped_message}\", author: '{commit.author}', "
                f"date: '{commit.date}', file: '{diff_file}'}}"
            )
    commit_data = ",\n            ".join(commit_data_lines)

    # HTML template (simplified version of API template)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haven CLI - Commit Diff Index</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #0366d6;
            padding-bottom: 10px;
        }}
        .info {{
            background-color: #e3f2fd;
            border-left: 4px solid #0366d6;
            padding: 10px 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}
        .stats {{
            margin: 20px 0;
            display: flex;
            gap: 20px;
        }}
        .stat {{
            background-color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #0366d6;
        }}
        .stat-label {{
            font-size: 14px;
            color: #586069;
            margin-top: 5px;
        }}
        .commit-list {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .commit {{
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid #e1e4e8;
            transition: background-color 0.2s;
        }}
        .commit:hover {{
            background-color: #f6f8fa;
        }}
        .commit:last-child {{
            border-bottom: none;
        }}
        .commit-number {{
            flex-shrink: 0;
            width: 40px;
            height: 40px;
            background-color: #0366d6;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }}
        .commit-details {{
            flex-grow: 1;
            min-width: 0;
        }}
        .commit-message {{
            font-weight: 500;
            color: #0366d6;
            text-decoration: none;
            display: block;
            margin-bottom: 5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .commit-message:hover {{
            text-decoration: underline;
        }}
        .commit-meta {{
            font-size: 14px;
            color: #586069;
        }}
        .commit-hash {{
            font-family: monospace;
            background-color: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h1>Haven CLI - Commit Diff Index</h1>

    <div class="info">
        <strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
        <strong>Total Commits:</strong> {len(commits)}
    </div>

    <div class="stats">
        <div class="stat">
            <div class="stat-value">{len(commits)}</div>
            <div class="stat-label">Total Commits</div>
        </div>
        <div class="stat">
            <div class="stat-value">{unique_authors}</div>
            <div class="stat-label">Contributors</div>
        </div>
        <div class="stat">
            <div class="stat-value">{date_range}</div>
            <div class="stat-label">Date Range</div>
        </div>
    </div>

    <div class="commit-list">
        <!-- Commits will be inserted here -->
    </div>

    <script>
        // Commit data
        const commits = [
            {commit_data}
        ];

        // Populate commit list
        const commitList = document.querySelector('.commit-list');

        if (commits.length === 0) {{
            // Show helpful message when no commits found
            const emptyDiv = document.createElement('div');
            emptyDiv.style.cssText = 'padding: 40px 20px; text-align: center; color: #586069;';
            emptyDiv.innerHTML = `
                <h3 style="margin-bottom: 10px;">No commits found</h3>
                <p style="margin-bottom: 20px;">The specified branch may not exist or have no commits.</p>
                <div style="background: #f6f8fa; padding: 15px; border-radius: 6px; text-align: left; max-width: 500px; margin: 0 auto;">
                    <strong>Try these commands:</strong><br>
                    <code style="display: block; margin: 5px 0;">haven-cli generate --base-branch HEAD</code>
                    <code style="display: block; margin: 5px 0;">haven-cli list-commits --base-branch HEAD</code>
                    <code style="display: block; margin: 5px 0;">haven-cli list-commits --base-branch main</code>
                </div>
            `;
            commitList.appendChild(emptyDiv);
        }} else {{
            commits.forEach(commit => {{
                const commitDiv = document.createElement('div');
                commitDiv.className = 'commit';
                commitDiv.innerHTML = `
                    <div class="commit-number">${{commit.number}}</div>
                    <div class="commit-details">
                        <a href="${{commit.file}}" class="commit-message" title="${{commit.message}}">${{commit.message}}</a>
                        <div class="commit-meta">
                            <span class="commit-hash">${{commit.hash}}</span>
                            by <strong>${{commit.author}}</strong>
                            on ${{commit.date}}
                        </div>
                    </div>
                `;
                commitList.appendChild(commitDiv);
            }});
        }}
    </script>
</body>
</html>"""

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write the file
    index_file = output_dir / "index.html"
    index_file.write_text(html_content)


@cli.command()
@click.option(
    "--repo-path",
    "-r",
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help="Path to git repository (default: current directory)",
)
@click.option(
    "--base-branch",
    "-b",
    default="main",
    help="Branch to show commits from (default: main)",
)
def list_commits(repo_path: Path, base_branch: str):
    """List all commits from the specified branch."""
    try:
        commits = asyncio.run(get_git_commits(repo_path, base_branch, max_commits=50))

        if not commits:
            console.print("[yellow]No commits found[/yellow]")
            return

        table = Table(title=f"Commits in {repo_path} (from {base_branch})")
        table.add_column("Number", style="cyan", width=8)
        table.add_column("Hash", style="yellow", width=10)
        table.add_column("Date", style="green", width=12)
        table.add_column("Author", style="blue", width=15)
        table.add_column("Message", style="black")

        for i, commit in enumerate(commits, 1):
            table.add_row(
                str(i),
                commit.hash[:8],
                commit.date,
                commit.author,
                commit.message[:60] + ("..." if len(commit.message) > 60 else ""),
            )

        console.print(table)
        console.print(f"\n[dim]Total: {len(commits)} commits[/dim]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
