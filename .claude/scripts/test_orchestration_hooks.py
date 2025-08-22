#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["colorama"]
# ///
"""
Test script for V2 orchestration hooks
Validates hook integration with state management
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import tempfile
from colorama import init, Fore, Style

init(autoreset=True)

def run_hook(hook_script: str, input_data: dict) -> tuple[int, str, str]:
    """Run a hook script with JSON input."""
    hook_path = Path(__file__).parent.parent / 'hooks' / hook_script
    if not hook_path.exists():
        return 1, '', f"Hook script not found: {hook_path}"
    
    try:
        result = subprocess.run(
            ['uv', 'run', str(hook_path)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)

def test_session_init():
    """Test session initialization hook."""
    print(f"\n{Fore.CYAN}Testing Session Initialization Hook...{Style.RESET_ALL}")
    
    returncode, stdout, stderr = run_hook('orchestration_session_init.py', {})
    
    if returncode == 0:
        print(f"{Fore.GREEN}✓ Session init hook executed successfully{Style.RESET_ALL}")
        if stdout:
            print(f"  Output: {stdout.strip()}")
        
        # Verify session was created
        session_file = Path.cwd() / '.claude' / 'state' / 'current_session'
        if session_file.exists():
            session_id = session_file.read_text().strip()
            print(f"{Fore.GREEN}✓ Session ID saved: {session_id}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Session file not created{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Session init hook failed{Style.RESET_ALL}")
        if stderr:
            print(f"  Error: {stderr}")
    
    return returncode == 0

def test_task_handler():
    """Test task completion tracking."""
    print(f"\n{Fore.CYAN}Testing Task Handler Hook...{Style.RESET_ALL}")
    
    # Create test TodoWrite event
    event_data = {
        "tool": "TodoWrite",
        "input": {
            "todos": [
                {"content": "Implement feature", "status": "completed"},
                {"content": "Write tests", "status": "in_progress"},
                {"content": "Update docs", "status": "pending"}
            ]
        }
    }
    
    returncode, stdout, stderr = run_hook('orchestration_handler.py', event_data)
    
    if returncode == 0:
        print(f"{Fore.GREEN}✓ Task handler executed successfully{Style.RESET_ALL}")
        
        # Check if metrics were updated
        try:
            result = subprocess.run(
                ['uv', 'run', 'state_manager.py', 'get', 'default', '$.metrics'],
                cwd=Path.cwd() / '.claude' / 'scripts',
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                metrics = json.loads(result.stdout)
                print(f"{Fore.GREEN}✓ Metrics updated: {metrics}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Could not verify metrics: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Task handler failed{Style.RESET_ALL}")
        if stderr:
            print(f"  Error: {stderr}")
    
    return returncode == 0

def test_agent_spawn():
    """Test agent spawn tracking."""
    print(f"\n{Fore.CYAN}Testing Agent Spawn Tracking...{Style.RESET_ALL}")
    
    # Create test Agent event
    event_data = {
        "tool": "Agent",
        "input": {
            "agent": "test-agent",
            "task": "Test task"
        }
    }
    
    returncode, stdout, stderr = run_hook('orchestration_handler.py', event_data)
    
    if returncode == 0:
        print(f"{Fore.GREEN}✓ Agent spawn handler executed successfully{Style.RESET_ALL}")
        
        # Check if agent was registered
        try:
            result = subprocess.run(
                ['uv', 'run', 'state_manager.py', 'get', 'default', '$.agents'],
                cwd=Path.cwd() / '.claude' / 'scripts',
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                agents = json.loads(result.stdout)
                if 'test-agent' in agents:
                    print(f"{Fore.GREEN}✓ Agent registered: test-agent{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}⚠ Agent not found in state{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Could not verify agent registration: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Agent spawn handler failed{Style.RESET_ALL}")
        if stderr:
            print(f"  Error: {stderr}")
    
    return returncode == 0

def test_state_sync():
    """Test state synchronization."""
    print(f"\n{Fore.CYAN}Testing State Synchronization...{Style.RESET_ALL}")
    
    # Create test state change event
    event_data = {
        "tool": "Bash",
        "input": {
            "command": "uv run state_manager.py update session_test $.test value"
        }
    }
    
    returncode, stdout, stderr = run_hook('orchestration_handler.py', event_data)
    
    if returncode == 0:
        print(f"{Fore.GREEN}✓ State sync handler executed successfully{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ State sync handler failed{Style.RESET_ALL}")
        if stderr:
            print(f"  Error: {stderr}")
    
    return returncode == 0

def main():
    """Run all hook tests."""
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}V2 Orchestration Hook Integration Tests{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    
    # Track test results
    results = []
    
    # Run tests
    results.append(("Session Initialization", test_session_init()))
    results.append(("Task Handler", test_task_handler()))
    results.append(("Agent Spawn Tracking", test_agent_spawn()))
    results.append(("State Synchronization", test_state_sync()))
    
    # Summary
    print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Test Summary{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if result else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Fore.CYAN}Results: {passed}/{total} tests passed{Style.RESET_ALL}")
    
    if passed == total:
        print(f"{Fore.GREEN}✓ All hooks are properly integrated!{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"{Fore.YELLOW}⚠ Some hooks need attention{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main()