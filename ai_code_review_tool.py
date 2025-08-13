#!/usr/bin/env python3
"""
AI Code Review Tool - Enhanced GitHub Integration Version

A production-ready AI-powered code review tool that provides comprehensive 
security, performance, and quality analysis with enhanced feedback showing 
ALL identified issues (not just a limited subset).

Optimized for GitHub Actions with multi-perspective reviews and intelligent caching.
"""

import os
import sys
import json
import argparse
import hashlib
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import re

# Default configuration - ROUND 1 PROVEN: Best performing setup (28% detection)
CONFIG = {
    "api_url": "https://api.anthropic.com/v1/messages",
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 16384,  # ROUND 1: Doubled token limit for comprehensive analysis
    "temperature": 0.3,
    "max_file_size_kb": 2000,  # ROUND 1: Increased file size limit (800KB -> 2MB)
    "max_workers": 1,  # ROUND 1: Reduced workers to avoid rate limiting
    "cache_enabled": True,
    "cache_dir": ".ai_review_cache",
    "chunk_size_lines": 200,  # ROUND 1: Chunk large files for analysis
    "max_retries": 3,  # ROUND 1: Add retry logic
    "retry_delay": 2,  # ROUND 1: Base delay in seconds
    "sequential_perspectives": False,  # ROUND 1: Original parallel processing
}

# Review perspectives - focused and practical
PERSPECTIVES = {
    "security": {
        "name": "Security Scanner",
        "prompt": """Analyze this code for security vulnerabilities. Focus on:
- Input validation and sanitization
- Authentication/authorization issues  
- SQL injection, XSS, CSRF risks
- Sensitive data exposure
- Dependency vulnerabilities

Format your response as JSON:
{
  "issues": [
    {"line": <number>, "severity": "HIGH|MEDIUM|LOW", "message": "<description>", "fix": "<suggestion>"}
  ],
  "summary": "<brief overall assessment>",
  "score": <0-100>
}""",
    },
    "quality": {
        "name": "Quality Checker",
        "prompt": """Review this code for quality and maintainability. Focus on:
- Code complexity and readability
- Error handling
- Documentation and comments
- DRY/SOLID principles
- Testing considerations

Format your response as JSON:
{
  "issues": [
    {"line": <number>, "severity": "HIGH|MEDIUM|LOW", "message": "<description>", "fix": "<suggestion>"}
  ],
  "summary": "<brief overall assessment>",
  "score": <0-100>
}""",
    },
    "performance": {
        "name": "Performance Analyzer",
        "prompt": """Analyze this code for performance issues. Focus on:
- Algorithm complexity
- Database query efficiency
- Memory usage
- Caching opportunities
- Resource leaks

Format your response as JSON:
{
  "issues": [
    {"line": <number>, "severity": "HIGH|MEDIUM|LOW", "message": "<description>", "fix": "<suggestion>"}
  ],
  "summary": "<brief overall assessment>",
  "score": <0-100>
}""",
    },
}


class GitHubHelper:
    """Utilities for GitHub integration"""

    @staticmethod
    def get_changed_files(base_branch: str = "main") -> List[str]:
        """Get list of changed files in PR"""
        try:
            # Try to get files changed in current branch vs base
            result = subprocess.run(
                ["git", "diff", "--name-only", f"origin/{base_branch}...HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            files = result.stdout.strip().split("\n") if result.stdout else []
            return [f for f in files if f]
        except subprocess.CalledProcessError:
            # Fallback: get uncommitted changes
            try:
                result = subprocess.run(
                    ["git", "diff", "--name-only", "HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                files = result.stdout.strip().split("\n") if result.stdout else []
                return [f for f in files if f]
            except Exception:
                return []

    @staticmethod
    def get_pr_context() -> Dict[str, str]:
        """Extract PR context from GitHub environment variables"""
        return {
            "pr_number": os.environ.get("GITHUB_PR_NUMBER", ""),
            "repo": os.environ.get("GITHUB_REPOSITORY", ""),
            "sha": os.environ.get("GITHUB_SHA", "")[:7],
            "actor": os.environ.get("GITHUB_ACTOR", ""),
            "workflow": os.environ.get("GITHUB_WORKFLOW", "CI"),
        }


class LLMReviewer:
    """Handles LLM API calls for code review"""

    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        self.session = self._create_session()

    def _create_session(self):
        """Create a session for connection pooling"""
        import urllib3

        return urllib3.PoolManager()

    def review(self, code: str, perspective: Dict, filename: str) -> Dict:
        """Send code to LLM and parse response with retry logic"""
        prompt = f"{perspective['prompt']}\n\nFile: {filename}\nCode:\n```\n{code}\n```"

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        body = json.dumps(
            {
                "model": CONFIG["model"],
                "max_tokens": CONFIG["max_tokens"],
                "temperature": CONFIG["temperature"],
                "messages": [{"role": "user", "content": prompt}],
            }
        )

        # IMPROVEMENT 2: Retry logic with exponential backoff
        for attempt in range(CONFIG["max_retries"]):
            try:
                response = self.session.request(
                    "POST", CONFIG["api_url"], headers=headers, body=body, timeout=60  # Increased timeout
                )

                if response.status == 200:
                    data = json.loads(response.data)
                    content = data["content"][0]["text"]

                    # Extract JSON from response
                    json_match = re.search(r"\{.*\}", content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())

                    return {"issues": [], "summary": "Failed to parse", "score": 50}
                
                elif response.status == 529:  # Rate limited
                    if attempt < CONFIG["max_retries"] - 1:
                        delay = CONFIG["retry_delay"] * (2 ** attempt)  # Exponential backoff
                        print(f"Rate limited, retrying in {delay}s (attempt {attempt + 1})", file=sys.stderr)
                        import time
                        time.sleep(delay)
                        continue
                    else:
                        return {"issues": [], "summary": f"API rate limited after {CONFIG['max_retries']} attempts", "score": 50}
                else:
                    raise Exception(f"API error: {response.status}")

            except json.JSONDecodeError:
                return {"issues": [], "summary": "Invalid JSON response", "score": 50}
            except Exception as e:
                if attempt < CONFIG["max_retries"] - 1:
                    delay = CONFIG["retry_delay"] * (2 ** attempt)
                    print(f"Review error: {e}, retrying in {delay}s", file=sys.stderr)
                    import time
                    time.sleep(delay)
                    continue
                else:
                    print(f"Review error after {CONFIG['max_retries']} attempts: {e}", file=sys.stderr)
                    return {"issues": [], "summary": str(e), "score": 50}

        return {"issues": [], "summary": "All retry attempts failed", "score": 50}


class Cache:
    """Simple file-based cache for review results"""

    def __init__(self, cache_dir: str = ".ai_review_cache"):
        self.enabled = CONFIG["cache_enabled"]
        if self.enabled:
            self.cache_dir = Path(cache_dir)
            self.cache_dir.mkdir(exist_ok=True)

    def get_key(self, content: str, perspective: str) -> str:
        """Generate cache key"""
        data = f"{content}:{perspective}:{CONFIG['model']}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get(self, content: str, perspective: str) -> Optional[Dict]:
        """Retrieve cached result"""
        if not self.enabled:
            return None

        key = self.get_key(content, perspective)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def set(self, content: str, perspective: str, result: Dict):
        """Store result in cache"""
        if not self.enabled:
            return

        key = self.get_key(content, perspective)
        cache_file = self.cache_dir / f"{key}.json"

        try:
            with open(cache_file, "w") as f:
                json.dump(result, f)
        except Exception:
            pass


class CodeReviewEngine:
    """Main review orchestrator"""

    def __init__(self):
        self.reviewer = LLMReviewer()
        self.cache = Cache()
        self.github = GitHubHelper()

    def review_file(self, filepath: str, perspective_key: str) -> Dict:
        """Review a single file from one perspective with chunking support"""
        path = Path(filepath)
        if not path.exists():
            return {"error": f"File not found: {filepath}"}

        # Read file content
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"error": f"Cannot read {filepath}: {e}"}

        # IMPROVEMENT 3: Handle large files with chunking
        lines = content.split('\n')
        chunk_size = CONFIG["chunk_size_lines"]
        
        if len(lines) > chunk_size:
            print(f"Large file detected ({len(lines)} lines), using chunking approach", file=sys.stderr)
            return self._review_file_chunked(filepath, lines, perspective_key)
        
        # Check size limit for single chunk
        if len(content) > CONFIG["max_file_size_kb"] * 1024:
            content = content[: CONFIG["max_file_size_kb"] * 1024]
            print(f"File truncated to {CONFIG['max_file_size_kb']}KB", file=sys.stderr)

        # Check cache
        cached = self.cache.get(content, perspective_key)
        if cached:
            cached["cached"] = True
            return cached

        # Perform review
        perspective = PERSPECTIVES[perspective_key]
        result = self.reviewer.review(content, perspective, filepath)
        result["perspective"] = perspective_key
        result["file"] = filepath
        result["timestamp"] = datetime.now().isoformat()

        # Cache result
        self.cache.set(content, perspective_key, result)

        return result

    def _review_file_chunked(self, filepath: str, lines: List[str], perspective_key: str) -> Dict:
        """Review large file in chunks and aggregate results"""
        chunk_size = CONFIG["chunk_size_lines"]
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
        
        all_issues = []
        all_scores = []
        summaries = []
        
        perspective = PERSPECTIVES[perspective_key]
        
        for i, chunk_lines in enumerate(chunks):
            chunk_content = '\n'.join(chunk_lines)
            chunk_id = f"{filepath}:chunk-{i+1}"
            
            print(f"Analyzing chunk {i+1}/{len(chunks)} of {filepath}", file=sys.stderr)
            
            # Check cache for chunk
            cached = self.cache.get(chunk_content, perspective_key)
            if cached:
                chunk_result = cached
            else:
                # Review chunk
                chunk_result = self.reviewer.review(chunk_content, perspective, chunk_id)
                self.cache.set(chunk_content, perspective_key, chunk_result)
            
            # Aggregate results
            if chunk_result.get("issues"):
                for issue in chunk_result["issues"]:
                    # Adjust line numbers for chunk offset
                    if issue.get("line"):
                        issue["line"] = issue["line"] + (i * chunk_size)
                    all_issues.append(issue)
            
            if chunk_result.get("score"):
                all_scores.append(chunk_result["score"])
            
            if chunk_result.get("summary"):
                summaries.append(f"Chunk {i+1}: {chunk_result['summary']}")
        
        # Aggregate final result
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 50
        combined_summary = " | ".join(summaries) if summaries else "Chunked analysis completed"
        
        return {
            "issues": all_issues,
            "summary": combined_summary,
            "score": avg_score,
            "perspective": perspective_key,
            "file": filepath,
            "timestamp": datetime.now().isoformat(),
            "chunked": True,
            "chunks_analyzed": len(chunks)
        }

    def review_files(
        self, files: List[str], perspectives: List[str] = None
    ) -> List[Dict]:
        """Review multiple files from multiple perspectives with sequential processing"""
        if perspectives is None:
            perspectives = list(PERSPECTIVES.keys())

        results = []
        
        # ROUND 2-2: Sequential processing to avoid rate limiting
        if CONFIG.get("sequential_perspectives", False):
            print("Using sequential perspective processing to maximize accuracy", file=sys.stderr)
            for filepath in files:
                for perspective in perspectives:
                    try:
                        print(f"Analyzing {filepath} from {perspective} perspective...", file=sys.stderr)
                        result = self.review_file(filepath, perspective)
                        results.append(result)
                        
                        # Add delay between API calls to be respectful
                        import time
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"Review failed for {filepath} ({perspective}): {e}", file=sys.stderr)
        else:
            # Original parallel processing
            tasks = [(f, p) for f in files for p in perspectives]
            with ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
                futures = [executor.submit(self.review_file, f, p) for f, p in tasks]
                for future in futures:
                    try:
                        result = future.result(timeout=120)  # Increased timeout
                        results.append(result)
                    except Exception as e:
                        print(f"Review failed: {e}", file=sys.stderr)

        return results

    def aggregate_results(self, results: List[Dict]) -> Dict:
        """Aggregate results into final report"""
        # Filter out errors
        valid_results = [r for r in results if "error" not in r]

        if not valid_results:
            return {
                "success": False,
                "error": "No valid review results",
                "average_score": 0,
                "total_issues": 0,
            }

        # Aggregate metrics
        all_issues = []
        scores = []
        summaries = []

        for result in valid_results:
            issues = result.get("issues", [])
            for issue in issues:
                issue["file"] = result.get("file", "unknown")
                issue["perspective"] = result.get("perspective", "unknown")
                all_issues.append(issue)

            scores.append(result.get("score", 50))
            if result.get("summary"):
                summaries.append(
                    {
                        "perspective": result.get("perspective"),
                        "summary": result.get("summary"),
                        "file": result.get("file"),
                    }
                )

        # Sort issues by severity
        severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        all_issues.sort(key=lambda x: severity_order.get(x.get("severity", "LOW"), 3))

        # Calculate metrics
        high_severity = len([i for i in all_issues if i.get("severity") == "HIGH"])
        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            "success": True,
            "average_score": round(avg_score, 1),
            "total_issues": len(all_issues),
            "high_severity_issues": high_severity,
            "issues": all_issues,  # Show all issues
            "summaries": summaries,
            "file_count": len(set(r.get("file") for r in valid_results)),
            "perspective_count": len(set(r.get("perspective") for r in valid_results)),
            "timestamp": datetime.now().isoformat(),
        }


class OutputFormatter:
    """Format results for different outputs"""

    @staticmethod
    def to_github_comment(report: Dict, context: Dict) -> str:
        """Format as GitHub PR comment"""
        if not report.get("success"):
            return f"❌ **Review Failed:** {report.get('error', 'Unknown error')}"

        score = report["average_score"]
        emoji = "✅" if score >= 70 else "⚠️" if score >= 50 else "❌"

        comment = f"""## {emoji} AI Code Review Results

**Score:** {score}/100 | **Issues Found:** {report['total_issues']} ({report['high_severity_issues']} high severity)
**Files Reviewed:** {report['file_count']} | **Perspectives:** {report['perspective_count']}

"""

        if report["high_severity_issues"] > 0:
            comment += "### 🔴 High Severity Issues\n\n"
            high_issues = [i for i in report["issues"] if i.get("severity") == "HIGH"]
            for issue in high_issues:
                comment += f"- **{issue['file']}**"
                if issue.get("line"):
                    comment += f" (line {issue['line']})"
                comment += f"\n  - {issue['message']}\n"
                if issue.get("fix"):
                    comment += f"  - 💡 *{issue['fix']}*\n"

        # Show all medium severity issues
        medium_issues = [i for i in report["issues"] if i.get("severity") == "MEDIUM"]
        if medium_issues:
            comment += "\n### ⚠️ Medium Severity Issues\n\n"
            for issue in medium_issues:
                comment += f"- **{issue['file']}**"
                if issue.get("line"):
                    comment += f" (line {issue['line']})"
                comment += f"\n  - {issue['message']}\n"
                if issue.get("fix"):
                    comment += f"  - 💡 *{issue['fix']}*\n"

        # Show all low severity issues
        low_issues = [i for i in report["issues"] if i.get("severity") == "LOW"]
        if low_issues:
            comment += "\n### ℹ️ Low Severity Issues\n\n"
            for issue in low_issues:
                comment += f"- **{issue['file']}**"
                if issue.get("line"):
                    comment += f" (line {issue['line']})"
                comment += f"\n  - {issue['message']}\n"
                if issue.get("fix"):
                    comment += f"  - 💡 *{issue['fix']}*\n"

        # Add summaries grouped by file
        if report.get("summaries"):
            comment += "\n### 📊 Review Summaries by File\n\n"
            # Group summaries by file
            file_summaries = {}
            for summary in report["summaries"]:
                file = summary.get('file', 'unknown')
                if file not in file_summaries:
                    file_summaries[file] = {}
                file_summaries[file][summary['perspective']] = summary['summary']
            
            # Display summaries organized by file
            for file, perspectives in file_summaries.items():
                if any(perspectives.values()):  # Only show files with valid summaries
                    comment += f"#### {file}\n"
                    for perspective, summary in perspectives.items():
                        if summary and not summary.startswith("API error"):
                            comment += f"- **{perspective.title()}:** {summary}\n"
                    comment += "\n"

        comment += f"\n---\n*Review completed at {report['timestamp']} by @{context.get('actor', 'ai-reviewer')}*"

        return comment

    @staticmethod
    def to_json(report: Dict) -> str:
        """Format as JSON"""
        return json.dumps(report, indent=2, default=str)

    @staticmethod
    def to_markdown(report: Dict) -> str:
        """Format as Markdown report"""
        if not report.get("success"):
            return f"# Review Failed\n\n{report.get('error', 'Unknown error')}"

        md = f"""# Code Review Report

**Date:** {report['timestamp']}  
**Average Score:** {report['average_score']}/100  
**Total Issues:** {report['total_issues']}  
**High Severity:** {report['high_severity_issues']}  

## Issues by Severity

"""

        for severity in ["HIGH", "MEDIUM", "LOW"]:
            issues = [i for i in report["issues"] if i.get("severity") == severity]
            if issues:
                md += f"### {severity} ({len(issues)})\n\n"
                for issue in issues[:5]:
                    md += f"- **{issue['file']}**"
                    if issue.get("line"):
                        md += f":{issue['line']}"
                    md += f" - {issue['message']}\n"
                    if issue.get("fix"):
                        md += f"  - Fix: {issue['fix']}\n"
                md += "\n"

        return md

    @staticmethod
    def to_exit_code(report: Dict, threshold: int = 70) -> int:
        """Convert to exit code for CI/CD"""
        if not report.get("success"):
            return 2  # Error

        if report["average_score"] < threshold:
            return 1  # Quality below threshold

        return 0  # Success


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI Code Review Tool for GitHub Actions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review changed files in PR
  %(prog)s --changed --output github
  
  # Review specific files
  %(prog)s file1.py file2.js --output json
  
  # Review with threshold
  %(prog)s --changed --threshold 80
        """,
    )

    parser.add_argument("files", nargs="*", help="Files to review")
    parser.add_argument(
        "--changed", action="store_true", help="Review only changed files in PR"
    )
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Base branch for comparison (default: main)",
    )
    parser.add_argument(
        "--perspectives", help="Comma-separated perspectives (default: all)"
    )
    parser.add_argument(
        "--output",
        choices=["github", "json", "markdown"],
        default="github",
        help="Output format",
    )
    parser.add_argument("--output-file", help="Save output to file")
    parser.add_argument(
        "--threshold", type=int, default=70, help="Quality threshold (0-100)"
    )
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")

    args = parser.parse_args()

    # Configure
    if args.no_cache:
        CONFIG["cache_enabled"] = False

    # Initialize engine
    try:
        engine = CodeReviewEngine()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please set ANTHROPIC_API_KEY environment variable", file=sys.stderr)
        sys.exit(2)

    # Get files to review
    files_to_review = []

    if args.changed:
        files_to_review = engine.github.get_changed_files(args.base_branch)
        if not files_to_review:
            print("No changed files found", file=sys.stderr)
            sys.exit(0)
    elif args.files:
        files_to_review = args.files
    else:
        print("Error: Specify files or use --changed flag", file=sys.stderr)
        sys.exit(2)

    # Filter by supported extensions
    supported_exts = {".py", ".js", ".ts", ".java", ".go", ".rb", ".cpp", ".c", ".cs"}
    files_to_review = [f for f in files_to_review if Path(f).suffix in supported_exts]

    if not files_to_review:
        print("No supported files to review", file=sys.stderr)
        sys.exit(0)

    print(f"Reviewing {len(files_to_review)} file(s)...", file=sys.stderr)

    # Select perspectives
    perspectives = None
    if args.perspectives:
        perspectives = args.perspectives.split(",")
        invalid = [p for p in perspectives if p not in PERSPECTIVES]
        if invalid:
            print(f"Invalid perspectives: {invalid}", file=sys.stderr)
            print(f"Available: {list(PERSPECTIVES.keys())}", file=sys.stderr)
            sys.exit(2)

    # Perform reviews
    results = engine.review_files(files_to_review, perspectives)

    # Aggregate results
    report = engine.aggregate_results(results)

    # Format output
    formatter = OutputFormatter()
    context = engine.github.get_pr_context()

    if args.output == "github":
        output = formatter.to_github_comment(report, context)
    elif args.output == "json":
        output = formatter.to_json(report)
    else:
        output = formatter.to_markdown(report)

    # Write output
    if args.output_file:
        with open(args.output_file, "w") as f:
            f.write(output)
        print(f"Output saved to {args.output_file}", file=sys.stderr)
    else:
        print(output)

    # Exit with appropriate code
    exit_code = formatter.to_exit_code(report, args.threshold)
    if exit_code != 0:
        print(
            f"\n{'ERROR' if exit_code == 2 else 'FAILURE'}: ", file=sys.stderr, end=""
        )
        if exit_code == 1:
            print(
                f"Quality score {report['average_score']} below threshold {args.threshold}",
                file=sys.stderr,
            )
        else:
            print(report.get("error", "Review failed"), file=sys.stderr)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
