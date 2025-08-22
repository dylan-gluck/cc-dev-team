#!/usr/bin/env python3
"""
Comprehensive test suite for shared_state.py UV script

Tests project configuration management, epic/sprint management,
tool registry operations, team updates, and cross-session state sharing.
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


class SharedStateTestCase(unittest.TestCase):
    """Base test case with common setup for shared state tests"""
    
    def setUp(self):
        """Set up test environment with comprehensive shared state"""
        self.test_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.test_dir, "test_state.json")
        self.script_path = ".claude/scripts/shared_state.py"
        
        # Create comprehensive initial state
        self.initial_state = {
            "project": {
                "name": "test_project",
                "version": "1.0.0",
                "description": "Test project for orchestration",
                "settings": {
                    "debug": True,
                    "timeout": 30,
                    "auto_save": True
                },
                "metadata": {
                    "created": "2025-01-01T10:00:00Z",
                    "last_updated": "2025-01-01T12:00:00Z",
                    "owner": "test_team"
                }
            },
            "epics": {
                "epic_001": {
                    "id": "epic_001",
                    "title": "Core Platform Development",
                    "description": "Build the foundational platform components",
                    "status": "in_progress",
                    "priority": "high",
                    "start_date": "2025-01-01",
                    "target_date": "2025-03-01",
                    "sprints": ["sprint_001", "sprint_002"],
                    "owner": "product-director",
                    "stakeholders": ["engineering-lead", "qa-director"]
                },
                "epic_002": {
                    "id": "epic_002",
                    "title": "User Experience Enhancement",
                    "description": "Improve user interface and experience",
                    "status": "planned",
                    "priority": "medium",
                    "start_date": "2025-02-01",
                    "target_date": "2025-04-01",
                    "sprints": [],
                    "owner": "product-manager",
                    "stakeholders": ["engineering-ux", "creative-director"]
                }
            },
            "sprints": {
                "sprint_001": {
                    "id": "sprint_001",
                    "epic_id": "epic_001",
                    "title": "Foundation Setup",
                    "start_date": "2025-01-01",
                    "end_date": "2025-01-14",
                    "status": "completed",
                    "goals": ["Set up infrastructure", "Create base APIs"],
                    "velocity": 25,
                    "tasks": ["task_001", "task_002", "task_003"],
                    "team": ["engineering-lead", "engineering-fullstack", "devops-manager"]
                },
                "sprint_002": {
                    "id": "sprint_002",
                    "epic_id": "epic_001",
                    "title": "Core Features",
                    "start_date": "2025-01-15",
                    "end_date": "2025-01-28",
                    "status": "active",
                    "goals": ["Implement user management", "Add authentication"],
                    "velocity": 20,
                    "tasks": ["task_004", "task_005"],
                    "team": ["engineering-fullstack", "engineering-api", "qa-scripts"]
                }
            },
            "tools": {
                "registry": {
                    "development": {
                        "python": {
                            "version": "3.11",
                            "packages": ["fastapi", "pytest", "black"],
                            "config": {"formatter": "black", "linter": "flake8"}
                        },
                        "node": {
                            "version": "18.0.0",
                            "packages": ["react", "typescript", "jest"],
                            "config": {"bundler": "vite", "test_runner": "jest"}
                        }
                    },
                    "infrastructure": {
                        "docker": {
                            "version": "24.0",
                            "images": ["python:3.11", "node:18", "nginx:alpine"],
                            "config": {"networks": ["dev_network"], "volumes": ["app_data"]}
                        },
                        "cloud": {
                            "provider": "aws",
                            "services": ["ec2", "rds", "s3"],
                            "config": {"region": "us-west-2", "environment": "development"}
                        }
                    }
                },
                "permissions": {
                    "engineering-lead": ["all_tools"],
                    "engineering-fullstack": ["development", "testing"],
                    "devops-manager": ["infrastructure", "deployment"],
                    "qa-scripts": ["testing", "automation"]
                }
            },
            "teams": {
                "engineering": {
                    "lead": "engineering-lead",
                    "members": ["engineering-fullstack", "engineering-api", "engineering-ux"],
                    "specializations": {
                        "backend": ["engineering-fullstack", "engineering-api"],
                        "frontend": ["engineering-ux", "engineering-fullstack"],
                        "infrastructure": ["devops-manager"]
                    },
                    "capacity": 40,
                    "current_sprint": "sprint_002"
                },
                "product": {
                    "lead": "product-director",
                    "members": ["product-manager", "product-analyst"],
                    "focus_areas": ["strategy", "roadmap", "user_research"],
                    "capacity": 20,
                    "current_epic": "epic_001"
                },
                "qa": {
                    "lead": "qa-director",
                    "members": ["qa-analyst", "qa-e2e", "qa-scripts"],
                    "specializations": {
                        "automation": ["qa-scripts", "qa-e2e"],
                        "analysis": ["qa-analyst"],
                        "strategy": ["qa-director"]
                    },
                    "capacity": 25
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
        """Helper to run shared_state.py script commands"""
        cmd = ["python3", self.script_path, command, "--state-file", self.state_file] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if expect_success and result.returncode != 0:
            self.fail(f"Script failed: {result.stderr}")
        
        return result


class TestProjectConfiguration(SharedStateTestCase):
    """Test project configuration management"""
    
    def test_get_project_config(self):
        """Test retrieving project configuration"""
        result = self.run_script("get-config")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["name"], "test_project")
        self.assertEqual(data["version"], "1.0.0")
        self.assertIn("settings", data)
        self.assertIn("metadata", data)
    
    def test_get_specific_config_section(self):
        """Test retrieving specific configuration section"""
        result = self.run_script("get-config", "--section", "settings")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["debug"], True)
        self.assertEqual(data["timeout"], 30)
    
    def test_update_project_settings(self):
        """Test updating project settings"""
        new_settings = {
            "debug": False,
            "timeout": 60,
            "new_feature": True
        }
        
        result = self.run_script("update-config", "--section", "settings", 
                                "--data", json.dumps(new_settings))
        self.assertEqual(result.returncode, 0)
        
        # Verify settings were updated
        result = self.run_script("get-config", "--section", "settings")
        data = json.loads(result.stdout)
        self.assertEqual(data["debug"], False)
        self.assertEqual(data["timeout"], 60)
        self.assertEqual(data["new_feature"], True)
    
    def test_update_project_metadata(self):
        """Test updating project metadata"""
        metadata_update = {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "version_history": ["1.0.0"],
            "contributors": ["dev1", "dev2"]
        }
        
        result = self.run_script("update-config", "--section", "metadata",
                                "--data", json.dumps(metadata_update))
        self.assertEqual(result.returncode, 0)
        
        # Verify metadata was updated
        result = self.run_script("get-config", "--section", "metadata")
        data = json.loads(result.stdout)
        self.assertIn("version_history", data)
        self.assertIn("contributors", data)
    
    def test_invalid_config_section(self):
        """Test handling of invalid configuration section"""
        result = self.run_script("get-config", "--section", "nonexistent", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Section not found", result.stderr)


class TestEpicManagement(SharedStateTestCase):
    """Test epic management functionality"""
    
    def test_list_epics(self):
        """Test listing all epics"""
        result = self.run_script("list-epics")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("epics", data)
        epic_ids = [epic["id"] for epic in data["epics"]]
        self.assertIn("epic_001", epic_ids)
        self.assertIn("epic_002", epic_ids)
    
    def test_list_epics_by_status(self):
        """Test listing epics filtered by status"""
        result = self.run_script("list-epics", "--status", "in_progress")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        epics = data["epics"]
        self.assertEqual(len(epics), 1)
        self.assertEqual(epics[0]["id"], "epic_001")
        self.assertEqual(epics[0]["status"], "in_progress")
    
    def test_get_epic_details(self):
        """Test retrieving detailed epic information"""
        result = self.run_script("get-epic", "epic_001")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["id"], "epic_001")
        self.assertEqual(data["title"], "Core Platform Development")
        self.assertIn("sprints", data)
        self.assertIn("stakeholders", data)
    
    def test_update_epic_status(self):
        """Test updating epic status"""
        result = self.run_script("update-epic", "epic_002", "--status", "in_progress")
        self.assertEqual(result.returncode, 0)
        
        # Verify status was updated
        result = self.run_script("get-epic", "epic_002")
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "in_progress")
    
    def test_update_epic_details(self):
        """Test updating epic details"""
        epic_updates = {
            "priority": "high",
            "target_date": "2025-05-01",
            "stakeholders": ["engineering-lead", "qa-director", "product-director"]
        }
        
        result = self.run_script("update-epic", "epic_002", "--data", json.dumps(epic_updates))
        self.assertEqual(result.returncode, 0)
        
        # Verify updates
        result = self.run_script("get-epic", "epic_002")
        data = json.loads(result.stdout)
        self.assertEqual(data["priority"], "high")
        self.assertEqual(data["target_date"], "2025-05-01")
    
    def test_create_new_epic(self):
        """Test creating a new epic"""
        new_epic = {
            "title": "Security Enhancement",
            "description": "Improve system security and compliance",
            "priority": "high",
            "owner": "security-lead",
            "target_date": "2025-06-01"
        }
        
        result = self.run_script("create-epic", "--data", json.dumps(new_epic))
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        epic_id = data["epic_id"]
        
        # Verify epic was created
        result = self.run_script("get-epic", epic_id)
        epic_data = json.loads(result.stdout)
        self.assertEqual(epic_data["title"], "Security Enhancement")
    
    def test_epic_sprint_association(self):
        """Test associating sprints with epics"""
        result = self.run_script("add-sprint-to-epic", "epic_002", "sprint_003")
        self.assertEqual(result.returncode, 0)
        
        # Verify association
        result = self.run_script("get-epic", "epic_002")
        data = json.loads(result.stdout)
        self.assertIn("sprint_003", data["sprints"])


class TestSprintManagement(SharedStateTestCase):
    """Test sprint management functionality"""
    
    def test_list_sprints(self):
        """Test listing all sprints"""
        result = self.run_script("list-sprints")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("sprints", data)
        sprint_ids = [sprint["id"] for sprint in data["sprints"]]
        self.assertIn("sprint_001", sprint_ids)
        self.assertIn("sprint_002", sprint_ids)
    
    def test_list_sprints_by_epic(self):
        """Test listing sprints for specific epic"""
        result = self.run_script("list-sprints", "--epic", "epic_001")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        sprints = data["sprints"]
        for sprint in sprints:
            self.assertEqual(sprint["epic_id"], "epic_001")
    
    def test_list_active_sprints(self):
        """Test listing active sprints"""
        result = self.run_script("list-sprints", "--status", "active")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        active_sprints = data["sprints"]
        self.assertEqual(len(active_sprints), 1)
        self.assertEqual(active_sprints[0]["id"], "sprint_002")
    
    def test_get_sprint_details(self):
        """Test retrieving detailed sprint information"""
        result = self.run_script("get-sprint", "sprint_002")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["id"], "sprint_002")
        self.assertEqual(data["status"], "active")
        self.assertIn("goals", data)
        self.assertIn("team", data)
        self.assertIn("velocity", data)
    
    def test_update_sprint_velocity(self):
        """Test updating sprint velocity"""
        result = self.run_script("update-sprint", "sprint_002", "--velocity", "30")
        self.assertEqual(result.returncode, 0)
        
        # Verify velocity was updated
        result = self.run_script("get-sprint", "sprint_002")
        data = json.loads(result.stdout)
        self.assertEqual(data["velocity"], 30)
    
    def test_update_sprint_team(self):
        """Test updating sprint team composition"""
        new_team = ["engineering-lead", "engineering-fullstack", "qa-e2e", "devops-cicd"]
        
        result = self.run_script("update-sprint", "sprint_002", "--team", json.dumps(new_team))
        self.assertEqual(result.returncode, 0)
        
        # Verify team was updated
        result = self.run_script("get-sprint", "sprint_002")
        data = json.loads(result.stdout)
        self.assertEqual(set(data["team"]), set(new_team))
    
    def test_create_new_sprint(self):
        """Test creating a new sprint"""
        new_sprint = {
            "epic_id": "epic_001",
            "title": "Integration Testing",
            "start_date": "2025-01-29",
            "end_date": "2025-02-11",
            "goals": ["Complete integration tests", "Performance optimization"],
            "team": ["qa-e2e", "engineering-fullstack", "devops-manager"]
        }
        
        result = self.run_script("create-sprint", "--data", json.dumps(new_sprint))
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        sprint_id = data["sprint_id"]
        
        # Verify sprint was created
        result = self.run_script("get-sprint", sprint_id)
        sprint_data = json.loads(result.stdout)
        self.assertEqual(sprint_data["title"], "Integration Testing")
    
    def test_sprint_metrics_calculation(self):
        """Test sprint metrics and analytics"""
        result = self.run_script("get-sprint-metrics", "sprint_001")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("completion_rate", data)
        self.assertIn("velocity_trend", data)
        self.assertIn("team_utilization", data)


class TestToolRegistry(SharedStateTestCase):
    """Test tool registry management"""
    
    def test_list_tool_categories(self):
        """Test listing tool registry categories"""
        result = self.run_script("list-tools")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("categories", data)
        categories = data["categories"]
        self.assertIn("development", categories)
        self.assertIn("infrastructure", categories)
    
    def test_get_category_tools(self):
        """Test retrieving tools for specific category"""
        result = self.run_script("get-tools", "--category", "development")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        tools = data["tools"]
        self.assertIn("python", tools)
        self.assertIn("node", tools)
    
    def test_get_specific_tool_config(self):
        """Test retrieving specific tool configuration"""
        result = self.run_script("get-tool", "--category", "development", "--tool", "python")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "3.11")
        self.assertIn("packages", data)
        self.assertIn("config", data)
    
    def test_update_tool_config(self):
        """Test updating tool configuration"""
        updated_config = {
            "version": "3.12",
            "packages": ["fastapi", "pytest", "black", "mypy"],
            "config": {"formatter": "black", "linter": "ruff", "type_checker": "mypy"}
        }
        
        result = self.run_script("update-tool", "--category", "development", 
                                "--tool", "python", "--config", json.dumps(updated_config))
        self.assertEqual(result.returncode, 0)
        
        # Verify update
        result = self.run_script("get-tool", "--category", "development", "--tool", "python")
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "3.12")
        self.assertIn("mypy", data["packages"])
    
    def test_add_new_tool(self):
        """Test adding new tool to registry"""
        new_tool_config = {
            "version": "1.8.0",
            "features": ["testing", "coverage", "reporting"],
            "config": {"output_format": "json", "coverage_threshold": 80}
        }
        
        result = self.run_script("add-tool", "--category", "development",
                                "--tool", "coverage_tool", "--config", json.dumps(new_tool_config))
        self.assertEqual(result.returncode, 0)
        
        # Verify tool was added
        result = self.run_script("get-tool", "--category", "development", "--tool", "coverage_tool")
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "1.8.0")
    
    def test_tool_permissions(self):
        """Test tool access permissions"""
        result = self.run_script("get-tool-permissions", "--agent", "engineering-fullstack")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        permissions = data["permissions"]
        self.assertIn("development", permissions)
        self.assertIn("testing", permissions)
    
    def test_update_tool_permissions(self):
        """Test updating tool permissions for agents"""
        new_permissions = ["development", "testing", "deployment"]
        
        result = self.run_script("update-permissions", "--agent", "engineering-fullstack",
                                "--permissions", json.dumps(new_permissions))
        self.assertEqual(result.returncode, 0)
        
        # Verify permissions update
        result = self.run_script("get-tool-permissions", "--agent", "engineering-fullstack")
        data = json.loads(result.stdout)
        self.assertEqual(set(data["permissions"]), set(new_permissions))


class TestTeamManagement(SharedStateTestCase):
    """Test team configuration and updates"""
    
    def test_list_teams(self):
        """Test listing all teams"""
        result = self.run_script("list-teams")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        teams = data["teams"]
        team_names = [team["name"] for team in teams]
        self.assertIn("engineering", team_names)
        self.assertIn("product", team_names)
        self.assertIn("qa", team_names)
    
    def test_get_team_details(self):
        """Test retrieving detailed team information"""
        result = self.run_script("get-team", "engineering")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertEqual(data["lead"], "engineering-lead")
        self.assertIn("members", data)
        self.assertIn("specializations", data)
        self.assertIn("capacity", data)
    
    def test_update_team_members(self):
        """Test updating team membership"""
        new_members = ["engineering-fullstack", "engineering-api", "engineering-ux", "engineering-mobile"]
        
        result = self.run_script("update-team", "engineering", "--members", json.dumps(new_members))
        self.assertEqual(result.returncode, 0)
        
        # Verify members were updated
        result = self.run_script("get-team", "engineering")
        data = json.loads(result.stdout)
        self.assertEqual(set(data["members"]), set(new_members))
    
    def test_update_team_capacity(self):
        """Test updating team capacity"""
        result = self.run_script("update-team", "engineering", "--capacity", "50")
        self.assertEqual(result.returncode, 0)
        
        # Verify capacity update
        result = self.run_script("get-team", "engineering")
        data = json.loads(result.stdout)
        self.assertEqual(data["capacity"], 50)
    
    def test_update_team_specializations(self):
        """Test updating team specializations"""
        new_specializations = {
            "backend": ["engineering-fullstack", "engineering-api"],
            "frontend": ["engineering-ux", "engineering-fullstack"],
            "mobile": ["engineering-mobile"],
            "infrastructure": ["devops-manager", "devops-infrastructure"]
        }
        
        result = self.run_script("update-team", "engineering", 
                                "--specializations", json.dumps(new_specializations))
        self.assertEqual(result.returncode, 0)
        
        # Verify specializations update
        result = self.run_script("get-team", "engineering")
        data = json.loads(result.stdout)
        self.assertIn("mobile", data["specializations"])
    
    def test_add_new_team(self):
        """Test adding a new team"""
        new_team = {
            "lead": "security-lead",
            "members": ["security-analyst", "security-engineer"],
            "focus_areas": ["vulnerability_assessment", "compliance", "incident_response"],
            "capacity": 15
        }
        
        result = self.run_script("create-team", "security", "--data", json.dumps(new_team))
        self.assertEqual(result.returncode, 0)
        
        # Verify team was created
        result = self.run_script("get-team", "security")
        data = json.loads(result.stdout)
        self.assertEqual(data["lead"], "security-lead")
    
    def test_team_workload_analysis(self):
        """Test team workload and capacity analysis"""
        result = self.run_script("analyze-team-workload", "engineering")
        self.assertEqual(result.returncode, 0)
        
        data = json.loads(result.stdout)
        self.assertIn("utilization_rate", data)
        self.assertIn("current_assignments", data)
        self.assertIn("available_capacity", data)


class TestCrossSessionStateSharing(SharedStateTestCase):
    """Test cross-session state sharing functionality"""
    
    def test_state_synchronization(self):
        """Test state synchronization across operations"""
        # Simulate concurrent state access
        result1 = self.run_script("get-config", "--section", "settings")
        result2 = self.run_script("list-epics", "--status", "in_progress")
        
        self.assertEqual(result1.returncode, 0)
        self.assertEqual(result2.returncode, 0)
        
        # Both operations should succeed and return consistent data
        config_data = json.loads(result1.stdout)
        epic_data = json.loads(result2.stdout)
        
        self.assertIn("debug", config_data)
        self.assertIn("epics", epic_data)
    
    def test_atomic_state_updates(self):
        """Test atomic state updates prevent corruption"""
        # Perform multiple updates in sequence
        updates = [
            ("update-config", ["--section", "settings", "--data", '{"debug": false}']),
            ("update-epic", ["epic_001", "--status", "completed"]),
            ("update-sprint", ["sprint_002", "--velocity", "35"])
        ]
        
        results = []
        for command, args in updates:
            result = self.run_script(command, *args)
            results.append(result.returncode)
        
        # All updates should succeed
        self.assertTrue(all(r == 0 for r in results))
        
        # Verify final state consistency
        result = self.run_script("get-config", "--section", "settings")
        config_data = json.loads(result.stdout)
        self.assertEqual(config_data["debug"], False)
    
    def test_concurrent_team_updates(self):
        """Test concurrent team updates"""
        def update_team_capacity(team, capacity):
            return self.run_script("update-team", team, "--capacity", str(capacity))
        
        # Update multiple teams concurrently
        import threading
        results = []
        
        def worker(team, capacity):
            result = update_team_capacity(team, capacity)
            results.append(result.returncode)
        
        threads = [
            threading.Thread(target=worker, args=("engineering", 45)),
            threading.Thread(target=worker, args=("product", 25)),
            threading.Thread(target=worker, args=("qa", 30))
        ]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All updates should succeed
        self.assertTrue(all(r == 0 for r in results))


class TestStateValidationAndErrorHandling(SharedStateTestCase):
    """Test state validation and error handling"""
    
    def test_invalid_epic_id(self):
        """Test handling of invalid epic ID"""
        result = self.run_script("get-epic", "nonexistent_epic", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Epic not found", result.stderr)
    
    def test_invalid_team_name(self):
        """Test handling of invalid team name"""
        result = self.run_script("get-team", "nonexistent_team", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Team not found", result.stderr)
    
    def test_invalid_json_data(self):
        """Test handling of invalid JSON data"""
        result = self.run_script("update-config", "--section", "settings",
                                "--data", "{invalid json}", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid JSON", result.stderr)
    
    def test_missing_required_parameters(self):
        """Test handling of missing required parameters"""
        # Missing epic ID
        result = self.run_script("get-epic", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        
        # Missing data for update
        result = self.run_script("update-epic", "epic_001", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
    
    def test_state_file_corruption_recovery(self):
        """Test recovery from state file corruption"""
        # Corrupt the state file
        with open(self.state_file, 'w') as f:
            f.write("{ corrupted json content }")
        
        result = self.run_script("get-config", expect_success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Failed to parse state", result.stderr)


if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestProjectConfiguration,
        TestEpicManagement,
        TestSprintManagement,
        TestToolRegistry,
        TestTeamManagement,
        TestCrossSessionStateSharing,
        TestStateValidationAndErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=open('test_shared_state_results.txt', 'w'))
    result = runner.run(test_suite)
    
    # Print summary to console
    print(f"\nShared State Test Results:")
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