---
source: https://github.com/modelcontextprotocol/python-sdk
fetched: 2025-08-20
version: latest
---

# MCP Practical Examples

## Table of Contents
- [Quick Start Examples](#quick-start-examples)
- [File System Server](#file-system-server)
- [Database Integration](#database-integration)
- [API Integration Server](#api-integration-server)
- [Development Tools Server](#development-tools-server)
- [Data Processing Server](#data-processing-server)
- [Client Examples](#client-examples)
- [Testing Examples](#testing-examples)
- [Production Deployment](#production-deployment)

## Quick Start Examples

### Simple Calculator Server
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@mcp.resource("calculator://history")
def calculation_history() -> list:
    """Get calculation history."""
    # In a real implementation, you'd track actual history
    return [
        {"operation": "add", "a": 5, "b": 3, "result": 8},
        {"operation": "multiply", "a": 4, "b": 7, "result": 28}
    ]

if __name__ == "__main__":
    mcp.run()
```

### Weather Information Server
```python
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

async def fetch_weather_data(city: str, api_key: str) -> Dict[str, Any]:
    """Fetch weather data from external API."""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise ValueError(f"Weather API error: {response.status}")

@mcp.tool()
async def get_current_weather(city: str) -> Dict[str, Any]:
    """Get current weather for a city."""
    api_key = "your_api_key_here"  # In production, use environment variable
    
    try:
        data = await fetch_weather_data(city, api_key)
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        return {"error": f"Failed to get weather for {city}: {e}"}

@mcp.resource("weather://{city}")
def weather_resource(city: str) -> str:
    """Get weather information as a resource."""
    return f"Weather data for {city} (use get_current_weather tool for live data)"

if __name__ == "__main__":
    mcp.run()
```

## File System Server

### Comprehensive File Management Server
```python
import os
import json
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FileSystem")

# Security: Define allowed directories
ALLOWED_DIRECTORIES = [
    str(Path.home()),
    "/tmp",
    os.getcwd()
]

def is_path_allowed(path: str) -> bool:
    """Check if path is within allowed directories."""
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(allowed) for allowed in ALLOWED_DIRECTORIES)

@mcp.tool()
def list_directory(path: str, show_hidden: bool = False) -> List[Dict[str, Any]]:
    """List directory contents with metadata."""
    if not is_path_allowed(path):
        raise ValueError(f"Access denied to path: {path}")
    
    dir_path = Path(path)
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {path}")
    
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    
    items = []
    for item in dir_path.iterdir():
        if not show_hidden and item.name.startswith('.'):
            continue
        
        stat = item.stat()
        items.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:],
            "mime_type": mimetypes.guess_type(str(item))[0] if item.is_file() else None
        })
    
    return sorted(items, key=lambda x: (x["type"], x["name"]))

@mcp.tool()
def create_directory(path: str) -> str:
    """Create a new directory."""
    if not is_path_allowed(path):
        raise ValueError(f"Access denied to path: {path}")
    
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"Directory created: {path}"
    except Exception as e:
        raise ValueError(f"Failed to create directory: {e}")

@mcp.tool()
def write_file(path: str, content: str, encoding: str = "utf-8") -> str:
    """Write content to a file."""
    if not is_path_allowed(path):
        raise ValueError(f"Access denied to path: {path}")
    
    try:
        Path(path).write_text(content, encoding=encoding)
        return f"File written: {path}"
    except Exception as e:
        raise ValueError(f"Failed to write file: {e}")

@mcp.tool()
def delete_file(path: str) -> str:
    """Delete a file."""
    if not is_path_allowed(path):
        raise ValueError(f"Access denied to path: {path}")
    
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"File does not exist: {path}")
    
    if file_path.is_dir():
        raise ValueError(f"Path is a directory, use delete_directory instead: {path}")
    
    try:
        file_path.unlink()
        return f"File deleted: {path}"
    except Exception as e:
        raise ValueError(f"Failed to delete file: {e}")

@mcp.resource("file://{path}")
def read_file_content(path: str) -> str:
    """Read file content as a resource."""
    if not is_path_allowed(path):
        raise ValueError(f"Access denied to path: {path}")
    
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"File does not exist: {path}")
    
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding='latin-1')
        except Exception as e:
            raise ValueError(f"Cannot read file as text: {e}")

@mcp.resource("directory://{path}")
def directory_summary(path: str) -> Dict[str, Any]:
    """Get directory summary as a resource."""
    if not is_path_allowed(path):
        raise ValueError(f"Access denied to path: {path}")
    
    dir_path = Path(path)
    if not dir_path.exists() or not dir_path.is_dir():
        raise ValueError(f"Invalid directory path: {path}")
    
    files = sum(1 for x in dir_path.iterdir() if x.is_file())
    dirs = sum(1 for x in dir_path.iterdir() if x.is_dir())
    total_size = sum(x.stat().st_size for x in dir_path.rglob('*') if x.is_file())
    
    return {
        "path": str(dir_path.absolute()),
        "files": files,
        "directories": dirs,
        "total_size": total_size,
        "size_human": format_bytes(total_size)
    }

def format_bytes(bytes_value: int) -> str:
    """Format bytes into human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f}{unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f}PB"

if __name__ == "__main__":
    mcp.run()
```

## Database Integration

### SQLite Database Server
```python
import sqlite3
import json
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Database")

DATABASE_PATH = "example.db"

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Initialize database with sample tables."""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()

@mcp.tool()
def execute_query(sql: str, params: Optional[List] = None) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return results."""
    if not sql.strip().upper().startswith('SELECT'):
        raise ValueError("Only SELECT queries are allowed")
    
    with get_db_connection() as conn:
        cursor = conn.execute(sql, params or [])
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        return [dict(zip(columns, row)) for row in rows]

@mcp.tool()
def create_user(name: str, email: str) -> Dict[str, Any]:
    """Create a new user."""
    with get_db_connection() as conn:
        try:
            cursor = conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()
            
            return {
                "success": True,
                "user_id": cursor.lastrowid,
                "message": f"User {name} created successfully"
            }
        except sqlite3.IntegrityError as e:
            return {
                "success": False,
                "error": f"User creation failed: {e}"
            }

@mcp.tool()
def create_post(user_id: int, title: str, content: str) -> Dict[str, Any]:
    """Create a new post."""
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
            (user_id, title, content)
        )
        conn.commit()
        
        return {
            "success": True,
            "post_id": cursor.lastrowid,
            "message": "Post created successfully"
        }

@mcp.resource("users://all")
def get_all_users() -> List[Dict[str, Any]]:
    """Get all users as a resource."""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM users ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

@mcp.resource("user://{user_id}/posts")
def get_user_posts(user_id: str) -> List[Dict[str, Any]]:
    """Get posts by user as a resource."""
    with get_db_connection() as conn:
        cursor = conn.execute(
            """
            SELECT p.*, u.name as author_name 
            FROM posts p 
            JOIN users u ON p.user_id = u.id 
            WHERE p.user_id = ? 
            ORDER BY p.created_at DESC
            """,
            (int(user_id),)
        )
        return [dict(row) for row in cursor.fetchall()]

# Initialize database on startup
init_database()

if __name__ == "__main__":
    mcp.run()
```

## API Integration Server

### GitHub API Integration
```python
import asyncio
import aiohttp
import os
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHub")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

async def github_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make authenticated request to GitHub API."""
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"{GITHUB_API_BASE}{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=headers, json=data) as response:
            if response.status >= 400:
                error_text = await response.text()
                raise ValueError(f"GitHub API error {response.status}: {error_text}")
            
            return await response.json()

@mcp.tool()
async def get_user_info(username: str) -> Dict[str, Any]:
    """Get GitHub user information."""
    user_data = await github_request(f"/users/{username}")
    
    return {
        "username": user_data["login"],
        "name": user_data.get("name"),
        "bio": user_data.get("bio"),
        "public_repos": user_data["public_repos"],
        "followers": user_data["followers"],
        "following": user_data["following"],
        "created_at": user_data["created_at"],
        "avatar_url": user_data["avatar_url"]
    }

@mcp.tool()
async def list_user_repos(username: str, limit: int = 10) -> List[Dict[str, Any]]:
    """List user's repositories."""
    repos_data = await github_request(f"/users/{username}/repos?per_page={limit}")
    
    return [
        {
            "name": repo["name"],
            "description": repo.get("description"),
            "language": repo.get("language"),
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "url": repo["html_url"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"]
        }
        for repo in repos_data
    ]

@mcp.tool()
async def search_repositories(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search GitHub repositories."""
    search_data = await github_request(f"/search/repositories?q={query}&per_page={limit}")
    
    return [
        {
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo.get("description"),
            "language": repo.get("language"),
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "url": repo["html_url"],
            "owner": repo["owner"]["login"]
        }
        for repo in search_data["items"]
    ]

@mcp.resource("github://user/{username}")
def github_user_resource(username: str) -> str:
    """GitHub user resource."""
    return f"GitHub user profile: {username} (use get_user_info tool for detailed data)"

@mcp.resource("github://trending")
def github_trending() -> str:
    """GitHub trending information."""
    return "GitHub trending repositories (use search_repositories with 'stars:>1000' for popular repos)"

if __name__ == "__main__":
    mcp.run()
```

## Development Tools Server

### Code Analysis and Project Tools
```python
import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DevTools")

@mcp.tool()
def analyze_python_file(file_path: str) -> Dict[str, Any]:
    """Analyze Python file for basic metrics."""
    if not file_path.endswith('.py'):
        raise ValueError("File must be a Python file (.py)")
    
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise ValueError(f"File not found: {file_path}")
    
    content = file_path_obj.read_text()
    lines = content.split('\n')
    
    # Basic analysis
    total_lines = len(lines)
    code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
    comment_lines = len([line for line in lines if line.strip().startswith('#')])
    blank_lines = total_lines - code_lines - comment_lines
    
    # Count functions and classes
    functions = len([line for line in lines if line.strip().startswith('def ')])
    classes = len([line for line in lines if line.strip().startswith('class ')])
    
    # Count imports
    imports = len([line for line in lines if line.strip().startswith(('import ', 'from '))])
    
    return {
        "file": file_path,
        "total_lines": total_lines,
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "complexity_score": code_lines / max(functions + classes, 1)  # Simple metric
    }

@mcp.tool()
def run_python_linter(file_path: str, linter: str = "flake8") -> Dict[str, Any]:
    """Run Python linter on a file."""
    if not Path(file_path).exists():
        raise ValueError(f"File not found: {file_path}")
    
    try:
        result = subprocess.run(
            [linter, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "file": file_path,
            "linter": linter,
            "exit_code": result.returncode,
            "output": result.stdout,
            "errors": result.stderr,
            "issues_found": result.returncode != 0
        }
    except subprocess.TimeoutExpired:
        return {"error": "Linter execution timed out"}
    except FileNotFoundError:
        return {"error": f"Linter '{linter}' not found. Install it with: pip install {linter}"}

@mcp.tool()
def run_tests(test_path: str = "tests/", framework: str = "pytest") -> Dict[str, Any]:
    """Run tests using specified framework."""
    try:
        cmd = [framework, test_path, "-v", "--tb=short"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return {
            "framework": framework,
            "test_path": test_path,
            "exit_code": result.returncode,
            "output": result.stdout,
            "errors": result.stderr,
            "tests_passed": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"error": "Test execution timed out"}
    except FileNotFoundError:
        return {"error": f"Test framework '{framework}' not found"}

@mcp.tool()
def git_status() -> Dict[str, Any]:
    """Get Git repository status."""
    try:
        # Check if we're in a git repository
        subprocess.run(["git", "rev-parse", "--git-dir"], 
                      capture_output=True, check=True)
        
        # Get status
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        )
        
        # Get current branch
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True
        )
        
        # Parse status
        status_lines = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
        modified_files = []
        new_files = []
        deleted_files = []
        
        for line in status_lines:
            if line:
                status_code = line[:2]
                file_path = line[3:]
                
                if 'M' in status_code:
                    modified_files.append(file_path)
                elif 'A' in status_code or '?' in status_code:
                    new_files.append(file_path)
                elif 'D' in status_code:
                    deleted_files.append(file_path)
        
        return {
            "current_branch": branch_result.stdout.strip(),
            "is_clean": len(status_lines) == 0,
            "modified_files": modified_files,
            "new_files": new_files,
            "deleted_files": deleted_files,
            "total_changes": len(status_lines)
        }
    
    except subprocess.CalledProcessError:
        return {"error": "Not a git repository"}

@mcp.resource("project://info")
def project_info() -> Dict[str, Any]:
    """Get project information."""
    cwd = Path.cwd()
    
    # Check for common project files
    project_files = {
        "requirements.txt": (cwd / "requirements.txt").exists(),
        "pyproject.toml": (cwd / "pyproject.toml").exists(),
        "package.json": (cwd / "package.json").exists(),
        "Dockerfile": (cwd / "Dockerfile").exists(),
        "README.md": (cwd / "README.md").exists(),
        ".gitignore": (cwd / ".gitignore").exists()
    }
    
    # Count Python files
    python_files = len(list(cwd.rglob("*.py")))
    
    return {
        "project_directory": str(cwd),
        "project_files": project_files,
        "python_files_count": python_files,
        "is_git_repo": (cwd / ".git").exists(),
        "has_tests": (cwd / "tests").exists() or (cwd / "test").exists()
    }

if __name__ == "__main__":
    mcp.run()
```

## Data Processing Server

### CSV and Data Analysis Server
```python
import pandas as pd
import json
import io
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DataProcessor")

# Store loaded datasets
_datasets: Dict[str, pd.DataFrame] = {}

@mcp.tool()
def load_csv(file_path: str, dataset_name: str, **kwargs) -> Dict[str, Any]:
    """Load CSV file into memory."""
    try:
        df = pd.read_csv(file_path, **kwargs)
        _datasets[dataset_name] = df
        
        return {
            "dataset_name": dataset_name,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
    except Exception as e:
        raise ValueError(f"Failed to load CSV: {e}")

@mcp.tool()
def dataset_info(dataset_name: str) -> Dict[str, Any]:
    """Get information about a loaded dataset."""
    if dataset_name not in _datasets:
        raise ValueError(f"Dataset '{dataset_name}' not found")
    
    df = _datasets[dataset_name]
    
    # Basic info
    info = {
        "name": dataset_name,
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "memory_usage": df.memory_usage(deep=True).sum()
    }
    
    # Statistical summary for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        info["numeric_summary"] = df[numeric_cols].describe().to_dict()
    
    return info

@mcp.tool()
def filter_dataset(
    dataset_name: str,
    column: str,
    operator: str,
    value: Union[str, int, float],
    new_dataset_name: Optional[str] = None
) -> Dict[str, Any]:
    """Filter dataset based on column criteria."""
    if dataset_name not in _datasets:
        raise ValueError(f"Dataset '{dataset_name}' not found")
    
    df = _datasets[dataset_name]
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataset")
    
    # Apply filter based on operator
    if operator == "==":
        filtered_df = df[df[column] == value]
    elif operator == "!=":
        filtered_df = df[df[column] != value]
    elif operator == ">":
        filtered_df = df[df[column] > value]
    elif operator == "<":
        filtered_df = df[df[column] < value]
    elif operator == ">=":
        filtered_df = df[df[column] >= value]
    elif operator == "<=":
        filtered_df = df[df[column] <= value]
    elif operator == "contains":
        filtered_df = df[df[column].astype(str).str.contains(str(value), na=False)]
    else:
        raise ValueError(f"Unsupported operator: {operator}")
    
    # Store filtered dataset
    result_name = new_dataset_name or f"{dataset_name}_filtered"
    _datasets[result_name] = filtered_df
    
    return {
        "original_dataset": dataset_name,
        "new_dataset": result_name,
        "original_rows": len(df),
        "filtered_rows": len(filtered_df),
        "filter_condition": f"{column} {operator} {value}"
    }

@mcp.tool()
def group_and_aggregate(
    dataset_name: str,
    group_by: Union[str, List[str]],
    aggregations: Dict[str, str],
    new_dataset_name: Optional[str] = None
) -> Dict[str, Any]:
    """Group dataset and apply aggregations."""
    if dataset_name not in _datasets:
        raise ValueError(f"Dataset '{dataset_name}' not found")
    
    df = _datasets[dataset_name]
    
    # Perform grouping and aggregation
    grouped = df.groupby(group_by).agg(aggregations).reset_index()
    
    # Flatten column names if multi-level
    if isinstance(grouped.columns, pd.MultiIndex):
        grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
    
    # Store result
    result_name = new_dataset_name or f"{dataset_name}_grouped"
    _datasets[result_name] = grouped
    
    return {
        "original_dataset": dataset_name,
        "new_dataset": result_name,
        "group_by": group_by,
        "aggregations": aggregations,
        "original_rows": len(df),
        "grouped_rows": len(grouped)
    }

@mcp.tool()
def export_dataset(dataset_name: str, file_path: str, format: str = "csv") -> str:
    """Export dataset to file."""
    if dataset_name not in _datasets:
        raise ValueError(f"Dataset '{dataset_name}' not found")
    
    df = _datasets[dataset_name]
    
    try:
        if format.lower() == "csv":
            df.to_csv(file_path, index=False)
        elif format.lower() == "json":
            df.to_json(file_path, orient="records", indent=2)
        elif format.lower() == "excel":
            df.to_excel(file_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return f"Dataset '{dataset_name}' exported to {file_path} as {format}"
    except Exception as e:
        raise ValueError(f"Export failed: {e}")

@mcp.resource("datasets://list")
def list_datasets() -> List[Dict[str, Any]]:
    """List all loaded datasets."""
    return [
        {
            "name": name,
            "rows": len(df),
            "columns": len(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
        for name, df in _datasets.items()
    ]

@mcp.resource("dataset://{dataset_name}/sample")
def dataset_sample(dataset_name: str, n: str = "5") -> List[Dict[str, Any]]:
    """Get sample rows from dataset."""
    if dataset_name not in _datasets:
        raise ValueError(f"Dataset '{dataset_name}' not found")
    
    df = _datasets[dataset_name]
    sample_size = min(int(n), len(df))
    
    return df.head(sample_size).to_dict(orient="records")

if __name__ == "__main__":
    mcp.run()
```

## Client Examples

### Basic MCP Client
```python
import asyncio
from mcp.client.stdio import StdioServerParameters, stdio_client

async def basic_client_example():
    """Basic client that connects to a server and calls tools."""
    
    # Server configuration
    server_params = StdioServerParameters(
        command="python",
        args=["calculator.py"],  # Path to your server script
        env={"PYTHONPATH": "."}
    )
    
    async with stdio_client(server_params) as client:
        # Initialize the connection
        await client.initialize()
        
        # List available tools
        tools_result = await client.list_tools()
        print("Available tools:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Call a tool
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"\nResult of add(5, 3): {result.content}")
        
        # List available resources
        resources_result = await client.list_resources()
        print(f"\nAvailable resources: {len(resources_result.resources)}")
        
        # Read a resource if available
        if resources_result.resources:
            resource = resources_result.resources[0]
            content = await client.read_resource(resource.uri)
            print(f"Resource content: {content.contents}")

if __name__ == "__main__":
    asyncio.run(basic_client_example())
```

### Advanced Client with Error Handling
```python
import asyncio
import logging
from typing import Any, Dict, List, Optional
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.exceptions import McpError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPClientWrapper:
    """Wrapper class for MCP client operations."""
    
    def __init__(self, server_command: str, server_args: List[str]):
        self.server_params = StdioServerParameters(
            command=server_command,
            args=server_args
        )
        self.client = None
    
    async def __aenter__(self):
        self.client = await stdio_client(self.server_params).__aenter__()
        await self.client.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def safe_call_tool(self, name: str, arguments: Dict[str, Any]) -> Optional[Any]:
        """Safely call a tool with error handling."""
        try:
            result = await self.client.call_tool(name, arguments)
            logger.info(f"Tool '{name}' executed successfully")
            return result.content
        except McpError as e:
            logger.error(f"MCP error calling tool '{name}': {e.message}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling tool '{name}': {e}")
            return None
    
    async def safe_read_resource(self, uri: str) -> Optional[str]:
        """Safely read a resource with error handling."""
        try:
            result = await self.client.read_resource(uri)
            logger.info(f"Resource '{uri}' read successfully")
            return result.contents[0].text if result.contents else None
        except McpError as e:
            logger.error(f"MCP error reading resource '{uri}': {e.message}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error reading resource '{uri}': {e}")
            return None
    
    async def get_capabilities(self) -> Dict[str, List[str]]:
        """Get server capabilities."""
        try:
            tools = await self.client.list_tools()
            resources = await self.client.list_resources()
            prompts = await self.client.list_prompts()
            
            return {
                "tools": [tool.name for tool in tools.tools],
                "resources": [resource.uri for resource in resources.resources],
                "prompts": [prompt.name for prompt in prompts.prompts]
            }
        except Exception as e:
            logger.error(f"Error getting capabilities: {e}")
            return {"tools": [], "resources": [], "prompts": []}

async def advanced_client_example():
    """Advanced client example with comprehensive error handling."""
    
    async with MCPClientWrapper("python", ["file_manager.py"]) as client:
        # Get server capabilities
        capabilities = await client.get_capabilities()
        print("Server capabilities:", capabilities)
        
        # Test file operations
        if "list_directory" in capabilities["tools"]:
            result = await client.safe_call_tool("list_directory", {"path": "."})
            if result:
                print(f"Directory listing: {len(result)} items")
        
        # Test resource reading
        if capabilities["resources"]:
            for resource_uri in capabilities["resources"][:3]:  # Test first 3
                content = await client.safe_read_resource(resource_uri)
                if content:
                    print(f"Resource {resource_uri}: {len(content)} characters")

if __name__ == "__main__":
    asyncio.run(advanced_client_example())
```

## Testing Examples

### Unit Testing for MCP Servers
```python
import pytest
import asyncio
from mcp.client.stdio import StdioServerParameters, stdio_client

class TestCalculatorServer:
    """Test suite for calculator MCP server."""
    
    @pytest.fixture
    async def client(self):
        """Fixture to create and initialize MCP client."""
        server_params = StdioServerParameters(
            command="python",
            args=["calculator.py"]
        )
        
        async with stdio_client(server_params) as client:
            await client.initialize()
            yield client
    
    @pytest.mark.asyncio
    async def test_add_tool(self, client):
        """Test the add tool."""
        result = await client.call_tool("add", {"a": 5, "b": 3})
        assert result.content == 8
    
    @pytest.mark.asyncio
    async def test_divide_by_zero(self, client):
        """Test division by zero error handling."""
        with pytest.raises(Exception):
            await client.call_tool("divide", {"a": 5, "b": 0})
    
    @pytest.mark.asyncio
    async def test_server_capabilities(self, client):
        """Test server capabilities."""
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools.tools]
        
        expected_tools = ["add", "subtract", "multiply", "divide"]
        for tool_name in expected_tools:
            assert tool_name in tool_names

# Run tests with: pytest test_calculator.py -v
```

### Integration Testing
```python
import pytest
import tempfile
import os
from pathlib import Path

class TestFileSystemServer:
    """Integration tests for file system MCP server."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    @pytest.fixture
    async def client(self):
        """Fixture to create file system client."""
        server_params = StdioServerParameters(
            command="python",
            args=["file_system.py"]
        )
        
        async with stdio_client(server_params) as client:
            await client.initialize()
            yield client
    
    @pytest.mark.asyncio
    async def test_file_operations(self, client, temp_dir):
        """Test complete file operation workflow."""
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Hello, MCP!"
        
        # Create file
        result = await client.call_tool("write_file", {
            "path": test_file,
            "content": test_content
        })
        assert "File written" in result
        
        # Read file
        content = await client.read_resource(f"file://{test_file}")
        assert content.contents[0].text == test_content
        
        # List directory
        files = await client.call_tool("list_directory", {"path": temp_dir})
        assert any(f["name"] == "test.txt" for f in files)
        
        # Delete file
        result = await client.call_tool("delete_file", {"path": test_file})
        assert "File deleted" in result
        
        # Verify deletion
        assert not Path(test_file).exists()
```

## Production Deployment

### Production Server Template
```python
import os
import logging
import signal
import sys
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProductionServer:
    """Production-ready MCP server with proper error handling and monitoring."""
    
    def __init__(self):
        self.mcp = FastMCP(
            name="ProductionServer",
            version=os.getenv("SERVER_VERSION", "1.0.0")
        )
        self.setup_tools()
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers."""
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)
    
    def shutdown_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        # Cleanup code here (close connections, save state, etc.)
        sys.exit(0)
    
    def setup_tools(self):
        """Setup all tools with proper error handling."""
        
        @self.mcp.tool()
        def health_check() -> dict:
            """Health check endpoint for monitoring."""
            return {
                "status": "healthy",
                "version": os.getenv("SERVER_VERSION", "1.0.0"),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        @self.mcp.tool()
        def get_metrics() -> dict:
            """Get server metrics for monitoring."""
            import psutil
            
            return {
                "memory_usage": psutil.virtual_memory().percent,
                "cpu_usage": psutil.cpu_percent(),
                "disk_usage": psutil.disk_usage('/').percent,
                "uptime": time.time() - self.start_time
            }
    
    def run(self):
        """Run the server."""
        logger.info("Starting MCP server...")
        try:
            self.mcp.run()
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            raise

if __name__ == "__main__":
    server = ProductionServer()
    server.run()
```

### Docker Deployment
```dockerfile
# Dockerfile for MCP server
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python health_check.py

EXPOSE 8080

CMD ["python", "production_server.py"]
```

### Environment Configuration
```python
# config.py
import os
from typing import Optional

class Config:
    """Configuration management for MCP server."""
    
    # Server settings
    SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "MCPServer")
    SERVER_VERSION: str = os.getenv("MCP_SERVER_VERSION", "1.0.0")
    
    # Database settings
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # API keys
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Security settings
    ALLOWED_PATHS: list = os.getenv("ALLOWED_PATHS", "/tmp,/home").split(",")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "mcp_server.log")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        required_vars = []  # Add required environment variables
        missing = [var for var in required_vars if not getattr(cls, var)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
        
        return True

# Load and validate config on import
Config.validate()
```

These examples provide a comprehensive foundation for building MCP servers and clients. Each example includes proper error handling, type hints, and production considerations. Use them as starting points and adapt them to your specific needs.