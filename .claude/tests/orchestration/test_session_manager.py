#!/usr/bin/env python3
"""
Comprehensive test suite for session_manager.py UV script

Tests session lifecycle management, different modes, recovery mechanisms,
heartbeat functionality, and session expiry handling.
"""

import json
import os
import subprocess
import tempfile
import threading
import time
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock


class SessionManagerTestCase(unittest.TestCase):
    """Base test case with common setup for session manager tests"""
    
    def setUp(self):
        """Set up test environment with temporary directories"""
        self.test_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.test_dir, "test_state.json")
        self.script_path = ".claude/scripts/session_manager.py"
        
        # Create initial state with some sessions
        self.initial_state = {
            "sessions": {
                "active_session": {
                    "id": "active_session",
                    "mode": "development",
                    "created": datetime.utcnow().isoformat() + "Z",
                    "last_heartbeat": datetime.utcnow().isoformat() + "Z",
                    "user": "test_user",
                    "status": "active",
                    "context": {
                        "current_task": "testing",
                        "project_id": "test_project"
                    }
                },
                "expired_session": {
                    "id": "expired_session",
                    "mode": "sprint",
                    "created": (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z",
                    "last_heartbeat": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z",
                    "user": "other_user",
                    "status": "inactive",
                    "context": {}
                }
            },
            "project": {
                "name": "test_project",
                "current_session": "active_session"
            }
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(self.initial_state, f, indent=2)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def run_script(self, command, *args, expect_success=True):
        """Helper to run session_manager.py script commands"""
        cmd = ["python3", self.script_path, command, "--state-file", self.state_file] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if expect_success and result.returncode != 0:
            self.fail(f"Script failed: {result.stderr}")
        
        return result


class TestSessionLifecycle(SessionManagerTestCase):
    """Test session creation, updates, and deletion"""
    
    def test_create_development_session(self):
        """Test creating a new development session"""
        result = self.run_script("create", "--mode", "development", "--user", "test_dev")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("session_id", data)
        self.assertEqual(data["mode"], "development")
        self.assertEqual(data["user"], "test_dev")
        self.assertEqual(data["status"], "active")
        
        # Verify session was stored in state
        session_id = data["session_id"]
        check_result = self.run_script("get", session_id)
        session_data = json.loads(check_result.stdout)
        self.assertEqual(session_data["mode"], "development")
    
    def test_create_leadership_session(self):
        """Test creating a leadership session"""
        result = self.run_script("create", "--mode", "leadership", "--user", "team_lead")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["mode"], "leadership")
        self.assertIn("permissions", data)
        self.assertIn("team_management", data["permissions"])
    
    def test_create_sprint_session(self):
        """Test creating a sprint execution session"""
        result = self.run_script("create", "--mode", "sprint", "--user", "scrum_master", 
                                "--context", json.dumps({"sprint_id": "sprint_001"}))
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["mode"], "sprint")
        self.assertEqual(data["context"]["sprint_id"], "sprint_001")
    
    def test_create_config_session(self):
        """Test creating a configuration session"""
        result = self.run_script("create", "--mode", "config", "--user", "admin")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["mode"], "config")
        self.assertIn("permissions", data)
        self.assertIn("system_config", data["permissions"])
    
    def test_create_session_with_context(self):
        """Test creating session with custom context"""
        context = {
            "project_id": "proj_123",
            "team": "engineering",
            "goal": "implement_feature_x"
        }
        
        result = self.run_script("create", "--mode", "development", "--user", "dev1",
                                "--context", json.dumps(context))
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["context"], context)
    
    def test_session_id_uniqueness(self):
        """Test that session IDs are unique"""
        session_ids = set()
        
        for i in range(5):
            result = self.run_script("create", "--mode", "development", "--user", f"user_{i}")
            data = json.loads(result.stdout)
            session_id = data["session_id"]
            self.assertNotIn(session_id, session_ids, "Session ID should be unique")
            session_ids.add(session_id)


class TestSessionModes(SessionManagerTestCase):
    """Test different session mode behaviors"""
    
    def test_development_mode_permissions(self):
        """Test development mode specific permissions"""
        result = self.run_script("create", "--mode", "development", "--user", "dev")
        data = json.loads(result.stdout)
        
        permissions = data.get("permissions", [])
        expected_permissions = ["code_edit", "test_run", "debug", "git_operations"]
        
        for perm in expected_permissions:
            self.assertIn(perm, permissions)
    
    def test_leadership_mode_permissions(self):
        """Test leadership mode specific permissions"""
        result = self.run_script("create", "--mode", "leadership", "--user", "lead")
        data = json.loads(result.stdout)
        
        permissions = data.get("permissions", [])
        expected_permissions = ["team_management", "resource_allocation", "strategic_planning"]
        
        for perm in expected_permissions:
            self.assertIn(perm, permissions)
    
    def test_sprint_mode_permissions(self):
        """Test sprint mode specific permissions"""
        result = self.run_script("create", "--mode", "sprint", "--user", "sm")
        data = json.loads(result.stdout)
        
        permissions = data.get("permissions", [])
        expected_permissions = ["task_assignment", "velocity_tracking", "sprint_management"]
        
        for perm in expected_permissions:
            self.assertIn(perm, permissions)
    
    def test_config_mode_permissions(self):
        """Test config mode specific permissions"""
        result = self.run_script("create", "--mode", "config", "--user", "admin")
        data = json.loads(result.stdout)
        
        permissions = data.get("permissions", [])
        expected_permissions = ["system_config", "agent_management", "tool_registry"]
        
        for perm in expected_permissions:
            self.assertIn(perm, permissions)
    
    def test_invalid_mode(self):
        """Test creating session with invalid mode"""
        result = self.run_script("create", "--mode", "invalid_mode", "--user", "user", 
                                expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid mode", result.stderr)


class TestHeartbeatFunctionality(SessionManagerTestCase):
    """Test session heartbeat and keepalive functionality"""
    
    def test_heartbeat_update(self):
        """Test updating session heartbeat"""
        session_id = "active_session"
        
        # Get initial heartbeat
        result = self.run_script("get", session_id)
        initial_data = json.loads(result.stdout)
        initial_heartbeat = initial_data["last_heartbeat"]
        
        # Wait a moment then send heartbeat
        time.sleep(0.1)
        result = self.run_script("heartbeat", session_id)
        self.assertEqual(result.returncode, 0)
        
        # Verify heartbeat was updated
        result = self.run_script("get", session_id)
        updated_data = json.loads(result.stdout)
        updated_heartbeat = updated_data["last_heartbeat"]
        
        self.assertGreater(updated_heartbeat, initial_heartbeat)
    
    def test_heartbeat_with_status_update(self):
        """Test heartbeat with status information"""
        session_id = "active_session"
        status_info = {
            "current_task": "running_tests",
            "progress": 75,
            "last_action": "test_execution"
        }
        
        result = self.run_script("heartbeat", session_id, "--status", json.dumps(status_info))
        self.assertEqual(result.returncode, 0)
        
        # Verify status was updated
        result = self.run_script("get", session_id)
        data = json.loads(result.stdout)
        self.assertEqual(data["status_info"], status_info)
    
    def test_heartbeat_nonexistent_session(self):
        """Test heartbeat for non-existent session"""
        result = self.run_script("heartbeat", "nonexistent_session", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Session not found", result.stderr)
    
    def test_heartbeat_expired_session(self):
        """Test heartbeat for expired session reactivates it"""
        session_id = "expired_session"
        
        result = self.run_script("heartbeat", session_id)
        self.assertEqual(result.returncode, 0)
        
        # Verify session is now active
        result = self.run_script("get", session_id)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "active")


class TestSessionHandoff(SessionManagerTestCase):
    """Test session handoff between users"""
    
    def test_basic_handoff(self):
        """Test basic session handoff between users"""
        session_id = "active_session"
        new_user = "new_user"
        handoff_notes = "Passing session to new user for continued work"
        
        result = self.run_script("handoff", session_id, "--to-user", new_user, 
                                "--notes", handoff_notes)
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["new_user"], new_user)
        self.assertEqual(data["handoff_notes"], handoff_notes)
        
        # Verify session was updated
        result = self.run_script("get", session_id)
        session_data = json.loads(result.stdout)
        self.assertEqual(session_data["user"], new_user)
        self.assertIn("handoff_history", session_data)
    
    def test_handoff_with_context_transfer(self):
        """Test handoff with context information transfer"""
        session_id = "active_session"
        context_update = {
            "current_task": "code_review",
            "priority": "high",
            "deadline": "2025-01-15"
        }
        
        result = self.run_script("handoff", session_id, "--to-user", "reviewer",
                                "--context", json.dumps(context_update))
        self.assertEqual(result.returncode, 0)
        
        # Verify context was updated
        result = self.run_script("get", session_id)
        data = json.loads(result.stdout)
        for key, value in context_update.items():
            self.assertEqual(data["context"][key], value)
    
    def test_handoff_preserves_history(self):
        """Test that handoff preserves session history"""
        session_id = "active_session"
        
        # Perform first handoff
        result = self.run_script("handoff", session_id, "--to-user", "user2", "--notes", "First handoff")
        self.assertEqual(result.returncode, 0)
        
        # Perform second handoff
        result = self.run_script("handoff", session_id, "--to-user", "user3", "--notes", "Second handoff")
        self.assertEqual(result.returncode, 0)
        
        # Verify history is preserved
        result = self.run_script("get", session_id)
        data = json.loads(result.stdout)
        handoff_history = data["handoff_history"]
        
        self.assertEqual(len(handoff_history), 2)
        self.assertEqual(handoff_history[0]["to_user"], "user2")
        self.assertEqual(handoff_history[1]["to_user"], "user3")
    
    def test_handoff_nonexistent_session(self):
        """Test handoff for non-existent session"""
        result = self.run_script("handoff", "nonexistent", "--to-user", "user", 
                                expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Session not found", result.stderr)


class TestSessionRecovery(SessionManagerTestCase):
    """Test session recovery mechanisms"""
    
    def test_recover_inactive_session(self):
        """Test recovering an inactive session"""
        session_id = "expired_session"
        
        result = self.run_script("recover", session_id, "--user", "recovery_user")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "recovered")
        
        # Verify session is now active
        result = self.run_script("get", session_id)
        session_data = json.loads(result.stdout)
        self.assertEqual(session_data["status"], "active")
        self.assertEqual(session_data["user"], "recovery_user")
    
    def test_recover_with_context_restoration(self):
        """Test recovery with context restoration"""
        session_id = "expired_session"
        restore_context = {
            "restored_from": "backup",
            "recovery_time": datetime.utcnow().isoformat() + "Z",
            "notes": "Session recovered after system restart"
        }
        
        result = self.run_script("recover", session_id, "--user", "admin",
                                "--context", json.dumps(restore_context))
        self.assertEqual(result.returncode, 0)
        
        # Verify context was restored
        result = self.run_script("get", session_id)
        data = json.loads(result.stdout)
        for key, value in restore_context.items():
            self.assertEqual(data["context"][key], value)
    
    def test_recover_already_active_session(self):
        """Test attempting to recover an already active session"""
        session_id = "active_session"
        
        result = self.run_script("recover", session_id, "--user", "user", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Session is already active", result.stderr)
    
    def test_bulk_recovery(self):
        """Test recovering multiple sessions"""
        # Create additional inactive sessions
        for i in range(3):
            self.run_script("create", "--mode", "development", "--user", f"user_{i}")
            # Immediately make them inactive by setting old heartbeat
            # This would be done through direct state manipulation in real test
        
        result = self.run_script("recover", "--all-inactive", "--user", "recovery_admin")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("recovered_sessions", data)
        self.assertGreater(len(data["recovered_sessions"]), 0)


class TestSessionExpiry(SessionManagerTestCase):
    """Test session expiry and cleanup functionality"""
    
    def test_list_expired_sessions(self):
        """Test listing sessions that have expired"""
        result = self.run_script("list", "--expired", "--max-age", "3600")  # 1 hour
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        expired_sessions = data["sessions"]
        
        # Should include the expired_session from setup
        expired_ids = [s["id"] for s in expired_sessions]
        self.assertIn("expired_session", expired_ids)
    
    def test_cleanup_expired_sessions(self):
        """Test cleaning up expired sessions"""
        result = self.run_script("cleanup", "--max-age", "3600", "--confirm")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("cleaned_up", data)
        self.assertGreater(data["cleaned_up"], 0)
        
        # Verify expired session was removed
        result = self.run_script("get", "expired_session", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
    
    def test_cleanup_with_archive(self):
        """Test cleanup with archiving instead of deletion"""
        result = self.run_script("cleanup", "--max-age", "3600", "--archive", "--confirm")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("archived", data)
        
        # Verify session was archived (moved to archived_sessions)
        # This would check the archived_sessions section in state
    
    def test_session_auto_expiry_check(self):
        """Test automatic expiry checking during operations"""
        # This would test that expired sessions are automatically detected
        # during normal operations like list, get, etc.
        pass


class TestConcurrentSessionOperations(SessionManagerTestCase):
    """Test concurrent session operations"""
    
    def test_concurrent_session_creation(self):
        """Test creating multiple sessions concurrently"""
        results = []
        errors = []
        
        def create_session(user_id):
            try:
                result = self.run_script("create", "--mode", "development", "--user", f"user_{user_id}")
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    results.append(data["session_id"])
            except Exception as e:
                errors.append(str(e))
        
        # Create sessions concurrently
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_session, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify all sessions were created successfully
        self.assertEqual(len(errors), 0, f"Errors: {errors}")
        self.assertEqual(len(results), 5)
        self.assertEqual(len(set(results)), 5)  # All IDs should be unique
    
    def test_concurrent_heartbeats(self):
        """Test concurrent heartbeat operations"""
        session_id = "active_session"
        results = []
        errors = []
        
        def send_heartbeat():
            try:
                result = self.run_script("heartbeat", session_id)
                if result.returncode == 0:
                    results.append("success")
            except Exception as e:
                errors.append(str(e))
        
        # Send concurrent heartbeats
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=send_heartbeat)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All heartbeats should succeed
        self.assertEqual(len(errors), 0, f"Errors: {errors}")
        self.assertEqual(len(results), 3)


class TestSessionValidation(SessionManagerTestCase):
    """Test session validation and error handling"""
    
    def test_invalid_user_parameter(self):
        """Test creation with invalid user parameter"""
        result = self.run_script("create", "--mode", "development", "--user", "", 
                                expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("User cannot be empty", result.stderr)
    
    def test_invalid_context_json(self):
        """Test creation with invalid JSON context"""
        result = self.run_script("create", "--mode", "development", "--user", "user",
                                "--context", "{invalid json}", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid JSON context", result.stderr)
    
    def test_session_mode_validation(self):
        """Test validation of session mode parameters"""
        valid_modes = ["development", "leadership", "sprint", "config"]
        
        for mode in valid_modes:
            result = self.run_script("create", "--mode", mode, "--user", "test")
            self.assertEqual(result.returncode, 0, f"Mode {mode} should be valid")
    
    def test_missing_required_parameters(self):
        """Test handling of missing required parameters"""
        # Missing user
        result = self.run_script("create", "--mode", "development", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        
        # Missing mode
        result = self.run_script("create", "--user", "test", expect_success=False)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestSessionLifecycle,
        TestSessionModes,
        TestHeartbeatFunctionality,
        TestSessionHandoff,
        TestSessionRecovery,
        TestSessionExpiry,
        TestConcurrentSessionOperations,
        TestSessionValidation
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=open('test_session_manager_results.txt', 'w'))
    result = runner.run(test_suite)
    
    # Print summary to console
    print(f"\nSession Manager Test Results:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")