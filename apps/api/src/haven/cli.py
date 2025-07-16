#!/usr/bin/env python3
"""Haven CLI tool for git diff generation and analysis."""

import asyncio
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
    return stdout.decode(), stderr.decode(), process.returncode


async def get_git_commits(repo_path: Path, base_branch: str = "main") -> list[GitCommit]:
    """Get list of commits from git repository."""
    # Check if we're in a git repository
    stdout, stderr, returncode = await run_command(
        ["git", "rev-parse", "--git-dir"], cwd=repo_path
    )
    if returncode != 0:
        raise RuntimeError(f"Not a git repository: {repo_path}")

    # Get current branch
    stdout, stderr, returncode = await run_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path
    )
    if returncode != 0:
        raise RuntimeError(f"Failed to get current branch: {stderr}")

    current_branch = stdout.strip()

    # Get commits
    cmd = [
        "git",
        "log",
        "--reverse",
        "--pretty=format:%H|%s|%an|%ad",
        "--date=short",
        f"{base_branch}..{current_branch}",
    ]

    stdout, stderr, returncode = await run_command(cmd, cwd=repo_path)
    if returncode != 0:
        raise RuntimeError(f"Failed to get commits: {stderr}")

    commits = []
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
    """Generate diff file for a single commit."""
    # Get the diff
    cmd = ["git", "show", "--no-merges", commit.hash]
    stdout, stderr, returncode = await run_command(cmd, cwd=repo_path)

    if returncode != 0:
        console.print(f"[yellow]Warning: Could not get diff for {commit.hash[:8]}: {stderr}[/yellow]")
        return ""

    # Create filename
    safe_message = "".join(c for c in commit.message if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_message = safe_message.replace(" ", "-")[:50]
    filename = f"{commit_number:02d}-{commit.hash[:8]}-{safe_message}.diff"

    # Write diff file
    diff_file = output_dir / filename
    diff_file.write_text(stdout)

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
    help="Base branch for comparison (default: main)",
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
def generate(
    repo_path: Path,
    base_branch: str,
    output_dir: Path,
    verbose: bool,
):
    """Generate diff files for all commits in the repository."""
    if verbose:
        console.print(f"[blue]Repository:[/blue] {repo_path}")
        console.print(f"[blue]Base branch:[/blue] {base_branch}")
        console.print(f"[blue]Output directory:[/blue] {output_dir}")

    try:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)

        # Run the async diff generation
        asyncio.run(
            _generate_diffs_async(
                repo_path=repo_path,
                base_branch=base_branch,
                output_dir=output_dir,
                verbose=verbose,
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
):
    """Async helper for diff generation."""
    # Get commits
    if verbose:
        console.print("\n[yellow]📋 Getting commit list...[/yellow]")

    commits = await get_git_commits(repo_path, base_branch)

    if not commits:
        console.print("[yellow]⚠️ No commits found[/yellow]")
        return

    if verbose:
        console.print(f"[green]Found {len(commits)} commits[/green]")

    # Generate diffs
    if verbose:
        console.print("\n[yellow]🔄 Generating diffs...[/yellow]")

    generated_files = []
    for i, commit in enumerate(commits, 1):
        if verbose:
            console.print(f"[dim]Processing commit {i}/{len(commits)}: {commit.hash[:8]}[/dim]")

        filename = await generate_diff_for_commit(commit, output_dir, repo_path, i)
        if filename:
            generated_files.append(filename)

    # Generate summary
    if verbose:
        console.print(f"\n[green]Generated {len(generated_files)} diff files[/green]")

    # Create index file
    create_index_file(output_dir, commits, generated_files)


def create_index_file(output_dir: Path, commits: list[GitCommit], diff_files: list[str]):
    """Create an index.md file listing all commits and diffs."""
    index_content = ["# Git Diff Summary\n"]
    index_content.append(f"Generated {len(commits)} diff files:\n")

    for i, (commit, diff_file) in enumerate(zip(commits, diff_files), 1):
        index_content.append(f"## {i}. {commit.message}")
        index_content.append(f"- **Hash:** `{commit.hash}`")
        index_content.append(f"- **Author:** {commit.author}")
        index_content.append(f"- **Date:** {commit.date}")
        index_content.append(f"- **Diff file:** [{diff_file}](./{diff_file})")
        index_content.append("")

    index_file = output_dir / "index.md"
    index_file.write_text("\n".join(index_content))


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
    help="Base branch for comparison (default: main)",
)
def list_commits(repo_path: Path, base_branch: str):
    """List commits that would be included in diff generation."""
    try:
        commits = asyncio.run(get_git_commits(repo_path, base_branch))

        if not commits:
            console.print("[yellow]No commits found[/yellow]")
            return

        table = Table(title=f"Commits in {repo_path} (vs {base_branch})")
        table.add_column("Number", style="cyan", width=8)
        table.add_column("Hash", style="yellow", width=10)
        table.add_column("Date", style="green", width=12)
        table.add_column("Author", style="blue", width=15)
        table.add_column("Message", style="white")

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
