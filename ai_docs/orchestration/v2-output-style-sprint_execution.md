# Sprint Execution Output Style Program

## System Identity

**Program Name**: `sprint_execution`  
**Purpose**: Real-time development workflow management and sprint coordination interface  
**Execution Context**: Operational-level orchestration focused on delivery and execution  
**Update Frequency**: High-frequency updates with task-level granularity (every 30 seconds)

## System Prompt/Instructions

```
You are the Sprint Execution Interface, the operational command center for managing active development sprints and delivery workflows.

CORE BEHAVIORS:
- Monitor and coordinate all active development work in real-time
- Provide tactical guidance for sprint execution and workflow optimization
- Facilitate agile ceremonies and sprint management activities
- Track progress against sprint goals and delivery commitments
- Identify and resolve blockers, dependencies, and workflow bottlenecks
- Enable rapid task assignment, status updates, and team coordination

EXECUTION FOCUS:
- Sprint goals and commitment tracking
- Task-level visibility and progress monitoring
- Workflow efficiency and throughput optimization
- Quality gates and definition-of-done enforcement
- Team velocity and capacity management
- Blocker identification and rapid resolution

INTERACTION MODEL:
- Real-time workflow visualization and updates
- Sprint ceremony facilitation (standups, reviews, retrospectives)
- Drag-and-drop task management and assignment
- Quick actions for common sprint operations
- Integrated communication for team coordination
- Automated workflow triggers and notifications

AGILE INTEGRATION:
- Sprint planning and backlog management
- User story and task breakdown
- Estimation and velocity tracking
- Burndown charts and progress visualization
- Retrospective insights and process improvement
- Continuous integration and deployment pipeline status
```

## Visual Layout Design

### Main Sprint Execution Interface

```
╭─ SPRINT EXECUTION: Alpha-2024.3 ─────────────────────────────────────── [Day 8 of 14] ─╮
│ Sprint Goal: Deliver enterprise auth platform MVP  │ Confidence: 78% │ Velocity: 34/40 │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ SPRINT PROGRESS                                                                          │
│ ┌─ Burndown Chart ─────────────────────────────────────────────────────────────────────┐ │
│ │ Story Points │                                                                       │ │
│ │     40 ├─●                                 Ideal ↘                                  │ │
│ │     35 │  ●●                                                                        │ │
│ │     30 │    ●●                                                                      │ │
│ │     25 │      ●●                       Actual ↘                                    │ │
│ │     20 │        ●                                                                   │ │
│ │     15 │         ●●                                                                 │ │
│ │     10 │           ●●                                                               │ │
│ │      5 │             ●                                                              │ │
│ │      0 └─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬───│ │
│ │              D1    D3    D5    D7    D9   D11   D13   D15                         │ │
│ │ Remaining: 15 SP │ On Track: ✓ │ Risk: Medium │ Completion Est: Day 13           │ │
│ └──────────────────────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ ACTIVE WORK BOARD                                                                        │
│ ┌─ TODO (5) ──────────────┐ ┌─ IN PROGRESS (8) ────────┐ ┌─ REVIEW (3) ──┐ ┌─ DONE (12) ─┐ │
│ │ [AUTH-023] JWT refresh  │ │ [AUTH-019] User mgmt API │ │ [AUTH-015] SSO │ │ [AUTH-001]  │ │
│ │ 🔴 BLOCKED              │ │ @maya 📊 75% Day 2       │ │ @alex Ready    │ │ [AUTH-002]  │ │
│ │ Waiting: Security audit │ │ Est: Tomorrow            │ │ [AUTH-017] DB  │ │ [AUTH-003]  │ │
│ │                         │ │                          │ │ @sam Review    │ │ [AUTH-004]  │ │
│ │ [AUTH-024] Mobile SDK   │ │ [AUTH-020] Frontend comp │ │ [AUTH-018] API │ │ [AUTH-005]  │ │
│ │ 🟡 READY                │ │ @jordan 📊 45% Day 1     │ │ @maya Review   │ │ [AUTH-006]  │ │
│ │ 8 SP │ Assigned: @alex   │ │ Est: Day 10              │ │                │ │ ...and 6 more │ │
│ │                         │ │                          │ │                │ │              │ │
│ │ [AUTH-025] Error handling│ │ [AUTH-021] Integration   │ │                │ │              │ │
│ │ 🟢 READY                │ │ @alex 📊 30% Day 1       │ │                │ │              │ │
│ │ 5 SP │ Priority: High    │ │ Dependencies: AUTH-019   │ │                │ │              │ │
│ │                         │ │                          │ │                │ │              │ │
│ │ [AUTH-026] Documentation│ │ [AUTH-022] Test suite    │ │                │ │              │ │
│ │ 🟢 READY                │ │ @taylor 📊 60% Day 3     │ │                │ │              │ │
│ │ 3 SP │ Can start anytime │ │ Coverage: 78%            │ │                │ │              │ │
│ └─────────────────────────┘ └──────────────────────────┘ └────────────────┘ └──────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ TEAM STATUS & CAPACITY                                                                   │
│ @maya [●●●●●] 100% │ Current: AUTH-019 User mgmt │ Next: AUTH-023 (blocked) │ Available: -- │
│ @alex [●●●○○]  75% │ Current: AUTH-021 Integration │ Next: AUTH-024 Mobile │ Available: Day 10 │
│ @sam  [●●●●○]  85% │ Current: Code reviews │ Next: AUTH-025 Errors │ Available: Day 9    │
│ @jordan [●●●●●] 100% │ Current: AUTH-020 Frontend │ Next: AUTH-026 Docs │ Available: --     │
│ @taylor [●●●○○]  70% │ Current: AUTH-022 Testing │ Next: Available │ Available: Day 9     │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ BLOCKERS & ALERTS                                                                        │
│ 🔴 CRITICAL: [AUTH-023] JWT refresh blocked - Security audit required (Day 3)           │
│ 🟡 WARNING: [AUTH-020] Frontend comp - Design tokens delayed, using placeholder         │
│ 🔵 INFO: [AUTH-022] Test coverage at 78% - Target 85% before sprint end                 │
│ 🟢 RESOLVED: [AUTH-019] Database schema - Performance testing completed successfully     │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ QUICK ACTIONS                                                                            │
│ [📋 Add Task] [👥 Assign Work] [🔄 Update Status] [🚫 Block/Unblock] [📊 Sprint Stats] │
│ [🎯 Daily Standup] [🔍 Review Queue] [⚡ Quick Deploy] [📈 Velocity Report]              │
╰──────────────────────────────────────────────────────────────────────────────────────────╯

> Type command, drag tasks, or [click] action above                        Last sync: 14:23:45
```

### Daily Standup Interface

```
╭─ DAILY STANDUP: Sprint Alpha-2024.3 ─────────────────────────────── [Day 8 - Mar 15] ─╮
│ Facilitator: @alex (Scrum Master) │ Attendees: 5/5 │ Duration: 12m │ Next: Tomorrow 9AM │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ STANDUP PROGRESS                                                                         │
│                                                                                          │
│ 👤 @maya [COMPLETE] ────────────────────────────────────────────────────────────────────│
│ │ ✅ YESTERDAY: Finished user management API endpoints (AUTH-019)                       │
│ │    • All CRUD operations working                                                      │
│ │    • Performance testing passed (avg 45ms response time)                             │
│ │    • Code review completed by @sam                                                    │
│ │                                                                                        │
│ │ 🎯 TODAY: Start JWT refresh token implementation (AUTH-023)                           │
│ │    • BLOCKED: Waiting for security audit completion                                   │
│ │    • Alternative: Can work on AUTH-024 Mobile SDK preparation                        │
│ │                                                                                        │
│ │ 🚫 BLOCKERS: Security team audit for JWT implementation (Day 3)                       │
│ │    • Escalated to @alex                                                               │
│ │    • Expected resolution: Today EOD                                                   │
│ └────────────────────────────────────────────────────────────────────────────────────────│
│                                                                                          │
│ 👤 @alex [IN PROGRESS] ─────────────────────────────────────────────────────────────────│
│ │ ✅ YESTERDAY: Integration testing framework setup (AUTH-021)                          │
│ │    • Test environment configured                                                      │
│ │    • Mock services implemented                                                        │
│ │    • 30% of integration tests written                                                 │
│ │                                                                                        │
│ │ 🎯 TODAY: Complete integration testing, resolve @maya's blocker                       │
│ │    • Finish remaining integration test cases                                          │
│ │    • Contact security team about AUTH-023 audit                                      │
│ │    • Code review for @jordan's frontend work                                          │
│ │                                                                                        │
│ │ 🚫 BLOCKERS: None                                                                      │
│ └────────────────────────────────────────────────────────────────────────────────────────│
│                                                                                          │
│ 👤 @jordan [IN PROGRESS] ───────────────────────────────────────────────────────────────│
│ │ ✅ YESTERDAY: Frontend authentication components (AUTH-020)                           │
│ │    • Login form component completed                                                   │
│ │    • Using placeholder design tokens (creative team delayed)                         │
│ │    • Unit tests at 85% coverage                                                       │
│ │                                                                                        │
│ │ 🎯 TODAY: Finish auth components, integrate with backend API                          │
│ │    • Complete registration and password reset forms                                   │
│ │    • Connect to @maya's user management API                                           │
│ │    • Update tests for API integration                                                 │
│ │                                                                                        │
│ │ 🚫 BLOCKERS: Design tokens still pending from creative team                           │
│ │    • Workaround: Using Material Design defaults                                       │
│ │    • Can update tokens when available                                                 │
│ └────────────────────────────────────────────────────────────────────────────────────────│
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ STANDUP INSIGHTS                                                                         │
│ Sprint Health: 🟡 GOOD (Minor blockers) │ Velocity: On Track │ Morale: High (4.2/5)     │
│ Action Items:                                                                            │
│ • @alex: Contact security team about AUTH-023 audit (Priority: High, Due: Today)       │
│ • @alex: Follow up with creative team on design tokens (Priority: Medium, Due: Tomorrow)│
│ • @sam: Prepare code review for AUTH-020 frontend work (Priority: Medium, Due: Today)   │
│                                                                                          │
│ Sprint Risks Identified:                                                                 │
│ • Security audit delay could impact sprint goal (Mitigation: Alternative work planned)  │
│ • Design token dependency creates technical debt (Mitigation: Refactor plan prepared)   │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

### Sprint Review Interface

```
╭─ SPRINT REVIEW: Alpha-2024.3 ────────────────────────────────────── [Day 14 - COMPLETE] ─╮
│ Demo: Enterprise Auth Platform MVP │ Stakeholders: 8 │ Feedback Score: 4.3/5 │ Duration: 45m │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ SPRINT ACHIEVEMENTS                                                                      │
│ ┌─ Sprint Goal Assessment ─────────────────────────────────────────────────────────────┐ │
│ │ 🎯 Goal: Deliver enterprise auth platform MVP                                        │ │
│ │ ✅ ACHIEVED: 95% complete (38/40 story points delivered)                             │ │
│ │ ├─ User authentication system ✅ Complete                                             │ │
│ │ ├─ JWT token management ✅ Complete                                                   │ │
│ │ ├─ API integration layer ✅ Complete                                                  │ │
│ │ ├─ Frontend components ✅ Complete (pending design token update)                     │ │
│ │ ├─ Security audit ✅ Passed                                                          │ │
│ │ ├─ Integration testing ✅ Complete (92% coverage)                                    │ │
│ │ ├─ Documentation ⏳ 80% complete (carries to next sprint)                            │ │
│ │ └─ Mobile SDK preparation ⏳ 60% complete (carries to next sprint)                   │ │
│ └──────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│ ┌─ Demonstration Results ──────────────────────────────────────────────────────────────┐ │
│ │ Demo Flow: User registration → Login → JWT refresh → API access → Dashboard          │ │
│ │                                                                                        │ │
│ │ Stakeholder Feedback:                                                                  │ │
│ │ • Product Manager: "Excellent user experience, smooth authentication flow" (5/5)     │ │
│ │ • Security Lead: "Robust implementation, passes all security requirements" (4/5)     │ │
│ │ • UI/UX Designer: "Functional but needs design token integration" (3/5)              │ │
│ │ • Customer Success: "Ready for pilot customer deployment" (5/5)                      │ │
│ │ • Engineering Manager: "Solid technical foundation, good test coverage" (4/5)        │ │
│ │                                                                                        │ │
│ │ Key Success Metrics:                                                                   │ │
│ │ • Authentication response time: <50ms (Target: <100ms) ✅ EXCEEDED                   │ │
│ │ • Security compliance: 100% (Target: 100%) ✅ MET                                    │ │
│ │ • Test coverage: 92% (Target: 85%) ✅ EXCEEDED                                       │ │
│ │ • User experience score: 4.3/5 (Target: 4.0/5) ✅ EXCEEDED                          │ │
│ └──────────────────────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ VELOCITY & METRICS                                                                       │
│ Sprint Velocity: 38 SP │ Team Velocity Avg: 35 SP │ Velocity Trend: ↗ +8.6%            │
│ Burndown: Completed Day 13 (1 day early) │ Estimation Accuracy: 94% │ Quality: High      │
│                                                                                          │
│ Individual Contributions:                                                                │
│ • @maya: 12 SP (User management, JWT implementation) - Excellent technical delivery     │ │
│ • @alex: 10 SP (Integration, leadership) - Strong coordination and problem solving      │ │
│ • @jordan: 8 SP (Frontend components) - Good progress despite design dependencies       │ │
│ • @sam: 6 SP (Code reviews, testing) - Thorough quality assurance                       │ │
│ • @taylor: 4 SP (Test automation) - Solid testing infrastructure improvements           │ │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ RETROSPECTIVE PREVIEW                                                                    │
│ What Went Well:                                                                          │
│ • Excellent team collaboration and communication                                         │ │
│ • Proactive blocker resolution (security audit)                                         │ │
│ • High quality delivery with strong test coverage                                        │ │
│ • Early completion despite mid-sprint challenges                                         │ │
│                                                                                          │
│ What Could Improve:                                                                      │ │
│ • Better dependency coordination with creative team                                      │ │
│ • Earlier security audit scheduling                                                      │ │
│ • More accurate initial story point estimation                                           │ │
│                                                                                          │
│ Action Items for Next Sprint:                                                            │ │
│ • Complete remaining documentation (AUTH-026)                                            │ │
│ • Finish mobile SDK preparation (AUTH-024)                                              │ │
│ • Integrate final design tokens from creative team                                       │ │
│ • Plan pilot customer deployment                                                         │ │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command Interpreter Design

### Sprint Command Processing

```python
class SprintCommandProcessor:
    def __init__(self):
        self.sprint_manager = SprintManager()
        self.task_manager = TaskManager()
        self.team_manager = TeamManager()
        self.workflow_engine = WorkflowEngine()
        
    def process_command(self, command: str, context: dict) -> dict:
        """Process sprint execution commands"""
        
        if command.startswith("/task"):
            return self.handle_task_command(command, context)
        elif command.startswith("/assign"):
            return self.handle_assignment_command(command, context)
        elif command.startswith("/status"):
            return self.handle_status_command(command, context)
        elif command.startswith("/sprint"):
            return self.handle_sprint_command(command, context)
        elif command.startswith("/standup"):
            return self.handle_standup_command(command, context)
        elif command.startswith("/review"):
            return self.handle_review_command(command, context)
        elif command.startswith("/block"):
            return self.handle_blocker_command(command, context)
        else:
            return self.handle_workflow_command(command, context)
    
    def handle_task_command(self, command: str, context: dict) -> dict:
        """Handle task-related operations"""
        
        # Parse task command
        parts = command.split()
        action = parts[1] if len(parts) > 1 else "list"
        
        task_commands = {
            "create": self.create_task,
            "update": self.update_task,
            "move": self.move_task,
            "assign": self.assign_task,
            "estimate": self.estimate_task,
            "block": self.block_task,
            "unblock": self.unblock_task,
            "comment": self.add_task_comment,
            "history": self.get_task_history,
            "dependencies": self.manage_task_dependencies
        }
        
        if action in task_commands:
            return task_commands[action](parts[2:], context)
        else:
            return {"error": f"Unknown task action: {action}"}
    
    def handle_assignment_command(self, command: str, context: dict) -> dict:
        """Handle work assignment operations"""
        
        # Examples:
        # /assign AUTH-023 @maya
        # /assign @alex next-available
        # /assign team-capacity
        
        parts = command.split()
        
        if len(parts) >= 3:
            task_id = parts[1]
            assignee = parts[2]
            
            if task_id.startswith("@"):
                # Assigning to person
                return self.assign_work_to_person(task_id[1:], assignee, context)
            else:
                # Assigning task to person
                return self.assign_task_to_person(task_id, assignee[1:], context)
        
        elif "capacity" in command:
            return self.show_team_capacity(context)
        
        elif "next-available" in command:
            return self.assign_next_available_work(parts[1][1:], context)
        
        else:
            return {"error": "Invalid assignment command format"}
    
    def handle_status_command(self, command: str, context: dict) -> dict:
        """Handle status update operations"""
        
        # Examples:
        # /status AUTH-023 in-progress
        # /status @maya available
        # /status sprint
        # /status blockers
        
        parts = command.split()
        
        if len(parts) >= 3:
            target = parts[1]
            new_status = parts[2]
            
            if target.startswith("@"):
                # Person status update
                return self.update_person_status(target[1:], new_status, context)
            else:
                # Task status update
                return self.update_task_status(target, new_status, context)
        
        elif "sprint" in command:
            return self.get_sprint_status(context)
        
        elif "blockers" in command:
            return self.get_blocker_status(context)
        
        else:
            return {"error": "Invalid status command format"}
```

### Workflow Automation Engine

```python
class WorkflowEngine:
    def __init__(self):
        self.automation_rules = AutomationRuleEngine()
        self.notification_manager = NotificationManager()
        self.integration_manager = IntegrationManager()
        
    def process_workflow_event(self, event: dict, context: dict) -> dict:
        """Process workflow events and trigger automations"""
        
        workflow_response = {
            "automations_triggered": [],
            "notifications_sent": [],
            "integrations_updated": [],
            "next_actions": []
        }
        
        # Task status change automation
        if event["type"] == "task_status_change":
            automations = self.handle_task_status_change(event, context)
            workflow_response["automations_triggered"].extend(automations)
        
        # Sprint milestone automation
        elif event["type"] == "sprint_milestone":
            automations = self.handle_sprint_milestone(event, context)
            workflow_response["automations_triggered"].extend(automations)
        
        # Blocker detection automation
        elif event["type"] == "blocker_detected":
            automations = self.handle_blocker_detection(event, context)
            workflow_response["automations_triggered"].extend(automations)
        
        # Team capacity change automation
        elif event["type"] == "capacity_change":
            automations = self.handle_capacity_change(event, context)
            workflow_response["automations_triggered"].extend(automations)
        
        # Generate notifications
        notifications = self.generate_workflow_notifications(event, workflow_response)
        workflow_response["notifications_sent"] = notifications
        
        # Update external integrations
        integrations = self.update_external_integrations(event, context)
        workflow_response["integrations_updated"] = integrations
        
        # Suggest next actions
        next_actions = self.suggest_next_actions(event, context)
        workflow_response["next_actions"] = next_actions
        
        return workflow_response
    
    def handle_task_status_change(self, event: dict, context: dict) -> list:
        """Handle task status change automations"""
        
        automations = []
        task = event["task"]
        old_status = event["old_status"]
        new_status = event["new_status"]
        
        # Task moved to "In Progress"
        if new_status == "in_progress":
            automations.extend([
                {"type": "assign_reviewer", "task_id": task["id"]},
                {"type": "start_time_tracking", "task_id": task["id"]},
                {"type": "update_sprint_board", "task_id": task["id"]}
            ])
        
        # Task moved to "Review"
        elif new_status == "review":
            automations.extend([
                {"type": "notify_reviewers", "task_id": task["id"]},
                {"type": "create_review_checklist", "task_id": task["id"]},
                {"type": "update_quality_metrics", "task_id": task["id"]}
            ])
        
        # Task moved to "Done"
        elif new_status == "done":
            automations.extend([
                {"type": "update_velocity_metrics", "task_id": task["id"]},
                {"type": "check_sprint_progress", "task_id": task["id"]},
                {"type": "auto_assign_next_task", "assignee": task["assignee"]},
                {"type": "update_burndown_chart", "task_id": task["id"]}
            ])
        
        # Task blocked
        elif new_status == "blocked":
            automations.extend([
                {"type": "escalate_blocker", "task_id": task["id"]},
                {"type": "find_alternative_work", "assignee": task["assignee"]},
                {"type": "update_risk_assessment", "task_id": task["id"]}
            ])
        
        return automations
    
    def suggest_next_actions(self, event: dict, context: dict) -> list:
        """Suggest contextual next actions based on workflow state"""
        
        suggestions = []
        
        # Analyze current sprint state
        sprint_state = self.analyze_sprint_state(context)
        
        # Sprint progress suggestions
        if sprint_state["days_remaining"] <= 3 and sprint_state["completion_rate"] < 0.8:
            suggestions.append({
                "priority": "high",
                "action": "Consider scope reduction or sprint extension",
                "rationale": "Sprint completion at risk",
                "command": "/sprint analyze-completion-risk"
            })
        
        # Team capacity suggestions
        if sprint_state["team_utilization"] < 0.7:
            suggestions.append({
                "priority": "medium",
                "action": "Assign additional work to available team members",
                "rationale": "Team has available capacity",
                "command": "/assign team-capacity"
            })
        
        # Quality suggestions
        if sprint_state["test_coverage"] < 0.85:
            suggestions.append({
                "priority": "medium",
                "action": "Improve test coverage before sprint completion",
                "rationale": "Test coverage below target",
                "command": "/task create type:testing priority:medium"
            })
        
        # Blocker resolution suggestions
        active_blockers = sprint_state.get("active_blockers", [])
        if active_blockers:
            suggestions.append({
                "priority": "high",
                "action": f"Resolve {len(active_blockers)} active blockers",
                "rationale": "Blockers impacting sprint progress",
                "command": "/block resolve-all"
            })
        
        return suggestions
```

## State Integration Points

### Sprint State Management

```python
class SprintStateManager:
    def __init__(self):
        self.task_tracker = TaskTracker()
        self.velocity_calculator = VelocityCalculator()
        self.burndown_generator = BurndownGenerator()
        self.capacity_analyzer = CapacityAnalyzer()
        
    def get_sprint_state(self, sprint_id: str) -> dict:
        """Get comprehensive sprint state"""
        
        return {
            "sprint_info": self.get_sprint_info(sprint_id),
            "progress_metrics": self.get_progress_metrics(sprint_id),
            "team_status": self.get_team_status(sprint_id),
            "task_board": self.get_task_board_state(sprint_id),
            "blockers": self.get_active_blockers(sprint_id),
            "quality_metrics": self.get_quality_metrics(sprint_id),
            "velocity_data": self.get_velocity_data(sprint_id),
            "burndown_data": self.get_burndown_data(sprint_id)
        }
    
    def get_sprint_info(self, sprint_id: str) -> dict:
        """Basic sprint information"""
        return {
            "id": sprint_id,
            "name": "Alpha-2024.3",
            "goal": "Deliver enterprise auth platform MVP",
            "start_date": "2024-03-04",
            "end_date": "2024-03-18",
            "current_day": 8,
            "total_days": 14,
            "days_remaining": 6,
            "confidence_level": 0.78,
            "risk_level": "medium"
        }
    
    def get_progress_metrics(self, sprint_id: str) -> dict:
        """Sprint progress and completion metrics"""
        return {
            "story_points": {
                "committed": 40,
                "completed": 25,
                "remaining": 15,
                "completion_rate": 0.625
            },
            "tasks": {
                "total": 28,
                "todo": 5,
                "in_progress": 8,
                "review": 3,
                "done": 12
            },
            "burndown": {
                "ideal_remaining": 18,
                "actual_remaining": 15,
                "trend": "ahead_of_schedule",
                "projected_completion": "day_13"
            },
            "velocity": {
                "current_sprint": 34,
                "average": 31,
                "trend": "increasing"
            }
        }
    
    def get_team_status(self, sprint_id: str) -> dict:
        """Current team member status and capacity"""
        return {
            "maya": {
                "status": "active",
                "current_task": "AUTH-019",
                "utilization": 1.0,
                "availability": "fully_booked",
                "next_available": None,
                "velocity_this_sprint": 12,
                "blockers": ["AUTH-023"]
            },
            "alex": {
                "status": "active",
                "current_task": "AUTH-021",
                "utilization": 0.75,
                "availability": "some_capacity",
                "next_available": "day_10",
                "velocity_this_sprint": 10,
                "blockers": []
            },
            "sam": {
                "status": "active",
                "current_task": "code_reviews",
                "utilization": 0.85,
                "availability": "some_capacity",
                "next_available": "day_9",
                "velocity_this_sprint": 6,
                "blockers": []
            },
            "jordan": {
                "status": "active",
                "current_task": "AUTH-020",
                "utilization": 1.0,
                "availability": "fully_booked",
                "next_available": None,
                "velocity_this_sprint": 8,
                "blockers": ["design_tokens"]
            },
            "taylor": {
                "status": "active",
                "current_task": "AUTH-022",
                "utilization": 0.70,
                "availability": "available",
                "next_available": "day_9",
                "velocity_this_sprint": 4,
                "blockers": []
            }
        }
    
    def get_task_board_state(self, sprint_id: str) -> dict:
        """Current state of the sprint task board"""
        return {
            "columns": {
                "todo": {
                    "count": 5,
                    "story_points": 16,
                    "tasks": [
                        {
                            "id": "AUTH-023",
                            "title": "JWT refresh token implementation",
                            "story_points": 5,
                            "priority": "high",
                            "assignee": None,
                            "status": "blocked",
                            "blocker": "Security audit required",
                            "dependencies": []
                        },
                        {
                            "id": "AUTH-024",
                            "title": "Mobile SDK preparation",
                            "story_points": 8,
                            "priority": "medium",
                            "assignee": "alex",
                            "status": "ready",
                            "dependencies": ["AUTH-019"]
                        }
                        # ... more tasks
                    ]
                },
                "in_progress": {
                    "count": 8,
                    "story_points": 22,
                    "tasks": [
                        {
                            "id": "AUTH-019",
                            "title": "User management API",
                            "story_points": 5,
                            "assignee": "maya",
                            "progress": 0.75,
                            "days_in_progress": 2,
                            "estimated_completion": "tomorrow"
                        }
                        # ... more tasks
                    ]
                },
                "review": {
                    "count": 3,
                    "story_points": 8,
                    "tasks": [
                        {
                            "id": "AUTH-015",
                            "title": "SSO integration",
                            "story_points": 3,
                            "assignee": "alex",
                            "reviewer": "sam",
                            "review_status": "ready",
                            "days_in_review": 1
                        }
                        # ... more tasks
                    ]
                },
                "done": {
                    "count": 12,
                    "story_points": 25,
                    "tasks": [
                        # Completed tasks...
                    ]
                }
            }
        }
```

### Real-Time Updates and Synchronization

```python
class RealTimeUpdateManager:
    def __init__(self):
        self.websocket_manager = WebSocketManager()
        self.event_stream = EventStreamProcessor()
        self.state_synchronizer = StateSynchronizer()
        
    async def start_real_time_updates(self, sprint_id: str):
        """Start real-time update stream for sprint execution"""
        
        # Subscribe to relevant event streams
        event_streams = [
            f"sprint.{sprint_id}.tasks",
            f"sprint.{sprint_id}.team",
            f"sprint.{sprint_id}.progress",
            f"sprint.{sprint_id}.blockers"
        ]
        
        for stream in event_streams:
            await self.event_stream.subscribe(stream, self.handle_sprint_event)
    
    async def handle_sprint_event(self, event: dict):
        """Handle real-time sprint events and update interface"""
        
        update_payload = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event["type"],
            "affected_areas": [],
            "updates": {}
        }
        
        if event["type"] == "task_status_change":
            update_payload["affected_areas"].extend(["task_board", "progress_metrics"])
            update_payload["updates"] = {
                "task_board": await self.get_updated_task_board_section(event["task_id"]),
                "progress_metrics": await self.get_updated_progress_metrics(event["sprint_id"])
            }
        
        elif event["type"] == "team_member_status_change":
            update_payload["affected_areas"].extend(["team_status", "capacity"])
            update_payload["updates"] = {
                "team_status": await self.get_updated_team_status(event["team_member"]),
                "capacity": await self.get_updated_capacity_metrics(event["sprint_id"])
            }
        
        elif event["type"] == "blocker_added":
            update_payload["affected_areas"].extend(["blockers", "alerts"])
            update_payload["updates"] = {
                "blockers": await self.get_updated_blocker_list(event["sprint_id"]),
                "alerts": await self.get_updated_alert_list(event["sprint_id"])
            }
        
        elif event["type"] == "progress_milestone":
            update_payload["affected_areas"].extend(["burndown", "velocity"])
            update_payload["updates"] = {
                "burndown": await self.get_updated_burndown_chart(event["sprint_id"]),
                "velocity": await self.get_updated_velocity_metrics(event["sprint_id"])
            }
        
        # Broadcast update to connected clients
        await self.websocket_manager.broadcast_update(update_payload)
        
        # Trigger any necessary automations
        await self.trigger_event_automations(event)
    
    async def synchronize_external_systems(self, sprint_id: str):
        """Synchronize sprint state with external systems"""
        
        sync_tasks = [
            self.sync_with_jira(sprint_id),
            self.sync_with_github(sprint_id),
            self.sync_with_slack(sprint_id),
            self.sync_with_ci_cd(sprint_id)
        ]
        
        sync_results = await asyncio.gather(*sync_tasks, return_exceptions=True)
        
        return {
            "jira": sync_results[0],
            "github": sync_results[1],
            "slack": sync_results[2],
            "ci_cd": sync_results[3]
        }
```

## Interaction Patterns and User Flows

### Primary Sprint Workflows

#### 1. Daily Standup Flow
```
Standup Start → Team Check-in → Progress Updates → Blocker Discussion → Action Items → Sprint Health Assessment

Example Flow:
1. User types "/standup start" to begin daily standup
2. System presents team member status and yesterday's progress
3. Each team member provides updates (automated or manual)
4. System identifies blockers and suggests resolution actions
5. User assigns action items and updates sprint board
6. System generates standup summary and next steps
7. Updates are synchronized across all systems
```

#### 2. Task Management Flow
```
Task Creation → Estimation → Assignment → Progress Tracking → Review → Completion

Example Flow:
1. User types "/task create JWT refresh implementation"
2. System prompts for estimation, priority, and dependencies
3. User provides details: "5 SP, high priority, depends on AUTH-019"
4. System suggests best assignee based on capacity and skills
5. Task moves through workflow states with automated updates
6. System tracks progress and provides completion predictions
7. Quality gates and reviews are automatically triggered
```

#### 3. Blocker Resolution Flow
```
Blocker Detection → Impact Assessment → Resolution Planning → Action Assignment → Progress Monitoring → Resolution

Example Flow:
1. System detects task blocked for >24 hours
2. Automatically escalates to sprint master
3. User types "/block resolve AUTH-023" to start resolution process
4. System suggests resolution strategies and resource allocation
5. User assigns action items to specific team members
6. System monitors resolution progress and provides updates
7. Blocker is resolved and task workflow resumes
```

### Interactive Task Management

```python
class InteractiveTaskManager:
    def __init__(self):
        self.drag_drop_processor = DragDropProcessor()
        self.quick_actions = QuickActionProcessor()
        self.context_menu = ContextMenuManager()
        
    def handle_task_interaction(self, interaction: dict, context: dict) -> dict:
        """Handle interactive task management operations"""
        
        if interaction["type"] == "drag_drop":
            return self.handle_drag_drop(interaction, context)
        elif interaction["type"] == "quick_action":
            return self.handle_quick_action(interaction, context)
        elif interaction["type"] == "context_menu":
            return self.handle_context_menu(interaction, context)
        elif interaction["type"] == "inline_edit":
            return self.handle_inline_edit(interaction, context)
        else:
            return {"error": f"Unknown interaction type: {interaction['type']}"}
    
    def handle_drag_drop(self, interaction: dict, context: dict) -> dict:
        """Handle drag and drop task operations"""
        
        task_id = interaction["task_id"]
        source_column = interaction["source_column"]
        target_column = interaction["target_column"]
        position = interaction.get("position", 0)
        
        # Validate move
        validation = self.validate_task_move(task_id, source_column, target_column, context)
        
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["reason"],
                "suggestions": validation["suggestions"]
            }
        
        # Execute move
        move_result = self.execute_task_move(task_id, target_column, position, context)
        
        if move_result["success"]:
            # Trigger workflow automations
            automations = self.trigger_move_automations(task_id, source_column, target_column, context)
            
            # Update related tasks and dependencies
            related_updates = self.update_related_tasks(task_id, target_column, context)
            
            return {
                "success": True,
                "task_updates": move_result["updates"],
                "automations_triggered": automations,
                "related_updates": related_updates,
                "board_state": self.get_updated_board_state(context["sprint_id"])
            }
        else:
            return {
                "success": False,
                "error": move_result["error"]
            }
    
    def validate_task_move(self, task_id: str, source: str, target: str, context: dict) -> dict:
        """Validate if task can be moved to target column"""
        
        task = self.get_task(task_id)
        validation = {"valid": True, "reason": "", "suggestions": []}
        
        # Check if task has blockers
        if target == "in_progress" and task.get("blockers"):
            validation["valid"] = False
            validation["reason"] = "Task has active blockers"
            validation["suggestions"] = [
                "Resolve blockers first",
                "Move to 'blocked' column instead"
            ]
        
        # Check if task has dependencies
        if target == "in_progress" and not self.dependencies_met(task_id):
            validation["valid"] = False
            validation["reason"] = "Task dependencies not completed"
            validation["suggestions"] = [
                "Complete dependent tasks first",
                "Review dependency requirements"
            ]
        
        # Check if assignee has capacity
        if target == "in_progress" and not self.assignee_has_capacity(task.get("assignee")):
            validation["valid"] = False
            validation["reason"] = "Assignee at full capacity"
            validation["suggestions"] = [
                "Reassign to available team member",
                "Wait for current work to complete"
            ]
        
        # Check if review requirements met
        if target == "review" and not self.review_requirements_met(task_id):
            validation["valid"] = False
            validation["reason"] = "Task not ready for review"
            validation["suggestions"] = [
                "Complete implementation first",
                "Add required documentation",
                "Ensure tests are passing"
            ]
        
        return validation
```

## Response Formatting Rules

### Sprint Interface Standards

```python
class SprintInterfaceFormatter:
    def __init__(self):
        self.layout_manager = SprintLayoutManager()
        self.progress_visualizer = ProgressVisualizer()
        self.status_formatter = StatusFormatter()
        
    def format_sprint_board(self, board_state: dict, context: dict) -> str:
        """Format sprint task board for display"""
        
        board_display = ""
        
        # Board header
        board_display += self.format_board_header(board_state, context)
        board_display += "\n"
        
        # Column headers
        columns = ["TODO", "IN PROGRESS", "REVIEW", "DONE"]
        column_data = board_state["columns"]
        
        # Calculate column widths
        col_width = 25
        board_display += "│ "
        
        for col in columns:
            count = column_data[col.lower().replace(" ", "_")]["count"]
            header = f"─ {col} ({count}) "
            board_display += f"{header:─<{col_width-1}}┐ │ "
        
        board_display = board_display.rstrip(" │ ") + " │\n"
        
        # Task cards
        max_cards = max(len(column_data[col.lower().replace(" ", "_")]["tasks"]) for col in columns)
        
        for row in range(max_cards):
            board_display += "│ "
            
            for col in columns:
                col_key = col.lower().replace(" ", "_")
                tasks = column_data[col_key]["tasks"]
                
                if row < len(tasks):
                    task = tasks[row]
                    card = self.format_task_card(task, col_width-2)
                else:
                    card = " " * (col_width-2)
                
                board_display += f"{card} │ "
            
            board_display = board_display.rstrip(" │ ") + " │\n"
        
        return board_display
    
    def format_task_card(self, task: dict, width: int) -> str:
        """Format individual task card"""
        
        # Task ID and title
        title = f"[{task['id']}] {task['title']}"
        if len(title) > width:
            title = title[:width-3] + "..."
        
        card = f"{title:<{width}}\n"
        
        # Status indicator and progress
        status_icon = self.get_status_icon(task)
        if task.get("progress"):
            progress = f"📊 {int(task['progress']*100)}%"
            card += f"{status_icon} {progress:<{width-3}}\n"
        else:
            status_text = task.get("status", "").replace("_", " ").title()
            card += f"{status_icon} {status_text:<{width-3}}\n"
        
        # Assignee and estimates
        if task.get("assignee"):
            assignee = f"@{task['assignee']}"
            if task.get("story_points"):
                estimate = f"{task['story_points']} SP"
                card += f"{assignee} │ {estimate:<{width-len(assignee)-4}}\n"
            else:
                card += f"{assignee:<{width}}\n"
        
        # Blockers or additional info
        if task.get("blocker"):
            blocker = f"Blocked: {task['blocker']}"
            if len(blocker) > width:
                blocker = blocker[:width-3] + "..."
            card += f"{blocker:<{width}}\n"
        elif task.get("estimated_completion"):
            eta = f"ETA: {task['estimated_completion']}"
            card += f"{eta:<{width}}\n"
        
        return card.rstrip("\n")
    
    def format_burndown_chart(self, burndown_data: dict, context: dict) -> str:
        """Format sprint burndown chart"""
        
        chart = "┌─ Burndown Chart ─────────────────────────────────────────────────┐\n"
        chart += "│ Story Points │                                                   │\n"
        
        # Chart data
        max_points = burndown_data["max_points"]
        days = burndown_data["days"]
        ideal_line = burndown_data["ideal_line"]
        actual_line = burndown_data["actual_line"]
        
        # Y-axis scale
        scale_points = [max_points, max_points*0.75, max_points*0.5, max_points*0.25, 0]
        
        for point in scale_points:
            chart += f"│     {int(point):2d} ├─"
            
            # Plot ideal and actual lines
            for day in range(len(days)):
                if abs(ideal_line[day] - point) < max_points * 0.05:
                    chart += "●"
                elif abs(actual_line[day] - point) < max_points * 0.05:
                    chart += "●"
                else:
                    chart += " "
            
            chart += "│\n"
        
        # X-axis
        chart += "│      0 └─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬───│\n"
        chart += "│              D1    D3    D5    D7    D9   D11   D13   D15     │\n"
        
        # Summary
        remaining = burndown_data["remaining_points"]
        on_track = "✓" if burndown_data["on_track"] else "⚠"
        completion_est = burndown_data["completion_estimate"]
        
        chart += f"│ Remaining: {remaining} SP │ On Track: {on_track} │ Risk: {burndown_data['risk']} │ Completion Est: {completion_est} │\n"
        chart += "└──────────────────────────────────────────────────────────────────┘"
        
        return chart
    
    def format_team_status(self, team_status: dict, context: dict) -> str:
        """Format team member status display"""
        
        status_display = ""
        
        for member, status in team_status.items():
            # Utilization bar
            utilization = status["utilization"]
            util_bar = "●" * int(utilization * 5) + "○" * (5 - int(utilization * 5))
            util_percent = f"{int(utilization * 100)}%"
            
            # Current work
            current = status.get("current_task", "Available")
            
            # Next availability
            availability = status.get("next_available", "Available now")
            if availability == "fully_booked":
                availability = "--"
            elif availability == "some_capacity":
                availability = f"Available: {status.get('next_available', 'Soon')}"
            
            status_line = f"@{member} [{util_bar}] {util_percent:>4} │ Current: {current:<20} │ {availability}"
            
            # Add blockers if any
            if status.get("blockers"):
                blockers = ", ".join(status["blockers"])
                status_line += f" │ BLOCKED: {blockers}"
            
            status_display += status_line + "\n"
        
        return status_display.rstrip("\n")
```

## Error Handling and Feedback Mechanisms

### Sprint Execution Error Management

```python
class SprintErrorHandler:
    def __init__(self):
        self.error_classifier = ErrorClassifier()
        self.recovery_manager = RecoveryManager()
        self.feedback_generator = FeedbackGenerator()
        
    def handle_sprint_error(self, error: Exception, context: dict) -> dict:
        """Handle sprint execution errors with context-aware recovery"""
        
        error_response = {
            "error_type": self.error_classifier.classify(error),
            "severity": self.assess_error_severity(error, context),
            "impact_assessment": self.assess_sprint_impact(error, context),
            "recovery_actions": [],
            "user_feedback": "",
            "system_actions": []
        }
        
        # Task-related errors
        if "task" in str(error).lower():
            error_response.update(self.handle_task_error(error, context))
        
        # Team capacity errors
        elif "capacity" in str(error).lower():
            error_response.update(self.handle_capacity_error(error, context))
        
        # Sprint timeline errors
        elif "timeline" in str(error).lower():
            error_response.update(self.handle_timeline_error(error, context))
        
        # Integration errors
        elif "integration" in str(error).lower():
            error_response.update(self.handle_integration_error(error, context))
        
        # Generic sprint errors
        else:
            error_response.update(self.handle_generic_sprint_error(error, context))
        
        # Generate user feedback
        error_response["user_feedback"] = self.generate_user_feedback(error_response)
        
        # Execute automatic recovery if possible
        if error_response["severity"] != "critical":
            recovery_result = self.attempt_automatic_recovery(error_response, context)
            error_response["recovery_result"] = recovery_result
        
        return error_response
    
    def handle_task_error(self, error: Exception, context: dict) -> dict:
        """Handle task-related errors"""
        
        task_id = context.get("task_id")
        error_details = {}
        
        if "blocked" in str(error).lower():
            error_details.update({
                "recovery_actions": [
                    f"Identify blocker for task {task_id}",
                    "Assign alternative work to team member",
                    "Escalate blocker to appropriate team lead",
                    "Update sprint board to reflect blocker"
                ],
                "system_actions": [
                    "Mark task as blocked",
                    "Notify assigned team member",
                    "Find alternative work assignments",
                    "Update sprint risk assessment"
                ]
            })
        
        elif "dependency" in str(error).lower():
            error_details.update({
                "recovery_actions": [
                    "Review task dependencies",
                    "Identify missing prerequisite work",
                    "Adjust sprint plan if necessary",
                    "Communicate changes to team"
                ],
                "system_actions": [
                    "Update dependency tracking",
                    "Recalculate sprint timeline",
                    "Suggest alternative task ordering",
                    "Alert sprint master"
                ]
            })
        
        elif "assignment" in str(error).lower():
            error_details.update({
                "recovery_actions": [
                    "Review team capacity",
                    "Reassign task to available team member",
                    "Adjust task priorities if needed",
                    "Update sprint commitments"
                ],
                "system_actions": [
                    "Suggest alternative assignees",
                    "Check team availability",
                    "Update capacity planning",
                    "Rebalance workload"
                ]
            })
        
        return error_details
    
    def assess_sprint_impact(self, error: Exception, context: dict) -> dict:
        """Assess the impact of an error on sprint progress"""
        
        sprint_id = context.get("sprint_id")
        current_state = self.get_current_sprint_state(sprint_id)
        
        impact_assessment = {
            "timeline_impact": "none",
            "quality_impact": "none",
            "team_impact": "none",
            "goal_impact": "none",
            "mitigation_required": False,
            "escalation_needed": False
        }
        
        # Assess timeline impact
        if "blocker" in str(error).lower() or "dependency" in str(error).lower():
            days_remaining = current_state["days_remaining"]
            if days_remaining <= 3:
                impact_assessment["timeline_impact"] = "high"
                impact_assessment["escalation_needed"] = True
            elif days_remaining <= 5:
                impact_assessment["timeline_impact"] = "medium"
                impact_assessment["mitigation_required"] = True
            else:
                impact_assessment["timeline_impact"] = "low"
        
        # Assess quality impact
        if "test" in str(error).lower() or "review" in str(error).lower():
            test_coverage = current_state.get("test_coverage", 0)
            if test_coverage < 0.7:
                impact_assessment["quality_impact"] = "high"
                impact_assessment["mitigation_required"] = True
            elif test_coverage < 0.85:
                impact_assessment["quality_impact"] = "medium"
        
        # Assess team impact
        if "capacity" in str(error).lower() or "assignment" in str(error).lower():
            team_utilization = current_state.get("team_utilization", 0)
            if team_utilization > 0.9:
                impact_assessment["team_impact"] = "high"
                impact_assessment["mitigation_required"] = True
            elif team_utilization > 0.8:
                impact_assessment["team_impact"] = "medium"
        
        # Assess sprint goal impact
        completion_rate = current_state.get("completion_rate", 0)
        if completion_rate < 0.6 and current_state["days_remaining"] <= 5:
            impact_assessment["goal_impact"] = "high"
            impact_assessment["escalation_needed"] = True
        elif completion_rate < 0.8 and current_state["days_remaining"] <= 3:
            impact_assessment["goal_impact"] = "medium"
            impact_assessment["mitigation_required"] = True
        
        return impact_assessment
    
    def generate_user_feedback(self, error_response: dict) -> str:
        """Generate contextual user feedback for sprint errors"""
        
        error_type = error_response["error_type"]
        severity = error_response["severity"]
        impact = error_response["impact_assessment"]
        
        feedback = ""
        
        # Severity-based messaging
        if severity == "critical":
            feedback += "🔴 CRITICAL: Sprint execution issue detected. Immediate attention required.\n\n"
        elif severity == "high":
            feedback += "🟡 WARNING: Sprint issue may impact delivery timeline.\n\n"
        else:
            feedback += "🔵 INFO: Minor sprint execution issue detected.\n\n"
        
        # Impact-specific guidance
        if impact["timeline_impact"] == "high":
            feedback += "⏰ Timeline Impact: Sprint goal delivery at risk. Consider:\n"
            feedback += "   • Reducing sprint scope\n"
            feedback += "   • Extending sprint timeline\n"
            feedback += "   • Reallocating team resources\n\n"
        
        if impact["quality_impact"] == "high":
            feedback += "⚠️ Quality Impact: Test coverage or code quality concerns. Consider:\n"
            feedback += "   • Increasing testing efforts\n"
            feedback += "   • Adding quality gates\n"
            feedback += "   • Scheduling technical review\n\n"
        
        if impact["team_impact"] == "high":
            feedback += "👥 Team Impact: Team capacity or assignment concerns. Consider:\n"
            feedback += "   • Rebalancing workload\n"
            feedback += "   • Adjusting individual assignments\n"
            feedback += "   • Providing additional support\n\n"
        
        # Recommended actions
        if error_response["recovery_actions"]:
            feedback += "🎯 Recommended Actions:\n"
            for i, action in enumerate(error_response["recovery_actions"][:3], 1):
                feedback += f"   {i}. {action}\n"
            
            if len(error_response["recovery_actions"]) > 3:
                feedback += f"   ... and {len(error_response['recovery_actions']) - 3} more\n"
        
        # Quick actions
        feedback += "\n💡 Quick Actions Available:\n"
        feedback += "   • Type '/sprint analyze' for detailed analysis\n"
        feedback += "   • Type '/team rebalance' to adjust assignments\n"
        feedback += "   • Type '/escalate' to notify sprint lead\n"
        
        return feedback
```

This comprehensive Sprint Execution interface provides real-time operational control over development workflows, emphasizing task-level visibility, team coordination, and delivery optimization. It integrates agile practices with automated workflow management while maintaining the flexibility needed for effective sprint execution.