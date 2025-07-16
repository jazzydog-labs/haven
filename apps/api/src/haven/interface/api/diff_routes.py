"""API routes for git diff generation."""

import asyncio
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

router = APIRouter(tags=["Diffs"])


class DiffRequest(BaseModel):
    """Request model for diff generation."""

    branch: str = "HEAD"
    base_branch: str = "main"
    max_commits: int = 50


class CommitInfo(BaseModel):
    """Information about a single commit."""

    number: int
    hash: str
    message: str
    author: str
    date: str
    filename: str


class DiffGenerationStatus(BaseModel):
    """Status of diff generation task."""

    task_id: str
    status: str  # "pending", "processing", "completed", "failed"
    message: str | None = None
    output_dir: str | None = None
    commit_count: int | None = None


# Store for background tasks status
diff_tasks = {}


async def run_command(cmd: list[str]) -> tuple[str, str, int]:
    """Run a shell command asynchronously."""
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode(), process.returncode


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Sanitize text for use in filenames."""
    import re

    sanitized = re.sub(r"[^a-zA-Z0-9]", "-", text)
    return sanitized[:max_length]


async def check_diff2html():
    """Check if diff2html is installed."""
    stdout, _, returncode = await run_command(["which", "diff2html"])
    if returncode != 0:
        # Try to install it
        stdout, stderr, returncode = await run_command(["npm", "install", "-g", "diff2html-cli"])
        if returncode != 0:
            raise RuntimeError(f"Failed to install diff2html: {stderr}")


async def generate_diffs_task(task_id: str, branch: str, base_branch: str, max_commits: int):
    """Background task to generate diffs."""
    try:
        diff_tasks[task_id]["status"] = "processing"

        # Create output directory
        output_dir = Path(f"diff-out-{task_id}")
        output_dir.mkdir(exist_ok=True)
        diff_tasks[task_id]["output_dir"] = str(output_dir)

        # Check diff2html
        await check_diff2html()

        # Get list of commits
        cmd = [
            "git",
            "rev-list",
            "--reverse",
            f"--max-count={max_commits}",
            f"{base_branch}..{branch}",
        ]
        stdout, stderr, returncode = await run_command(cmd)
        if returncode != 0:
            raise RuntimeError(f"Failed to get commits: {stderr}")

        commits = stdout.strip().split("\n") if stdout.strip() else []
        if not commits:
            diff_tasks[task_id]["status"] = "completed"
            diff_tasks[task_id]["message"] = "No commits to diff"
            diff_tasks[task_id]["commit_count"] = 0
            return

        # Arrays to store commit info
        commit_infos = []

        # Generate diff for each commit
        for i, commit in enumerate(commits, 1):
            # Get commit info
            hash_cmd = ["git", "rev-parse", "--short", commit]
            hash_stdout, _, _ = await run_command(hash_cmd)
            commit_hash = hash_stdout.strip()

            msg_cmd = ["git", "log", "-1", "--pretty=format:%s", commit]
            msg_stdout, _, _ = await run_command(msg_cmd)
            message = msg_stdout.strip()

            author_cmd = ["git", "log", "-1", "--pretty=format:%an", commit]
            author_stdout, _, _ = await run_command(author_cmd)
            author = author_stdout.strip()

            date_cmd = ["git", "log", "-1", "--pretty=format:%ad", "--date=short", commit]
            date_stdout, _, _ = await run_command(date_cmd)
            date = date_stdout.strip()

            # Generate filename
            filename = f"{i}-{commit_hash}-{sanitize_filename(message)}.html"

            commit_infos.append(
                CommitInfo(
                    number=i,
                    hash=commit_hash,
                    message=message,
                    author=author,
                    date=date,
                    filename=filename,
                )
            )

            # Generate diff HTML
            diff_cmd = [
                "diff2html",
                "-s",
                "side",
                "-f",
                "html",
                "-F",
                str(output_dir / filename),
                "-t",
                f"{commit_hash}: {message}",
                "--summary",
                "open",
                "--highlightCode",
                "--",
                f"{commit}^..{commit}",
            ]

            _, stderr, returncode = await run_command(diff_cmd)
            if returncode != 0:
                print(f"Warning: Could not generate diff for {commit_hash}: {stderr}")

        # Generate index.html
        await generate_index_html(output_dir, commit_infos, branch, base_branch)

        diff_tasks[task_id]["status"] = "completed"
        diff_tasks[task_id]["commit_count"] = len(commit_infos)
        diff_tasks[task_id]["message"] = f"Generated {len(commit_infos)} diff files"

    except Exception as e:
        diff_tasks[task_id]["status"] = "failed"
        diff_tasks[task_id]["message"] = str(e)


async def generate_index_html(
    output_dir: Path, commits: list[CommitInfo], branch: str, base_branch: str
):
    """Generate the index.html file."""
    # Get current branch name if HEAD
    if branch == "HEAD":
        stdout, _, _ = await run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        branch_display = stdout.strip()
    else:
        branch_display = branch

    # Calculate stats
    unique_authors = len({c.author for c in commits})
    date_range = f"{commits[0].date} - {commits[-1].date}" if commits else "No commits"

    # Generate JavaScript array
    commit_data_lines = []
    for commit in commits:
        escaped_message = commit.message.replace('"', '\\"')
        commit_data_lines.append(
            f"{{number: {commit.number}, hash: '{commit.hash}', "
            f"message: \"{escaped_message}\", author: '{commit.author}', "
            f"date: '{commit.date}', file: '{commit.filename}'}}"
        )
    commit_data = ",\n            ".join(commit_data_lines)

    # HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commit Diff Index</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
            font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
            background-color: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 12px;
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

        .branch-info {{
            background-color: #f3f4f6;
            padding: 8px 12px;
            border-radius: 4px;
            display: inline-block;
            font-family: monospace;
            font-size: 14px;
        }}

        @media (max-width: 768px) {{
            .commit {{
                flex-direction: column;
                align-items: flex-start;
            }}

            .commit-number {{
                margin-bottom: 10px;
            }}

            .stats {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <h1>Commit Diff Index</h1>

    <div class="info">
        <strong>Branch:</strong> <span class="branch-info">{branch_display}</span> → <span class="branch-info">{base_branch}</span><br>
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
    </script>
</body>
</html>"""

    # Write the file
    with open(output_dir / "index.html", "w") as f:
        f.write(html_content)


@router.post("/diffs/generate", response_model=DiffGenerationStatus)
async def generate_diffs(
    request: DiffRequest, background_tasks: BackgroundTasks
) -> DiffGenerationStatus:
    """Generate diff files for commits in a branch."""
    task_id = str(uuid4())

    # Initialize task status
    diff_tasks[task_id] = {
        "status": "pending",
        "message": "Task queued",
        "output_dir": None,
        "commit_count": None,
    }

    # Queue the background task
    background_tasks.add_task(
        generate_diffs_task, task_id, request.branch, request.base_branch, request.max_commits
    )

    return DiffGenerationStatus(
        task_id=task_id, status="pending", message="Diff generation started"
    )


@router.get("/diffs/status/{task_id}", response_model=DiffGenerationStatus)
async def get_diff_status(task_id: str) -> DiffGenerationStatus:
    """Get the status of a diff generation task."""
    if task_id not in diff_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = diff_tasks[task_id]
    return DiffGenerationStatus(
        task_id=task_id,
        status=task["status"],
        message=task["message"],
        output_dir=task["output_dir"],
        commit_count=task["commit_count"],
    )


@router.get("/diffs/{task_id}/index.html", response_class=HTMLResponse)
async def get_diff_index(task_id: str):
    """Get the generated index.html file."""
    if task_id not in diff_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = diff_tasks[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Task is {task['status']}")

    output_dir = Path(task["output_dir"])
    index_file = output_dir / "index.html"

    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Index file not found")

    return FileResponse(index_file, media_type="text/html")


@router.get("/diffs/{task_id}/files/{filename}", response_class=HTMLResponse)
async def get_diff_file(task_id: str, filename: str):
    """Get a specific diff HTML file."""
    if task_id not in diff_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = diff_tasks[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Task is {task['status']}")

    output_dir = Path(task["output_dir"])
    diff_file = output_dir / filename

    if not diff_file.exists() or not diff_file.is_file():
        raise HTTPException(status_code=404, detail="Diff file not found")

    return FileResponse(diff_file, media_type="text/html")


@router.delete("/diffs/{task_id}")
async def cleanup_diff_task(task_id: str):
    """Clean up generated diff files and task data."""
    if task_id not in diff_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = diff_tasks[task_id]

    # Clean up files if they exist
    if task["output_dir"]:
        output_dir = Path(task["output_dir"])
        if output_dir.exists():
            import shutil

            shutil.rmtree(output_dir)

    # Remove from tasks
    del diff_tasks[task_id]

    return {"message": "Task cleaned up successfully"}
