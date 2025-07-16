#!/usr/bin/env python3
"""Scan all documentation for consistency issues.

This script analyzes documentation files to find:
- Invalid file paths
- Broken commands
- Outdated code examples
- Dead internal links
- Inconsistent information
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class DocumentationScanner:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues = defaultdict(list)
        self.stats = defaultdict(int)
        
    def scan_all_docs(self) -> Dict:
        """Scan all documentation files."""
        doc_files = self._find_all_docs()
        
        for doc_file in doc_files:
            print(f"Scanning {doc_file}...")
            self.scan_document(doc_file)
            
        return {
            "issues": dict(self.issues),
            "stats": dict(self.stats),
            "summary": self._generate_summary()
        }
        
    def _find_all_docs(self) -> List[Path]:
        """Find all markdown documentation files."""
        doc_files = []
        
        # Root level docs
        for pattern in ["*.md", "*.MD"]:
            doc_files.extend(self.project_root.glob(pattern))
            
        # Docs directory
        docs_dir = self.project_root / "docs"
        if docs_dir.exists():
            doc_files.extend(docs_dir.rglob("*.md"))
            
        # App-specific docs
        for app_dir in ["apps/api", "apps/web"]:
            app_path = self.project_root / app_dir
            if app_path.exists():
                doc_files.extend(app_path.glob("*.md"))
                
        self.stats["total_files"] = len(doc_files)
        return sorted(doc_files)
        
    def scan_document(self, doc_path: Path):
        """Scan a single document for issues."""
        content = doc_path.read_text()
        relative_path = doc_path.relative_to(self.project_root)
        
        # Scan for various issues
        self._scan_file_paths(content, relative_path)
        self._scan_commands(content, relative_path)
        self._scan_code_blocks(content, relative_path)
        self._scan_internal_links(content, relative_path)
        self._scan_urls(content, relative_path)
        
    def _scan_file_paths(self, content: str, doc_path: Path):
        """Extract and validate file paths."""
        # Pattern for file paths
        path_patterns = [
            r'`([^`]+\.[a-zA-Z]+)`',  # Backtick paths with extensions
            r'"([^"]+\.[a-zA-Z]+)"',   # Quoted paths with extensions
            r'([a-zA-Z0-9_\-/]+/[a-zA-Z0-9_\-/.]+)',  # Unquoted paths
        ]
        
        checked_paths = set()
        
        for pattern in path_patterns:
            for match in re.finditer(pattern, content):
                path_str = match.group(1)
                
                # Skip URLs and obviously non-file paths
                if any(skip in path_str for skip in ['http://', 'https://', '{{', '}}', '::', '<', '>']):
                    continue
                    
                # Skip if already checked
                if path_str in checked_paths:
                    continue
                checked_paths.add(path_str)
                
                # Check if path exists
                full_path = self.project_root / path_str
                if not full_path.exists():
                    # Try relative to doc location
                    doc_dir = doc_path.parent
                    relative_path = doc_dir / path_str
                    
                    if not relative_path.exists() and not self._is_example_path(path_str):
                        self.issues[str(doc_path)].append({
                            "type": "invalid_path",
                            "path": path_str,
                            "line": self._get_line_number(content, match.start())
                        })
                        self.stats["invalid_paths"] += 1
                        
    def _scan_commands(self, content: str, doc_path: Path):
        """Extract and validate commands."""
        # Pattern for commands
        command_patterns = [
            r'```bash\n(.*?)\n```',  # Bash code blocks
            r'```sh\n(.*?)\n```',    # Shell code blocks
            r'`(just [^`]+)`',       # Just commands
            r'`(docker [^`]+)`',     # Docker commands
            r'`(npm [^`]+)`',        # NPM commands
            r'`(python [^`]+)`',     # Python commands
        ]
        
        for pattern in command_patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                commands = match.group(1).strip().split('\n')
                
                for command in commands:
                    command = command.strip()
                    if not command or command.startswith('#'):
                        continue
                        
                    # Extract just the command name
                    if command.startswith('just '):
                        self._validate_just_command(command, doc_path, match.start())
                        
    def _validate_just_command(self, command: str, doc_path: Path, position: int):
        """Validate a just command exists."""
        # Extract command parts
        parts = command.split()
        if len(parts) < 2:
            return
            
        just_cmd = parts[1]
        
        # Check if command exists using just --list
        try:
            result = subprocess.run(
                ["just", "--list"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Check if command is in the list
            if just_cmd not in result.stdout:
                self.issues[str(doc_path)].append({
                    "type": "invalid_command",
                    "command": command,
                    "line": self._get_line_number(doc_path.read_text(), position)
                })
                self.stats["invalid_commands"] += 1
                
        except Exception:
            # Just not available, skip validation
            pass
            
    def _scan_code_blocks(self, content: str, doc_path: Path):
        """Extract and validate code examples."""
        # Pattern for code blocks with language
        code_block_pattern = r'```(\w+)\n(.*?)\n```'
        
        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            language = match.group(1)
            code = match.group(2)
            
            if language == "python":
                self._validate_python_imports(code, doc_path, match.start())
                
    def _validate_python_imports(self, code: str, doc_path: Path, position: int):
        """Validate Python import statements."""
        import_pattern = r'^(?:from|import)\s+([a-zA-Z0-9_.]+)'
        
        for line in code.split('\n'):
            match = re.match(import_pattern, line.strip())
            if match:
                module = match.group(1).split('.')[0]
                
                # Check if it's a project module
                if module in ['haven', 'src']:
                    # Verify module exists
                    module_path = self.project_root / "apps" / "api" / "src" / module
                    if not module_path.exists():
                        self.issues[str(doc_path)].append({
                            "type": "invalid_import",
                            "import": line.strip(),
                            "line": self._get_line_number(doc_path.read_text(), position)
                        })
                        self.stats["invalid_imports"] += 1
                        
    def _scan_internal_links(self, content: str, doc_path: Path):
        """Extract and validate internal documentation links."""
        # Pattern for markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        for match in re.finditer(link_pattern, content):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # Skip external links
            if link_url.startswith(('http://', 'https://', '#')):
                continue
                
            # Check if linked file exists
            if link_url.endswith('.md'):
                doc_dir = doc_path.parent
                linked_path = (doc_dir / link_url).resolve()
                
                try:
                    relative_to_root = linked_path.relative_to(self.project_root)
                    if not linked_path.exists():
                        self.issues[str(doc_path)].append({
                            "type": "broken_link",
                            "link": link_url,
                            "text": link_text,
                            "line": self._get_line_number(content, match.start())
                        })
                        self.stats["broken_links"] += 1
                except ValueError:
                    # Path is outside project root
                    pass
                    
    def _scan_urls(self, content: str, doc_path: Path):
        """Scan for localhost URLs that should use domain names."""
        localhost_pattern = r'http://localhost:(\d+)'
        
        for match in re.finditer(localhost_pattern, content):
            port = match.group(1)
            
            self.issues[str(doc_path)].append({
                "type": "localhost_url",
                "url": match.group(0),
                "port": port,
                "line": self._get_line_number(content, match.start()),
                "suggestion": self._suggest_domain_replacement(port)
            })
            self.stats["localhost_urls"] += 1
            
    def _suggest_domain_replacement(self, port: str) -> str:
        """Suggest domain replacement for localhost URLs."""
        replacements = {
            "3000": "http://web.haven.local",
            "8080": "http://api.haven.local",
            "8001": "http://docs.haven.local"
        }
        return replacements.get(port, f"http://haven.local:{port}")
        
    def _is_example_path(self, path: str) -> bool:
        """Check if a path is an example/placeholder."""
        example_indicators = [
            'path/to/', 'your/', 'my-', '<', '>', 
            'example', 'placeholder', 'TODO', 'FIXME'
        ]
        return any(indicator in path for indicator in example_indicators)
        
    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number for a position in content."""
        return content[:position].count('\n') + 1
        
    def _generate_summary(self) -> Dict:
        """Generate summary statistics."""
        total_issues = sum(len(issues) for issues in self.issues.values())
        
        return {
            "total_files_scanned": self.stats["total_files"],
            "files_with_issues": len(self.issues),
            "total_issues": total_issues,
            "issues_by_type": {
                "invalid_paths": self.stats.get("invalid_paths", 0),
                "invalid_commands": self.stats.get("invalid_commands", 0),
                "invalid_imports": self.stats.get("invalid_imports", 0),
                "broken_links": self.stats.get("broken_links", 0),
                "localhost_urls": self.stats.get("localhost_urls", 0)
            }
        }


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scan documentation for consistency issues")
    parser.add_argument("--output", "-o", help="Output file for results (JSON)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    
    # Find project root
    project_root = Path(__file__).parent.parent
    
    # Run scanner
    scanner = DocumentationScanner(project_root)
    results = scanner.scan_all_docs()
    
    # Output results
    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:
        output = generate_markdown_report(results)
        
    if args.output:
        Path(args.output).write_text(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


def generate_markdown_report(results: Dict) -> str:
    """Generate a markdown report from scan results."""
    lines = []
    
    lines.append("# Documentation Audit Report")
    lines.append("")
    
    # Summary
    summary = results["summary"]
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Files Scanned**: {summary['total_files_scanned']}")
    lines.append(f"- **Files with Issues**: {summary['files_with_issues']}")
    lines.append(f"- **Total Issues**: {summary['total_issues']}")
    lines.append("")
    
    # Issues by type
    lines.append("### Issues by Type")
    lines.append("")
    for issue_type, count in summary["issues_by_type"].items():
        if count > 0:
            lines.append(f"- **{issue_type.replace('_', ' ').title()}**: {count}")
    lines.append("")
    
    # Detailed issues
    if results["issues"]:
        lines.append("## Detailed Issues")
        lines.append("")
        
        for doc_path, issues in sorted(results["issues"].items()):
            lines.append(f"### {doc_path}")
            lines.append("")
            
            for issue in issues:
                issue_type = issue["type"].replace("_", " ").title()
                line_num = issue.get("line", "?")
                
                if issue["type"] == "invalid_path":
                    lines.append(f"- **Line {line_num}**: {issue_type} - `{issue['path']}`")
                elif issue["type"] == "invalid_command":
                    lines.append(f"- **Line {line_num}**: {issue_type} - `{issue['command']}`")
                elif issue["type"] == "invalid_import":
                    lines.append(f"- **Line {line_num}**: {issue_type} - `{issue['import']}`")
                elif issue["type"] == "broken_link":
                    lines.append(f"- **Line {line_num}**: {issue_type} - [{issue['text']}]({issue['link']})")
                elif issue["type"] == "localhost_url":
                    lines.append(f"- **Line {line_num}**: {issue_type} - `{issue['url']}` → `{issue['suggestion']}`")
                    
            lines.append("")
    else:
        lines.append("## No Issues Found")
        lines.append("")
        lines.append("All documentation appears to be consistent! 🎉")
        
    return "\n".join(lines)


if __name__ == "__main__":
    main()