#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///
"""
V2 Orchestration Session Initializer
Sets up new orchestration sessions with proper state structure
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import time

# Add scripts directory to path
scripts_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve() / '.claude' / 'scripts'
sys.path.insert(0, str(scripts_dir))

def run_uv_script(script_name: str, *args) -> tuple[int, str, str]:
    """Run a UV script in the scripts directory."""
    try:
        result = subprocess.run(
            ['uv', 'run', script_name] + list(args),
            cwd=scripts_dir,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)

def initialize_session() -> str:
    """Initialize a new orchestration session."""
    # Generate session ID
    timestamp = int(time.time())
    pid = os.getpid()
    session_id = f"session_{timestamp}_{pid}"
    
    # Create session using session_manager
    returncode, _, _ = run_uv_script('session_manager.py', 'create', session_id)
    
    # Create initial state structure
    initial_state = {
        "session_id": session_id,
        "created_at": datetime.utcnow().isoformat() + 'Z',
        "workflow": {
            "type": None,
            "status": "initialized",
            "progress": 0,
            "config": {}
        },
        "agents": {},
        "metrics": {
            "tokens_used": 0,
            "tasks_completed": 0,
            "tests_written": False,
            "documentation_updated": False,
            "start_time": datetime.utcnow().isoformat() + 'Z'
        },
        "shared_context": {
            "requirements": [],
            "decisions": [],
            "blockers": []
        },
        "output_style": "default",
        "orchestration_mode": "manual",
        "integrations": {
            "hooks_enabled": True,
            "state_sync": True,
            "observability": True
        }
    }
    
    # Save initial state
    state_json = json.dumps(initial_state)
    returncode, _, _ = run_uv_script('state_manager.py', 'set', session_id, '$', '--stdin')
    
    # Create session directories
    project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.'))
    session_dir = project_dir / '.claude' / 'state' / 'sessions' / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / 'outputs').mkdir(exist_ok=True)
    (session_dir / 'artifacts').mkdir(exist_ok=True)
    
    # Initialize event stream
    run_uv_script('event_stream.py', 'init', session_id)
    
    # Log session creation
    run_uv_script('observability.py', 'log', 'session_created',
                  '--session', session_id,
                  '--mode', 'v2_orchestration')
    
    # Save current session reference
    current_session_file = project_dir / '.claude' / 'state' / 'current_session'
    current_session_file.parent.mkdir(parents=True, exist_ok=True)
    current_session_file.write_text(session_id)
    
    return session_id

def check_existing_session() -> str:
    """Check if there's an existing active session."""
    returncode, session_id, _ = run_uv_script('session_manager.py', 'current')
    if returncode == 0 and session_id.strip():
        return session_id.strip()
    return None

def main():
    """Main entry point for session initialization."""
    try:
        # Check for existing session
        existing_session = check_existing_session()
        
        if existing_session:
            # Validate existing session is still valid
            returncode, state_json, _ = run_uv_script('state_manager.py', 'get', existing_session, '$')
            if returncode == 0:
                try:
                    state = json.loads(state_json)
                    # If session exists and is valid, just update last_accessed
                    run_uv_script('state_manager.py', 'update', existing_session,
                                '$.last_accessed', datetime.utcnow().isoformat() + 'Z')
                    print(f"Resuming orchestration session: {existing_session}")
                    sys.exit(0)
                except json.JSONDecodeError:
                    pass
        
        # Initialize new session
        session_id = initialize_session()
        print(f"V2 Orchestration session initialized: {session_id}")
        print(f"Mode: manual (use /orchestrate commands to control workflow)")
        
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't block
        print(f"Session initialization notice: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()