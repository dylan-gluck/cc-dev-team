# Leadership Chat Output Style Program

## System Identity

**Program Name**: `leadership_chat`  
**Purpose**: Strategic planning interface for high-level decision making and cross-team coordination  
**Execution Context**: Executive-level orchestration with advanced reasoning and planning capabilities  
**Update Frequency**: Context-aware updates with strategic insight generation

## System Prompt/Instructions

```
You are the Leadership Chat Interface, the strategic command center for executive-level decision making in the v2 orchestration system.

CORE BEHAVIORS:
- Facilitate high-level strategic planning and decision making
- Provide executive summaries with actionable insights
- Coordinate cross-team initiatives and resource allocation
- Maintain strategic context across all conversations
- Generate forward-looking analysis and recommendations
- Enable rapid escalation from operational to strategic thinking

STRATEGIC MINDSET:
- Think in terms of business impact and organizational goals
- Balance short-term execution with long-term vision  
- Consider resource constraints and opportunity costs
- Synthesize complex information into clear action plans
- Anticipate risks and provide mitigation strategies
- Foster alignment across teams and stakeholders

INTERACTION MODEL:
- Conversational interface optimized for executive dialog
- Context-aware responses that build on previous discussions
- Automatic elevation of tactical issues to strategic implications
- Integration with planning frameworks (OKRs, roadmaps, budgets)
- Real-time polling of team leads and subject matter experts
- Decision tracking with follow-up and accountability

PLANNING INTEGRATION:
- Access to organizational goals and key results
- Real-time team capacity and performance data
- Project portfolio and resource allocation visibility
- Market and competitive intelligence integration
- Risk assessment and scenario planning capabilities
- ROI and impact modeling for strategic decisions
```

## Visual Layout Design

### Main Leadership Interface

```
╭─ LEADERSHIP STRATEGIC PLANNING ─────────────────────────────────────── [Executive Mode] ─╮
│                                                    Today: Q4 Sprint Planning │ CEO: Sarah M. │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ STRATEGIC CONTEXT                                                                          │
│ ┌─ Current Quarter Status ────────────────────────────────────────────────────────────────┐ │
│ │ Q4 2024 Progress: ████████░░ 82% complete │ 15 days remaining │ On track for goals    │ │
│ │ ├─ Revenue Target: $2.4M (achieved $2.1M, 87%) │ Customer Satisfaction: 4.7/5          │ │
│ │ ├─ Product Milestones: 8/10 completed           │ Team Utilization: 89% avg            │ │
│ │ └─ Market Expansion: 3/4 regions launched       │ Technical Debt Ratio: 12% (↓3%)      │ │
│ └────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                            │
│ ┌─ Active Strategic Initiatives ──────────────────────────────────────────────────────────┐ │
│ │ 🎯 AUTH-2024-Q4: Enterprise Authentication Platform                                      │ │
│ │    Impact: $500K ARR potential │ Risk: Medium │ Timeline: 3 weeks │ Confidence: 85%    │ │
│ │    Teams: Engineering(4), Product(2), QA(2) │ Budget: $45K │ Dependencies: Security   │ │
│ │                                                                                          │ │
│ │ 🚀 SCALE-2024-Q4: Infrastructure Modernization                                          │ │
│ │    Impact: 40% cost reduction │ Risk: High │ Timeline: 6 weeks │ Confidence: 70%       │ │
│ │    Teams: DevOps(3), Engineering(2) │ Budget: $120K │ Dependencies: AWS migration      │ │
│ │                                                                                          │ │
│ │ 📈 MARKET-2024-Q4: European Market Entry                                                │ │
│ │    Impact: $300K ARR potential │ Risk: Low │ Timeline: 4 weeks │ Confidence: 92%       │ │
│ │    Teams: Marketing(3), Sales(2), Legal(1) │ Budget: $80K │ Dependencies: Compliance  │ │
│ └────────────────────────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ EXECUTIVE CONVERSATION                                                                     │
│                                                                                            │
│ [You]: I'm concerned about the authentication platform timeline. The engineering team     │
│        is reporting some integration challenges with the legacy systems.                  │
│                                                                                            │
│ [Strategic Analysis]: Based on current sprint velocity and dependency analysis, the AUTH  │
│ platform faces 3 critical path risks:                                                     │
│                                                                                            │
│ 1. Legacy System Integration (Engineering bottleneck - 65% probability of 1-week delay)  │
│    • Recommendation: Assign engineering-lead to pair with engineering-api specialist      │
│    • Alternative: Phase rollout starting with greenfield customers                        │
│    • Impact: Reduces go-to-market timeline by 40% while maintaining quality              │
│                                                                                            │
│ 2. Security Audit Requirements (Compliance checkpoint - 30% delay risk)                   │
│    • Recommendation: Parallel security review with incremental delivery                   │
│    • Resource: Engage external security consultant (budgeted $15K available)             │
│    • Timeline: Can reduce critical path by 5 days with proactive approach                 │
│                                                                                            │
│ 3. Load Testing Under Enterprise Scale (Performance validation - 45% delay risk)         │
│    • Recommendation: Synthetic load testing with AWS capacity simulation                  │
│    • Cross-team: Coordinate with SCALE initiative for shared infrastructure benefits      │
│    • Synergy: Combined testing reduces overall risk and accelerates both initiatives     │
│                                                                                            │
│ [Strategic Options]:                                                                       │
│ A) [Accelerate]: Increase team allocation (+2 engineering, +$25K) - 95% on-time delivery │
│ B) [De-risk]: Phase rollout approach - 85% revenue capture, 100% delivery confidence     │
│ C) [Optimize]: Cross-initiative resource sharing - 78% timeline, +15% ROI from synergies │
│                                                                                            │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ DECISION SUPPORT TOOLS                                                                     │
│ [📊 Impact Model] [🎯 Resource Optimizer] [📈 Scenario Planner] [⚠️ Risk Assessment]      │
│ [🔄 Team Sync] [📋 Action Items] [📅 Timeline Adjust] [💰 Budget Reallocation]            │
╰──────────────────────────────────────────────────────────────────────────────────────────╯

> Your strategic decision or next question:                          Last analysis: 14:23:45
```

### Scenario Planning Interface

```
╭─ SCENARIO PLANNING: AUTH PLATFORM DELIVERY ─────────────────── [Risk Analysis Mode] ─╮
│                                                        Confidence Intervals │ Monte Carlo │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ TIMELINE SCENARIOS                                                                       │
│                                                                                          │
│ 🟢 BEST CASE (15% probability)                                                          │
│ ├─ Duration: 18 days │ Cost: $42K │ Revenue Impact: $520K ARR                         │
│ ├─ Success Factors: No integration issues, security audit expedited, team focus       │
│ └─ Key Assumption: Engineering team maintains 95% velocity, no external dependencies  │
│                                                                                          │
│ 🟡 MOST LIKELY (60% probability)                                                        │
│ ├─ Duration: 23 days │ Cost: $48K │ Revenue Impact: $485K ARR                         │
│ ├─ Challenges: Minor integration delays, standard security review process              │
│ └─ Mitigation: Proactive communication, parallel workstreams, risk buffer included    │
│                                                                                          │
│ 🟠 PESSIMISTIC (20% probability)                                                        │
│ ├─ Duration: 32 days │ Cost: $58K │ Revenue Impact: $420K ARR                         │
│ ├─ Risks: Legacy integration blockers, security audit findings, resource conflicts    │
│ └─ Contingency: External contractors, scope reduction, customer communication plan     │
│                                                                                          │
│ 🔴 WORST CASE (5% probability)                                                          │
│ ├─ Duration: 45+ days │ Cost: $75K+ │ Revenue Impact: $200K ARR (Q1 delivery)        │
│ ├─ Crisis: Major architectural refactoring required, security compliance failure      │
│ └─ Response: Complete strategy pivot, stakeholder realignment, damage control          │
│                                                                                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ STRATEGIC DECISION MATRIX                                                                │
│                                │ Timeline │ Quality │ Budget │ Risk │ Team Morale │ ROI    │
│ ├─ Option A: Accelerate        │    ★★★    │   ★★★   │   ★★    │  ★★  │     ★★      │ ★★★    │
│ ├─ Option B: De-risk           │    ★★     │   ★★★   │   ★★★   │  ★★★ │     ★★★     │ ★★     │
│ ├─ Option C: Cross-optimize    │    ★★     │   ★★    │   ★★★   │  ★★  │     ★★      │ ★★★    │
│ └─ Option D: Scope reduction   │    ★★★    │   ★★    │   ★★★   │  ★★★ │     ★      │ ★★     │
│                                                                                          │
│ [Recommended]: Option B + C Hybrid - De-risk with selective cross-optimization         │
│ • Rationale: Maximizes delivery confidence while capturing synergy opportunities       │
│ • Trade-offs: 5-day timeline extension for 25% risk reduction and 12% ROI improvement  │
│ • Success Metrics: 95% delivery confidence, $470K ARR, team satisfaction >85%          │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command Interpreter Design

### Strategic Command Processing

```python
class LeadershipCommandProcessor:
    def __init__(self):
        self.strategic_context = StrategicContextManager()
        self.decision_frameworks = DecisionFrameworkLibrary()
        self.analysis_engine = StrategicAnalysisEngine()
        
    def process_command(self, command: str, context: dict) -> dict:
        """Process leadership commands with strategic interpretation"""
        
        if self.is_strategic_question(command):
            return self.handle_strategic_inquiry(command, context)
        elif self.is_decision_request(command):
            return self.handle_decision_support(command, context)
        elif self.is_planning_command(command):
            return self.handle_planning_operation(command, context)
        else:
            return self.handle_analysis_request(command, context)
    
    def handle_strategic_inquiry(self, inquiry: str, context: dict) -> dict:
        """Process open-ended strategic questions"""
        
        # Extract strategic intent
        intent = self.analyze_strategic_intent(inquiry)
        
        # Gather relevant data
        strategic_data = self.strategic_context.get_relevant_context(intent)
        
        # Generate analysis
        analysis = self.analysis_engine.generate_strategic_analysis(
            inquiry, strategic_data, context
        )
        
        # Format strategic response
        return {
            "type": "strategic_analysis",
            "analysis": analysis,
            "options": self.generate_strategic_options(analysis),
            "recommendations": self.rank_recommendations(analysis),
            "follow_up_questions": self.suggest_follow_up_questions(analysis)
        }
    
    def handle_decision_support(self, decision_request: str, context: dict) -> dict:
        """Provide structured decision support"""
        
        # Parse decision parameters
        decision_params = self.extract_decision_parameters(decision_request)
        
        # Apply decision framework
        framework = self.decision_frameworks.select_framework(decision_params)
        
        # Generate decision matrix
        decision_matrix = framework.analyze(decision_params, context)
        
        # Create scenario analysis
        scenarios = self.generate_scenario_analysis(decision_params, context)
        
        return {
            "type": "decision_support",
            "framework": framework.name,
            "decision_matrix": decision_matrix,
            "scenarios": scenarios,
            "risk_assessment": self.assess_risks(decision_params),
            "success_criteria": self.define_success_criteria(decision_params)
        }
```

### Strategic Analysis Engine

```python
class StrategicAnalysisEngine:
    def __init__(self):
        self.analysis_frameworks = {
            "swot": SWOTAnalysis(),
            "porter_five": PorterFiveForces(),
            "ansoff_matrix": AnsoffMatrix(),
            "bcg_matrix": BCGMatrix(),
            "okr_alignment": OKRAlignment(),
            "resource_optimization": ResourceOptimization()
        }
        
    def generate_strategic_analysis(self, inquiry: str, data: dict, context: dict) -> dict:
        """Generate comprehensive strategic analysis"""
        
        # Determine relevant analysis frameworks
        relevant_frameworks = self.select_analysis_frameworks(inquiry, data)
        
        # Run analyses
        analyses = {}
        for framework_name in relevant_frameworks:
            framework = self.analysis_frameworks[framework_name]
            analyses[framework_name] = framework.analyze(data, context)
        
        # Synthesize insights
        synthesis = self.synthesize_insights(analyses, inquiry)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(synthesis, context)
        
        return {
            "frameworks_used": relevant_frameworks,
            "individual_analyses": analyses,
            "synthesis": synthesis,
            "recommendations": recommendations,
            "confidence_score": self.calculate_confidence(analyses),
            "key_assumptions": self.extract_key_assumptions(analyses)
        }
    
    def synthesize_insights(self, analyses: dict, inquiry: str) -> dict:
        """Synthesize insights across multiple analysis frameworks"""
        
        synthesis = {
            "key_insights": [],
            "conflicting_indicators": [],
            "convergent_themes": [],
            "strategic_implications": []
        }
        
        # Extract key insights from each analysis
        for framework, analysis in analyses.items():
            insights = analysis.get("insights", [])
            synthesis["key_insights"].extend(insights)
        
        # Identify convergent themes
        synthesis["convergent_themes"] = self.find_convergent_themes(analyses)
        
        # Identify conflicts
        synthesis["conflicting_indicators"] = self.find_conflicts(analyses)
        
        # Generate strategic implications
        synthesis["strategic_implications"] = self.derive_implications(
            synthesis["key_insights"], 
            synthesis["convergent_themes"],
            inquiry
        )
        
        return synthesis
```

### Decision Support Tools

```python
class DecisionSupportTools:
    def __init__(self):
        self.impact_modeler = ImpactModeler()
        self.resource_optimizer = ResourceOptimizer()
        self.scenario_planner = ScenarioPlanner()
        self.risk_assessor = RiskAssessor()
    
    def generate_impact_model(self, decision_params: dict) -> dict:
        """Model the potential impact of strategic decisions"""
        
        return {
            "financial_impact": {
                "revenue_impact": self.calculate_revenue_impact(decision_params),
                "cost_impact": self.calculate_cost_impact(decision_params),
                "roi_projection": self.calculate_roi_projection(decision_params),
                "payback_period": self.calculate_payback_period(decision_params)
            },
            "operational_impact": {
                "team_utilization": self.assess_team_impact(decision_params),
                "process_changes": self.identify_process_changes(decision_params),
                "capability_gaps": self.identify_capability_gaps(decision_params),
                "timeline_implications": self.assess_timeline_impact(decision_params)
            },
            "strategic_impact": {
                "market_position": self.assess_market_impact(decision_params),
                "competitive_advantage": self.assess_competitive_impact(decision_params),
                "customer_impact": self.assess_customer_impact(decision_params),
                "long_term_value": self.assess_long_term_value(decision_params)
            }
        }
    
    def optimize_resource_allocation(self, initiatives: list, constraints: dict) -> dict:
        """Optimize resource allocation across multiple initiatives"""
        
        # Model resource requirements
        resource_model = self.model_resource_requirements(initiatives)
        
        # Apply constraints
        constrained_model = self.apply_constraints(resource_model, constraints)
        
        # Optimize allocation
        optimal_allocation = self.solve_optimization(constrained_model)
        
        # Generate allocation report
        return {
            "optimal_allocation": optimal_allocation,
            "resource_utilization": self.calculate_utilization(optimal_allocation),
            "initiative_prioritization": self.prioritize_initiatives(optimal_allocation),
            "constraint_analysis": self.analyze_constraints(constrained_model),
            "sensitivity_analysis": self.perform_sensitivity_analysis(optimal_allocation)
        }
```

## State Integration Points

### Strategic Context Management

```python
class StrategicContextManager:
    def __init__(self):
        self.organizational_data = OrganizationalDataProvider()
        self.market_intelligence = MarketIntelligenceProvider()
        self.performance_analytics = PerformanceAnalyticsProvider()
        self.resource_tracking = ResourceTrackingProvider()
        
    def get_strategic_context(self) -> dict:
        """Aggregate strategic context for leadership decisions"""
        
        return {
            "organizational_health": self.get_organizational_health(),
            "strategic_initiatives": self.get_active_initiatives(),
            "market_conditions": self.get_market_conditions(),
            "competitive_landscape": self.get_competitive_landscape(),
            "resource_capacity": self.get_resource_capacity(),
            "performance_trends": self.get_performance_trends(),
            "risk_profile": self.get_organizational_risks()
        }
    
    def get_organizational_health(self) -> dict:
        """Overall organizational health metrics"""
        return {
            "team_satisfaction": 4.3,  # Out of 5
            "productivity_index": 0.89,  # Normalized score
            "retention_rate": 0.94,  # Annual retention
            "knowledge_sharing": 0.78,  # Cross-team collaboration score
            "technical_debt_ratio": 0.12,  # Technical debt as % of codebase
            "deployment_frequency": 2.3,  # Deployments per day
            "lead_time": 4.2,  # Days from commit to production
            "mttr": 0.8  # Mean time to recovery in hours
        }
    
    def get_active_initiatives(self) -> list:
        """Current strategic initiatives with progress"""
        return [
            {
                "id": "AUTH-2024-Q4",
                "name": "Enterprise Authentication Platform",
                "strategic_priority": "high",
                "progress": 0.65,
                "timeline": "3 weeks",
                "budget": {"allocated": 45000, "spent": 28000},
                "team_allocation": {
                    "engineering": 4,
                    "product": 2,
                    "qa": 2
                },
                "success_metrics": {
                    "arr_impact": 500000,
                    "customer_adoption": 0.75,
                    "security_compliance": 1.0
                },
                "risk_factors": [
                    {"type": "technical", "description": "Legacy integration complexity", "probability": 0.65, "impact": "medium"},
                    {"type": "timeline", "description": "Security audit delays", "probability": 0.30, "impact": "low"},
                    {"type": "resource", "description": "Key engineer availability", "probability": 0.20, "impact": "high"}
                ]
            }
        ]
    
    def get_market_conditions(self) -> dict:
        """Current market intelligence and trends"""
        return {
            "market_size": {"current": 15.2e9, "projected_growth": 0.12},  # Billion USD, 12% CAGR
            "competitive_intensity": "high",
            "customer_demand": {
                "enterprise_auth": {"trend": "increasing", "urgency": "high"},
                "mobile_integration": {"trend": "stable", "urgency": "medium"},
                "api_performance": {"trend": "increasing", "urgency": "medium"}
            },
            "regulatory_changes": [
                {"area": "data_privacy", "impact": "medium", "timeline": "6 months"},
                {"area": "security_compliance", "impact": "high", "timeline": "3 months"}
            ],
            "technology_trends": [
                {"trend": "ai_integration", "adoption_rate": 0.45, "strategic_importance": "high"},
                {"trend": "edge_computing", "adoption_rate": 0.23, "strategic_importance": "medium"}
            ]
        }
```

### Real-Time Intelligence Gathering

```python
class IntelligenceGatherer:
    def __init__(self):
        self.team_monitors = TeamStatusMonitor()
        self.performance_monitors = PerformanceMonitor()
        self.external_monitors = ExternalIntelligenceMonitor()
        
    async def gather_strategic_intelligence(self, focus_areas: list) -> dict:
        """Gather real-time intelligence for strategic decision making"""
        
        intelligence = {
            "timestamp": datetime.now().isoformat(),
            "focus_areas": focus_areas,
            "internal_intelligence": await self.gather_internal_intelligence(focus_areas),
            "external_intelligence": await self.gather_external_intelligence(focus_areas),
            "synthesis": {}
        }
        
        # Synthesize intelligence
        intelligence["synthesis"] = self.synthesize_intelligence(
            intelligence["internal_intelligence"],
            intelligence["external_intelligence"],
            focus_areas
        )
        
        return intelligence
    
    async def gather_internal_intelligence(self, focus_areas: list) -> dict:
        """Gather internal organizational intelligence"""
        
        tasks = []
        
        for area in focus_areas:
            if area in ["team_capacity", "resource_allocation"]:
                tasks.append(self.team_monitors.get_capacity_analysis())
            
            if area in ["performance_trends", "quality_metrics"]:
                tasks.append(self.performance_monitors.get_trend_analysis())
            
            if area in ["initiative_progress", "milestone_tracking"]:
                tasks.append(self.get_initiative_progress_analysis())
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return self.consolidate_internal_intelligence(results, focus_areas)
    
    def synthesize_intelligence(self, internal: dict, external: dict, focus_areas: list) -> dict:
        """Synthesize internal and external intelligence"""
        
        synthesis = {
            "key_insights": [],
            "strategic_implications": [],
            "action_recommendations": [],
            "confidence_scores": {}
        }
        
        # Cross-reference internal capabilities with external opportunities/threats
        for area in focus_areas:
            internal_data = internal.get(area, {})
            external_data = external.get(area, {})
            
            area_synthesis = self.synthesize_area_intelligence(
                area, internal_data, external_data
            )
            
            synthesis["key_insights"].extend(area_synthesis["insights"])
            synthesis["strategic_implications"].extend(area_synthesis["implications"])
            synthesis["action_recommendations"].extend(area_synthesis["recommendations"])
            synthesis["confidence_scores"][area] = area_synthesis["confidence"]
        
        return synthesis
```

## Interaction Patterns and User Flows

### Strategic Conversation Flows

#### 1. Strategic Problem Solving Flow
```
Executive Input → Context Analysis → Strategic Options → Decision Support → Action Plan

Example Flow:
1. Executive: "Our authentication rollout is behind schedule. What are our options?"
2. System: Analyzes current project state, team capacity, market timing
3. System: Presents 3-4 strategic options with trade-offs
4. Executive: "What's the ROI impact of each option?"
5. System: Generates detailed ROI analysis and risk assessment
6. Executive: "Let's go with Option B. What's needed to execute?"
7. System: Creates detailed execution plan with milestones and assignments
8. System: Sets up monitoring and follow-up checkpoints
```

#### 2. Resource Optimization Flow
```
Resource Constraint → Portfolio Analysis → Optimization Recommendations → Implementation

Example Flow:
1. Executive: "We need to optimize team allocation across Q4 initiatives"
2. System: Analyzes current allocation, capacity, and initiative priorities
3. System: Models different allocation scenarios with impact projections
4. System: Recommends optimal allocation based on strategic goals
5. Executive: "How does this affect our market launch timeline?"
6. System: Shows timeline implications and suggests risk mitigation
7. Executive: Approves reallocation plan
8. System: Generates team communication and transition plan
```

#### 3. Scenario Planning Flow
```
Strategic Question → Scenario Generation → Impact Analysis → Risk Assessment → Preparation

Example Flow:
1. Executive: "What if our main competitor launches a similar feature next month?"
2. System: Generates multiple competitive response scenarios
3. System: Analyzes impact on our roadmap, market position, revenue
4. System: Assesses likelihood and severity of each scenario
5. Executive: "What's our best defensive strategy?"
6. System: Recommends proactive and reactive response strategies
7. System: Creates monitoring alerts for competitive intelligence
8. System: Develops contingency plans for each scenario
```

### Conversation Management

```python
class ConversationManager:
    def __init__(self):
        self.conversation_history = []
        self.strategic_context = {}
        self.decision_threads = {}
        
    def process_executive_input(self, input_text: str, context: dict) -> dict:
        """Process executive input with strategic context awareness"""
        
        # Analyze strategic intent
        intent = self.analyze_strategic_intent(input_text)
        
        # Retrieve relevant context
        relevant_context = self.get_relevant_strategic_context(intent)
        
        # Generate strategic response
        response = self.generate_strategic_response(
            input_text, intent, relevant_context, context
        )
        
        # Update conversation history
        self.update_conversation_history(input_text, response, intent)
        
        # Track decision points
        if intent.get("decision_required"):
            self.track_decision_thread(intent, response)
        
        return response
    
    def generate_strategic_response(self, input_text: str, intent: dict, 
                                  context: dict, conversation_context: dict) -> dict:
        """Generate contextually aware strategic response"""
        
        response = {
            "type": intent["type"],
            "analysis": {},
            "options": [],
            "recommendations": [],
            "follow_up": []
        }
        
        if intent["type"] == "strategic_inquiry":
            response["analysis"] = self.perform_strategic_analysis(input_text, context)
            response["options"] = self.generate_strategic_options(response["analysis"])
            response["recommendations"] = self.rank_recommendations(response["options"])
            
        elif intent["type"] == "decision_support":
            response["analysis"] = self.perform_decision_analysis(input_text, context)
            response["decision_matrix"] = self.create_decision_matrix(response["analysis"])
            response["risk_assessment"] = self.assess_decision_risks(response["analysis"])
            
        elif intent["type"] == "planning_request":
            response["analysis"] = self.perform_planning_analysis(input_text, context)
            response["scenarios"] = self.generate_planning_scenarios(response["analysis"])
            response["timeline"] = self.create_strategic_timeline(response["analysis"])
        
        # Add contextual follow-up questions
        response["follow_up"] = self.suggest_strategic_follow_up(intent, response)
        
        return response
```

## Response Formatting Rules

### Executive Communication Standards

```python
class ExecutiveCommunicationFormatter:
    def __init__(self):
        self.executive_preferences = {
            "conciseness": "high",
            "data_density": "medium",
            "visual_emphasis": "high",
            "action_orientation": "critical"
        }
        
    def format_strategic_response(self, response: dict, context: dict) -> str:
        """Format responses for executive consumption"""
        
        formatted_response = ""
        
        # Executive Summary (always first)
        if response.get("analysis"):
            formatted_response += self.format_executive_summary(response["analysis"])
            formatted_response += "\n\n"
        
        # Strategic Options (if applicable)
        if response.get("options"):
            formatted_response += self.format_strategic_options(response["options"])
            formatted_response += "\n\n"
        
        # Decision Matrix (for decision support)
        if response.get("decision_matrix"):
            formatted_response += self.format_decision_matrix(response["decision_matrix"])
            formatted_response += "\n\n"
        
        # Risk Assessment (always included for strategic decisions)
        if response.get("risk_assessment"):
            formatted_response += self.format_risk_assessment(response["risk_assessment"])
            formatted_response += "\n\n"
        
        # Action Items (always end with actionable next steps)
        if response.get("recommendations"):
            formatted_response += self.format_action_items(response["recommendations"])
        
        return formatted_response
    
    def format_executive_summary(self, analysis: dict) -> str:
        """Format executive summary with key insights"""
        
        summary = "[Strategic Analysis]:\n\n"
        
        # Key insights (top 3 most important)
        key_insights = analysis.get("key_insights", [])[:3]
        for i, insight in enumerate(key_insights, 1):
            summary += f"{i}. {insight['description']} ({insight['impact']} impact - {insight['confidence']}% confidence)\n"
            if insight.get("supporting_data"):
                summary += f"   • {insight['supporting_data']}\n"
            if insight.get("implication"):
                summary += f"   • Implication: {insight['implication']}\n"
        
        summary += "\n"
        
        # Strategic implications
        implications = analysis.get("strategic_implications", [])
        if implications:
            summary += "[Strategic Implications]:\n"
            for implication in implications[:2]:  # Top 2 most critical
                summary += f"• {implication}\n"
        
        return summary
    
    def format_strategic_options(self, options: list) -> str:
        """Format strategic options for executive decision"""
        
        formatted = "[Strategic Options]:\n"
        
        option_labels = ["A", "B", "C", "D", "E"]
        
        for i, option in enumerate(options):
            label = option_labels[i] if i < len(option_labels) else str(i+1)
            
            formatted += f"{label}) [{option['approach']}]: {option['description']}\n"
            
            # Key metrics for each option
            if option.get("metrics"):
                metrics = option["metrics"]
                formatted += f"   • Timeline: {metrics.get('timeline', 'TBD')}"
                formatted += f" | ROI: {metrics.get('roi', 'TBD')}"
                formatted += f" | Risk: {metrics.get('risk_level', 'TBD')}"
                formatted += f" | Confidence: {metrics.get('confidence', 'TBD')}%\n"
            
            # Resource requirements
            if option.get("resources"):
                formatted += f"   • Resources: {option['resources']}\n"
            
            # Key trade-offs
            if option.get("trade_offs"):
                formatted += f"   • Trade-offs: {option['trade_offs']}\n"
            
            formatted += "\n"
        
        return formatted
    
    def format_decision_matrix(self, matrix: dict) -> str:
        """Format decision matrix for comparative analysis"""
        
        formatted = "[Decision Matrix]:\n"
        formatted += "                               │ Timeline │ Quality │ Budget │ Risk │ ROI │ Confidence │\n"
        formatted += "├──────────────────────────────┼──────────┼─────────┼────────┼──────┼─────┼────────────┤\n"
        
        for option_id, scores in matrix.items():
            option_name = scores.get("name", option_id)
            formatted += f"├─ {option_name:<28} │"
            
            # Format each score with star rating
            for criterion in ["timeline", "quality", "budget", "risk", "roi", "confidence"]:
                score = scores.get(criterion, 0)
                stars = "★" * score + "☆" * (5 - score)
                formatted += f" {stars:^8} │"
            
            formatted += "\n"
        
        # Add recommendation
        recommended = matrix.get("recommended")
        if recommended:
            formatted += f"\n[Recommended]: {recommended['option']} - {recommended['rationale']}\n"
        
        return formatted
```

## Error Handling and Feedback Mechanisms

### Strategic Decision Validation

```python
class StrategicDecisionValidator:
    def __init__(self):
        self.validation_frameworks = ValidationFrameworkLibrary()
        self.stakeholder_requirements = StakeholderRequirements()
        
    def validate_strategic_decision(self, decision: dict, context: dict) -> dict:
        """Validate strategic decisions against multiple criteria"""
        
        validation_result = {
            "is_valid": True,
            "validation_score": 0.0,
            "warnings": [],
            "blockers": [],
            "recommendations": []
        }
        
        # Strategic alignment validation
        alignment_check = self.validate_strategic_alignment(decision, context)
        validation_result["alignment"] = alignment_check
        
        if alignment_check["score"] < 0.7:
            validation_result["warnings"].append(
                "Decision shows weak alignment with organizational strategy"
            )
        
        # Resource feasibility validation
        feasibility_check = self.validate_resource_feasibility(decision, context)
        validation_result["feasibility"] = feasibility_check
        
        if not feasibility_check["is_feasible"]:
            validation_result["blockers"].append(
                f"Insufficient resources: {feasibility_check['constraints']}"
            )
            validation_result["is_valid"] = False
        
        # Risk tolerance validation
        risk_check = self.validate_risk_tolerance(decision, context)
        validation_result["risk_assessment"] = risk_check
        
        if risk_check["risk_level"] > context.get("risk_tolerance", 0.7):
            validation_result["warnings"].append(
                "Decision exceeds organizational risk tolerance"
            )
        
        # Stakeholder impact validation
        stakeholder_check = self.validate_stakeholder_impact(decision, context)
        validation_result["stakeholder_impact"] = stakeholder_check
        
        if stakeholder_check["negative_impact_score"] > 0.6:
            validation_result["warnings"].append(
                "Decision may have significant negative stakeholder impact"
            )
        
        # Calculate overall validation score
        validation_result["validation_score"] = self.calculate_validation_score(
            alignment_check["score"],
            feasibility_check["score"],
            risk_check["score"],
            stakeholder_check["score"]
        )
        
        # Generate recommendations
        validation_result["recommendations"] = self.generate_validation_recommendations(
            validation_result
        )
        
        return validation_result
    
    def generate_validation_recommendations(self, validation_result: dict) -> list:
        """Generate recommendations based on validation results"""
        
        recommendations = []
        
        # Address alignment issues
        if validation_result["alignment"]["score"] < 0.7:
            recommendations.append({
                "type": "strategic_alignment",
                "priority": "high",
                "description": "Strengthen strategic alignment by emphasizing key organizational goals",
                "actions": [
                    "Review decision against current OKRs",
                    "Consult with strategic planning team",
                    "Adjust decision criteria to better align with strategy"
                ]
            })
        
        # Address resource constraints
        if not validation_result["feasibility"]["is_feasible"]:
            recommendations.append({
                "type": "resource_optimization",
                "priority": "critical",
                "description": "Resolve resource constraints before proceeding",
                "actions": [
                    "Identify alternative resource sources",
                    "Consider timeline adjustments",
                    "Explore partnership opportunities",
                    "Reassess scope and requirements"
                ]
            })
        
        # Address risk concerns
        if validation_result["risk_assessment"]["risk_level"] > 0.7:
            recommendations.append({
                "type": "risk_mitigation",
                "priority": "high",
                "description": "Implement risk mitigation strategies",
                "actions": [
                    "Develop comprehensive risk mitigation plan",
                    "Establish risk monitoring checkpoints",
                    "Create contingency plans for high-probability risks",
                    "Consider risk transfer or sharing options"
                ]
            })
        
        return recommendations
```

### Escalation and Crisis Management

```python
class StrategicEscalationManager:
    def __init__(self):
        self.escalation_criteria = EscalationCriteriaManager()
        self.crisis_protocols = CrisisProtocolManager()
        self.stakeholder_network = StakeholderNetworkManager()
        
    def assess_escalation_need(self, situation: dict, context: dict) -> dict:
        """Assess if situation requires escalation to higher authority"""
        
        escalation_assessment = {
            "escalation_required": False,
            "escalation_level": "none",
            "urgency": "low",
            "stakeholders_to_notify": [],
            "recommended_actions": []
        }
        
        # Financial impact assessment
        financial_impact = situation.get("financial_impact", 0)
        if financial_impact > 100000:  # $100K threshold
            escalation_assessment["escalation_required"] = True
            escalation_assessment["escalation_level"] = "executive"
            escalation_assessment["stakeholders_to_notify"].append("CFO")
        
        # Strategic impact assessment
        strategic_impact = situation.get("strategic_impact", "low")
        if strategic_impact in ["high", "critical"]:
            escalation_assessment["escalation_required"] = True
            escalation_assessment["escalation_level"] = "board"
            escalation_assessment["stakeholders_to_notify"].extend(["CEO", "Board"])
        
        # Timeline impact assessment
        timeline_impact = situation.get("timeline_impact", 0)
        if timeline_impact > 30:  # 30+ day delay
            escalation_assessment["escalation_required"] = True
            escalation_assessment["urgency"] = "high"
            escalation_assessment["stakeholders_to_notify"].append("COO")
        
        # Customer impact assessment
        customer_impact = situation.get("customer_impact", "low")
        if customer_impact in ["high", "critical"]:
            escalation_assessment["escalation_required"] = True
            escalation_assessment["urgency"] = "critical"
            escalation_assessment["stakeholders_to_notify"].append("Customer Success")
        
        # Generate recommended actions
        escalation_assessment["recommended_actions"] = self.generate_escalation_actions(
            escalation_assessment, situation
        )
        
        return escalation_assessment
    
    def handle_strategic_crisis(self, crisis: dict, context: dict) -> dict:
        """Handle strategic crisis situations"""
        
        crisis_response = {
            "response_level": self.assess_crisis_level(crisis),
            "immediate_actions": [],
            "communication_plan": {},
            "recovery_plan": {},
            "lessons_learned": []
        }
        
        # Activate appropriate crisis protocol
        protocol = self.crisis_protocols.get_protocol(crisis_response["response_level"])
        
        # Execute immediate response
        crisis_response["immediate_actions"] = protocol.get_immediate_actions(crisis)
        
        # Develop communication strategy
        crisis_response["communication_plan"] = self.develop_crisis_communication_plan(
            crisis, context
        )
        
        # Create recovery plan
        crisis_response["recovery_plan"] = self.develop_recovery_plan(crisis, context)
        
        # Document lessons learned (for future prevention)
        crisis_response["lessons_learned"] = self.extract_lessons_learned(crisis, context)
        
        return crisis_response
```

This sophisticated Leadership Chat interface provides executives with strategic decision-making capabilities, comprehensive analysis tools, and crisis management support. It emphasizes strategic thinking, contextual awareness, and actionable insights while maintaining the conversational flow that executives prefer for high-level planning and decision making.