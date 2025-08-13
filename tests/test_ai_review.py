#!/usr/bin/env python3
"""
Tests for AI Code Review Tool
"""

import pytest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the tool (adjust path as needed)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_code_review_tool import (
    CodeReviewEngine, 
    LLMReviewer, 
    Cache, 
    GitHubHelper,
    OutputFormatter,
    CONFIG,
    PERSPECTIVES
)


class TestCache:
    """Test the caching functionality"""
    
    def test_cache_initialization(self):
        """Test cache initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(temp_dir)
            assert cache.enabled == CONFIG["cache_enabled"]
            assert cache.cache_dir == Path(temp_dir)
    
    def test_cache_key_generation(self):
        """Test cache key generation"""
        cache = Cache()
        content = "test code content"
        perspective = "security"
        
        key1 = cache.get_key(content, perspective)
        key2 = cache.get_key(content, perspective)
        
        assert key1 == key2
        assert len(key1) == 64  # SHA256 hash length
    
    def test_cache_get_set(self):
        """Test cache get and set operations"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(temp_dir)
            content = "test code"
            perspective = "security"
            result = {"score": 85, "issues": []}
            
            # Initially no cache
            assert cache.get(content, perspective) is None
            
            # Set cache
            cache.set(content, perspective, result)
            
            # Get cached result
            cached = cache.get(content, perspective)
            assert cached == result


class TestGitHubHelper:
    """Test GitHub integration utilities"""
    
    @patch('subprocess.run')
    def test_get_changed_files(self, mock_run):
        """Test getting changed files"""
        mock_run.return_value.stdout = "file1.py\nfile2.js\n"
        mock_run.return_value.returncode = 0
        
        files = GitHubHelper.get_changed_files()
        assert files == ["file1.py", "file2.js"]
    
    def test_get_pr_context(self):
        """Test PR context extraction"""
        with patch.dict(os.environ, {
            'GITHUB_PR_NUMBER': '123',
            'GITHUB_REPOSITORY': 'test/repo',
            'GITHUB_SHA': 'abc123def456',
            'GITHUB_ACTOR': 'testuser',
            'GITHUB_WORKFLOW': 'CI'
        }):
            context = GitHubHelper.get_pr_context()
            assert context['pr_number'] == '123'
            assert context['repo'] == 'test/repo'
            assert context['sha'] == 'abc123d'
            assert context['actor'] == 'testuser'


class TestOutputFormatter:
    """Test output formatting"""
    
    def test_github_comment_formatting(self):
        """Test GitHub comment formatting"""
        report = {
            "success": True,
            "average_score": 85.5,
            "total_issues": 3,
            "high_severity_issues": 1,
            "file_count": 2,
            "perspective_count": 3,
            "issues": [
                {
                    "file": "test.py",
                    "line": 10,
                    "severity": "HIGH",
                    "message": "Security issue found",
                    "fix": "Use parameterized queries"
                }
            ],
            "summaries": [
                {
                    "perspective": "security",
                    "summary": "Good overall security"
                }
            ],
            "timestamp": "2024-01-01T12:00:00"
        }
        
        context = {"actor": "testuser"}
        comment = OutputFormatter.to_github_comment(report, context)
        
        assert "✅ AI Code Review Results" in comment
        assert "**Score:** 85.5/100" in comment
        assert "Security issue found" in comment
        assert "Use parameterized queries" in comment
    
    def test_json_formatting(self):
        """Test JSON output formatting"""
        report = {"success": True, "score": 85}
        json_output = OutputFormatter.to_json(report)
        
        parsed = json.loads(json_output)
        assert parsed["success"] is True
        assert parsed["score"] == 85
    
    def test_exit_code_calculation(self):
        """Test exit code calculation"""
        # Success case
        report = {"success": True, "average_score": 85}
        assert OutputFormatter.to_exit_code(report, 70) == 0
        
        # Below threshold
        assert OutputFormatter.to_exit_code(report, 90) == 1
        
        # Error case
        error_report = {"success": False}
        assert OutputFormatter.to_exit_code(error_report) == 2


class TestCodeReviewEngine:
    """Test the main review engine"""
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        with patch('ai_code_review_tool.LLMReviewer') as mock_reviewer:
            mock_reviewer.return_value = MagicMock()
            engine = CodeReviewEngine()
            
            assert hasattr(engine, 'reviewer')
            assert hasattr(engine, 'cache')
            assert hasattr(engine, 'github')
    
    def test_file_size_limit(self):
        """Test file size limiting"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Create a file larger than the limit
            large_content = "x" * (CONFIG["max_file_size_kb"] * 1024 + 1000)
            f.write(large_content)
            f.flush()
            
            with patch('ai_code_review_tool.LLMReviewer') as mock_reviewer:
                mock_reviewer.return_value = MagicMock()
                engine = CodeReviewEngine()
                
                # This should not raise an exception
                result = engine.review_file(f.name, "security")
                assert "error" not in result
                
            os.unlink(f.name)


class TestPerspectives:
    """Test review perspectives"""
    
    def test_perspective_structure(self):
        """Test that all perspectives have required fields"""
        for key, perspective in PERSPECTIVES.items():
            assert "name" in perspective
            assert "prompt" in perspective
            assert isinstance(perspective["name"], str)
            assert isinstance(perspective["prompt"], str)
            assert len(perspective["prompt"]) > 0
    
    def test_perspective_prompts_contain_json_format(self):
        """Test that perspective prompts include JSON formatting instructions"""
        for key, perspective in PERSPECTIVES.items():
            prompt = perspective["prompt"]
            assert "JSON" in prompt
            assert "issues" in prompt
            assert "severity" in prompt
            assert "message" in prompt


class TestConfiguration:
    """Test configuration settings"""
    
    def test_config_structure(self):
        """Test that configuration has all required fields"""
        required_fields = [
            "api_url", "model", "max_tokens", "temperature",
            "max_file_size_kb", "max_workers", "cache_enabled", "cache_dir"
        ]
        
        for field in required_fields:
            assert field in CONFIG
    
    def test_config_values(self):
        """Test configuration value types and ranges"""
        assert isinstance(CONFIG["max_tokens"], int)
        assert CONFIG["max_tokens"] > 0
        
        assert isinstance(CONFIG["temperature"], float)
        assert 0 <= CONFIG["temperature"] <= 1
        
        assert isinstance(CONFIG["max_file_size_kb"], int)
        assert CONFIG["max_file_size_kb"] > 0
        
        assert isinstance(CONFIG["max_workers"], int)
        assert CONFIG["max_workers"] > 0
        
        assert isinstance(CONFIG["cache_enabled"], bool)


if __name__ == "__main__":
    pytest.main([__file__])
