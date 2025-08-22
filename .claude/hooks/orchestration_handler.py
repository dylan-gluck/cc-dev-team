#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///
"""
V2 Orchestration Hook Handler
Integrates with state_manager.py, session_manager.py, and shared_state.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess

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

def handle_task_completion(event_data: dict) -> None:
    """Process TodoWrite events for task tracking."""
    tool_name = event_data.get('tool', '')
    
    if tool_name == 'TodoWrite':
        todos = event_data.get('input', {}).get('todos', [])
        if todos:
            # Get current session
            returncode, session_id, _ = run_uv_script('session_manager.py', 'current')
            if returncode != 0:
                session_id = 'default'
            else:
                session_id = session_id.strip()
            
            # Count task statuses
            completed = sum(1 for t in todos if t.get('status') == 'completed')
            in_progress = sum(1 for t in todos if t.get('status') == 'in_progress')
            pending = sum(1 for t in todos if t.get('status') == 'pending')
            
            # Update metrics
            if completed > 0:
                run_uv_script('state_manager.py', 'update', session_id,
                            '$.metrics.tasks_completed', str(completed))
                
                # Check for sprint workflow
                returncode, state_json, _ = run_uv_script('state_manager.py', 'get', session_id, '$')
                if returncode == 0:
                    try:
                        state = json.loads(state_json)
                        if state.get('workflow', {}).get('type') == 'sprint':
                            # Update sprint progress
                            total = completed + in_progress + pending
                            if total > 0:
                                progress = int((completed / total) * 100)
                                run_uv_script('state_manager.py', 'update', session_id,
                                            '$.workflow.progress', str(progress))
                    except json.JSONDecodeError:
                        pass
            
            # Log metrics
            run_uv_script('observability.py', 'log', 'task_update',
                        '--session', session_id,
                        '--completed', str(completed),
                        '--in_progress', str(in_progress),
                        '--pending', str(pending))

def handle_agent_spawn(event_data: dict) -> None:
    """Track agent spawning in state."""
    tool_name = event_data.get('tool', '')
    
    if tool_name == 'Agent':
        agent_name = event_data.get('input', {}).get('agent', '')
        if agent_name:
            # Get current session
            returncode, session_id, _ = run_uv_script('session_manager.py', 'current')
            if returncode != 0:
                session_id = 'default'
            else:
                session_id = session_id.strip()
            
            # Register agent spawn
            timestamp = datetime.utcnow().isoformat() + 'Z'
            run_uv_script('state_manager.py', 'update', session_id,
                        f'$.agents.{agent_name}.spawned_at', timestamp)
            
            # Sync shared state if needed
            run_uv_script('shared_state.py', 'sync', session_id)

def handle_state_change(event_data: dict) -> None:
    """Synchronize state changes across the system."""
    tool_name = event_data.get('tool', '')
    tool_input = event_data.get('input', {})
    
    # Check for state management operations
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        if 'state_manager.py' in command:
            # Extract session ID from command
            parts = command.split()
            if 'session_' in command:
                for part in parts:
                    if part.startswith('session_'):
                        session_id = part
                        break
                else:
                    session_id = 'default'
            else:
                session_id = 'default'
            
            # Sync shared state
            run_uv_script('shared_state.py', 'sync', session_id)
            
            # Update observability
            run_uv_script('observability.py', 'log', 'state_change',
                        '--session', session_id)

def main():
    """Main hook handler entry point."""
    try:
        # Read event data from stdin
        event_data = json.load(sys.stdin)
        
        # Route to appropriate handler
        handle_task_completion(event_data)
        handle_agent_spawn(event_data)
        handle_state_change(event_data)
        
        # Always exit successfully to not block operations
        sys.exit(0)
        
    except Exception:
        # Silently handle any errors to not disrupt workflow
        sys.exit(0)

if __name__ == '__main__':
    main()