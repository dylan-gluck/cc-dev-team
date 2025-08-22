#!/usr/bin/env python3
"""
Comprehensive test suite for state_manager.py UV script

Tests all CRUD operations, JSONPath queries, concurrent access,
error handling, and session management functions.
"""

import json
import os
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock


class StateManagerTestCase(unittest.TestCase):
    """Base test case with common setup for state manager tests"""
    
    def setUp(self):
        """Set up test environment with temporary directories"""
        self.test_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.test_dir, "test_state.json")
        self.script_path = ".claude/scripts/state_manager.py"
        
        # Create initial state file
        self.initial_state = {
            "sessions": {
                "session_1": {
                    "id": "session_1",
                    "mode": "development",
                    "created": "2025-01-01T10:00:00Z",
                    "last_heartbeat": "2025-01-01T10:30:00Z",
                    "user": "test_user",
                    "status": "active"
                }
            },
            "project": {
                "name": "test_project",
                "version": "1.0.0",
                "settings": {
                    "debug": True,
                    "timeout": 30
                }
            },
            "teams": {
                "engineering": {
                    "lead": "engineering-lead",
                    "members": ["engineering-fullstack", "engineering-api"]
                }
            }
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(self.initial_state, f, indent=2)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def run_script(self, command, *args, expect_success=True):
        """Helper to run state_manager.py script commands"""
        cmd = ["python3", self.script_path, command, "--state-file", self.state_file] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if expect_success and result.returncode != 0:
            self.fail(f"Script failed: {result.stderr}")
        
        return result


class TestStateCRUDOperations(StateManagerTestCase):
    """Test Create, Read, Update, Delete operations"""
    
    def test_get_existing_path(self):
        """Test retrieving existing state values"""
        result = self.run_script("get", "project.name")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["value"], "test_project")
        self.assertEqual(data["path"], "project.name")
    
    def test_get_nonexistent_path(self):
        """Test retrieving non-existent state values"""
        result = self.run_script("get", "nonexistent.path", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Path not found", result.stderr)
    
    def test_set_new_value(self):
        """Test setting new state values"""
        result = self.run_script("set", "project.description", "A test project")
        self.assertEqual(result.returncode, 0)
        
        # Verify the value was set
        result = self.run_script("get", "project.description")
        data = json.loads(result.stdout)
        self.assertEqual(data["value"], "A test project")
    
    def test_set_nested_path(self):
        """Test setting values in nested paths"""
        result = self.run_script("set", "project.database.host", "localhost")
        self.assertEqual(result.returncode, 0)
        
        # Verify nested structure was created
        result = self.run_script("get", "project.database.host")
        data = json.loads(result.stdout)
        self.assertEqual(data["value"], "localhost")
    
    def test_set_complex_value(self):
        """Test setting complex JSON values"""
        complex_value = json.dumps({"items": [1, 2, 3], "enabled": True})
        result = self.run_script("set", "project.config", complex_value)
        self.assertEqual(result.returncode, 0)
        
        # Verify complex value was stored correctly
        result = self.run_script("get", "project.config")
        data = json.loads(result.stdout)
        expected = {"items": [1, 2, 3], "enabled": True}
        self.assertEqual(data["value"], expected)
    
    def test_merge_operation(self):
        """Test merging values into existing objects"""
        merge_data = json.dumps({"new_field": "new_value", "timeout": 60})
        result = self.run_script("merge", "project.settings", merge_data)
        self.assertEqual(result.returncode, 0)
        
        # Verify merge results
        result = self.run_script("get", "project.settings")
        data = json.loads(result.stdout)
        self.assertEqual(data["value"]["debug"], True)  # Original value preserved
        self.assertEqual(data["value"]["timeout"], 60)  # Updated value
        self.assertEqual(data["value"]["new_field"], "new_value")  # New value added
    
    def test_merge_nonexistent_path(self):
        """Test merging into non-existent path creates new object"""
        merge_data = json.dumps({"key": "value"})
        result = self.run_script("merge", "project.new_section", merge_data)
        self.assertEqual(result.returncode, 0)
        
        # Verify new object was created
        result = self.run_script("get", "project.new_section")
        data = json.loads(result.stdout)
        self.assertEqual(data["value"], {"key": "value"})
    
    def test_delete_existing_path(self):
        """Test deleting existing state values"""
        result = self.run_script("delete", "project.settings.debug")
        self.assertEqual(result.returncode, 0)
        
        # Verify deletion
        result = self.run_script("get", "project.settings.debug", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        
        # Verify parent object still exists
        result = self.run_script("get", "project.settings")
        data = json.loads(result.stdout)
        self.assertNotIn("debug", data["value"])
        self.assertIn("timeout", data["value"])
    
    def test_delete_nonexistent_path(self):
        """Test deleting non-existent path fails gracefully"""
        result = self.run_script("delete", "nonexistent.path", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Path not found", result.stderr)


class TestJSONPathQueries(StateManagerTestCase):
    """Test JSONPath query functionality"""
    
    def test_simple_jsonpath_query(self):
        """Test basic JSONPath queries"""
        result = self.run_script("query", "$.sessions[*].mode")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("development", data["results"])
    
    def test_complex_jsonpath_query(self):
        """Test complex JSONPath with filters"""
        result = self.run_script("query", "$.sessions[?(@.status=='active')].id")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("session_1", data["results"])
    
    def test_recursive_descent_query(self):
        """Test recursive descent JSONPath queries"""
        result = self.run_script("query", "$..members")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertTrue(any("engineering-fullstack" in str(result) for result in data["results"]))
    
    def test_invalid_jsonpath_expression(self):
        """Test invalid JSONPath expressions are handled"""
        result = self.run_script("query", "invalid[[[path", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid JSONPath", result.stderr)


class TestConcurrentAccess(StateManagerTestCase):
    """Test concurrent access and file locking"""
    
    def test_concurrent_read_operations(self):
        """Test multiple concurrent read operations"""
        results = []
        errors = []
        
        def read_worker():
            try:
                result = self.run_script("get", "project.name")
                results.append(json.loads(result.stdout)["value"])
            except Exception as e:
                errors.append(str(e))
        
        # Start multiple concurrent readers
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=read_worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all reads succeeded
        self.assertEqual(len(errors), 0, f"Read errors: {errors}")
        self.assertEqual(len(results), 5)
        self.assertTrue(all(r == "test_project" for r in results))
    
    def test_concurrent_write_operations(self):
        """Test concurrent write operations with locking"""
        results = []
        errors = []
        
        def write_worker(worker_id):
            try:
                result = self.run_script("set", f"workers.worker_{worker_id}", f"value_{worker_id}")
                if result.returncode == 0:
                    results.append(worker_id)
            except Exception as e:
                errors.append(f"Worker {worker_id}: {str(e)}")
        
        # Start multiple concurrent writers
        threads = []
        for i in range(3):
            thread = threading.Thread(target=write_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all writes succeeded (file locking should prevent corruption)
        self.assertEqual(len(errors), 0, f"Write errors: {errors}")
        self.assertEqual(len(results), 3)
        
        # Verify final state is consistent
        for worker_id in range(3):
            result = self.run_script("get", f"workers.worker_{worker_id}")
            data = json.loads(result.stdout)
            self.assertEqual(data["value"], f"value_{worker_id}")
    
    def test_read_write_concurrency(self):
        """Test concurrent read and write operations"""
        read_results = []
        write_results = []
        errors = []
        
        def reader():
            try:
                for _ in range(5):
                    result = self.run_script("get", "project.name")
                    read_results.append(json.loads(result.stdout)["value"])
                    time.sleep(0.01)
            except Exception as e:
                errors.append(f"Reader: {str(e)}")
        
        def writer():
            try:
                for i in range(3):
                    result = self.run_script("set", f"concurrent.write_{i}", f"data_{i}")
                    if result.returncode == 0:
                        write_results.append(i)
                    time.sleep(0.01)
            except Exception as e:
                errors.append(f"Writer: {str(e)}")
        
        # Start concurrent reader and writer
        reader_thread = threading.Thread(target=reader)
        writer_thread = threading.Thread(target=writer)
        
        reader_thread.start()
        writer_thread.start()
        
        reader_thread.join()
        writer_thread.join()
        
        # Verify no errors occurred
        self.assertEqual(len(errors), 0, f"Concurrency errors: {errors}")
        self.assertEqual(len(read_results), 5)
        self.assertEqual(len(write_results), 3)


class TestSessionManagement(StateManagerTestCase):
    """Test session management functions"""
    
    def test_list_sessions(self):
        """Test listing all sessions"""
        result = self.run_script("list-sessions")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("sessions", data)
        self.assertIn("session_1", [s["id"] for s in data["sessions"]])
    
    def test_list_sessions_with_filter(self):
        """Test listing sessions with status filter"""
        result = self.run_script("list-sessions", "--status", "active")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertTrue(all(s["status"] == "active" for s in data["sessions"]))
    
    def test_cleanup_expired_sessions(self):
        """Test cleanup of expired sessions"""
        # Add an expired session
        expired_session = {
            "id": "expired_session",
            "mode": "development",
            "created": "2024-01-01T10:00:00Z",
            "last_heartbeat": "2024-01-01T10:00:00Z",
            "user": "test_user",
            "status": "active"
        }
        
        self.run_script("set", "sessions.expired_session", json.dumps(expired_session))
        
        # Run cleanup with 1 hour expiry
        result = self.run_script("cleanup-expired", "--max-age", "3600")
        self.assertEqual(result.returncode, 0)
        
        # Verify expired session was removed
        result = self.run_script("get", "sessions.expired_session", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        
        # Verify active session was preserved
        result = self.run_script("get", "sessions.session_1")
        self.assertEqual(result.returncode, 0)


class TestErrorHandling(StateManagerTestCase):
    """Test error handling scenarios"""
    
    def test_invalid_json_in_set(self):
        """Test setting invalid JSON values"""
        result = self.run_script("set", "project.invalid", "{invalid json}", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid JSON", result.stderr)
    
    def test_invalid_path_format(self):
        """Test invalid path formats"""
        result = self.run_script("get", "", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid path", result.stderr)
    
    def test_permission_denied_state_file(self):
        """Test handling of permission denied errors"""
        # Make state file read-only
        os.chmod(self.state_file, 0o444)
        
        try:
            result = self.run_script("set", "project.readonly", "value", expect_success=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Permission denied", result.stderr)
        finally:
            # Restore permissions for cleanup
            os.chmod(self.state_file, 0o644)
    
    def test_corrupted_state_file(self):
        """Test handling of corrupted state files"""
        # Corrupt the state file
        with open(self.state_file, 'w') as f:
            f.write("{ invalid json content }")
        
        result = self.run_script("get", "project.name", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Failed to parse state file", result.stderr)
    
    def test_missing_state_file(self):
        """Test handling when state file doesn't exist"""
        os.remove(self.state_file)
        
        # First operation should create new state file
        result = self.run_script("set", "new.key", "value")
        self.assertEqual(result.returncode, 0)
        
        # Verify file was created and value set
        self.assertTrue(os.path.exists(self.state_file))
        result = self.run_script("get", "new.key")
        data = json.loads(result.stdout)
        self.assertEqual(data["value"], "value")


class TestPerformanceAndBenchmarks(StateManagerTestCase):
    """Test performance characteristics and benchmarks"""
    
    def test_large_state_performance(self):
        """Test performance with large state objects"""
        # Create large state with many nested objects
        large_data = {
            f"item_{i}": {
                "value": f"data_{i}",
                "nested": {f"key_{j}": f"value_{j}" for j in range(10)}
            }
            for i in range(100)
        }
        
        start_time = time.time()
        result = self.run_script("set", "performance.large_data", json.dumps(large_data))
        set_time = time.time() - start_time
        
        self.assertEqual(result.returncode, 0)
        self.assertLess(set_time, 1.0, "Set operation should complete within 1 second")
        
        # Test retrieval performance
        start_time = time.time()
        result = self.run_script("get", "performance.large_data.item_50")
        get_time = time.time() - start_time
        
        self.assertEqual(result.returncode, 0)
        self.assertLess(get_time, 0.1, "Get operation should complete within 100ms")
    
    def test_query_performance(self):
        """Test JSONPath query performance"""
        # Create test data for queries
        test_data = {
            "items": [
                {"id": i, "status": "active" if i % 2 == 0 else "inactive", "value": f"item_{i}"}
                for i in range(50)
            ]
        }
        
        self.run_script("set", "performance.query_data", json.dumps(test_data))
        
        start_time = time.time()
        result = self.run_script("query", "$.performance.query_data.items[?(@.status=='active')].id")
        query_time = time.time() - start_time
        
        self.assertEqual(result.returncode, 0)
        self.assertLess(query_time, 0.2, "Query operation should complete within 200ms")
        
        # Verify query results
        data = json.loads(result.stdout)
        active_ids = data["results"]
        self.assertEqual(len(active_ids), 25)  # Half should be active


if __name__ == "__main__":
    # Create test suite with different test categories
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestStateCRUDOperations,
        TestJSONPathQueries,
        TestConcurrentAccess,
        TestSessionManagement,
        TestErrorHandling,
        TestPerformanceAndBenchmarks
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=open('test_state_manager_results.txt', 'w'))
    result = runner.run(test_suite)
    
    # Print summary to console
    print(f"\nState Manager Test Results:")
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