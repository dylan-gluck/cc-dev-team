#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.24.0",
# ]
# ///
"""
Test script to verify ArtDept MCP server installation and dependencies.

Usage:
    ./test_server.py
"""

import json
import os
import sys
from pathlib import Path


def main() -> int:
    """Test the ArtDept MCP server setup."""
    print("ArtDept MCP Server Test")
    print("=" * 50)

    # Check Python version
    import sys
    print(f"Python version: {sys.version}")

    # Check if main.py exists
    main_path = Path(__file__).parent / "main.py"
    if main_path.exists():
        print(f"✓ Main server script found: {main_path}")
    else:
        print(f"✗ Main server script not found at: {main_path}")
        return 1

    # Check if executable
    if os.access(main_path, os.X_OK):
        print("✓ Server script is executable")
    else:
        print("✗ Server script is not executable")
        return 1

    # Check environment variable
    if os.getenv("OPENAI_API_KEY"):
        print("✓ OPENAI_API_KEY environment variable is set")
    else:
        print("✗ OPENAI_API_KEY environment variable is not set")
        print("  Set it with: export OPENAI_API_KEY='your-api-key'")
        return 1

    # Try importing required modules
    try:
        import mcp
        print(f"✓ MCP module available: {mcp.__version__ if hasattr(mcp, '__version__') else 'unknown version'}")
    except ImportError as e:
        print(f"✗ MCP module import failed: {e}")
        return 1

    try:
        import openai
        print(f"✓ OpenAI module available: {openai.__version__ if hasattr(openai, '__version__') else 'unknown version'}")
    except ImportError as e:
        print(f"✗ OpenAI module import failed: {e}")
        return 1

    print("\n" + "=" * 50)
    print("All checks passed! The ArtDept MCP server is ready to use.")
    print("\nTo run the server directly:")
    print("  ./main.py")
    print("\nOr with uv:")
    print("  uv run main.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
