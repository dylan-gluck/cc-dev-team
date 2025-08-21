# V2 Orchestration State Management Design

## Executive Summary

This document defines the comprehensive state management architecture for the v2 orchestration system, providing session isolation, high-performance in-memory operations, crash recovery, and event sourcing capabilities. The design supports multiple orchestration modes with efficient queries, automatic persistence, and comprehensive audit trails.

## Architecture Overview

### Core Principles

1. **Session Isolation**: Each Claude Code instance maintains independent state
2. **Performance First**: In-memory operations with strategic persistence
3. **Resilience**: Automatic crash recovery and state reconstruction
4. **Observability**: Complete audit trail through event sourcing
5. **Scalability**: Efficient operations regardless of session complexity

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Session State Manager                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   In-Memory     │  │   Persistence   │  │  Event Store    │  │
│  │     Cache       │  │    Manager      │  │   (JSONL)       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Query API     │  │  Recovery       │  │   Cleanup       │  │
│  │   (JSONPath)    │  │  Engine         │  │   Manager       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Session State Schema

### Core JSON Schema Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Claude Code Orchestration Session State",
  "version": "2.0.0",
  "properties": {
    "session": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid",
          "description": "Unique session identifier"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string", 
          "format": "date-time"
        },
        "mode": {
          "type": "string",
          "enum": ["development", "leadership", "config", "emergency"],
          "description": "Current orchestration mode"
        },
        "user_context": {
          "type": "object",
          "properties": {
            "workspace_path": {"type": "string"},
            "project_name": {"type": "string"},
            "git_branch": {"type": "string"},
            "user_preferences": {
              "type": "object",
              "properties": {
                "max_parallel_agents": {"type": "integer", "minimum": 1, "maximum": 10},
                "auto_persistence_interval": {"type": "integer", "minimum": 10},
                "consent_mode": {"type": "string", "enum": ["explicit", "informed", "automatic"]}
              }
            }
          },
          "required": ["workspace_path"]
        },
        "lifecycle": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string",
              "enum": ["initializing", "active", "suspended", "terminating", "terminated"]
            },
            "last_activity": {"type": "string", "format": "date-time"},
            "expiry": {"type": "string", "format": "date-time"},
            "auto_cleanup": {"type": "boolean", "default": true}
          }
        }
      },
      "required": ["id", "created_at", "mode", "user_context", "lifecycle"]
    },
    "organization": {
      "type": "object",
      "properties": {
        "teams": {
          "type": "object",
          "patternProperties": {
            "^[a-z][a-z0-9-]*$": {
              "$ref": "#/$defs/team"
            }
          }
        },
        "projects": {
          "type": "object",
          "patternProperties": {
            "^[a-z0-9-]+$": {
              "$ref": "#/$defs/project"
            }
          }
        },
        "global_settings": {
          "type": "object",
          "properties": {
            "token_budget": {"type": "integer", "minimum": 0},
            "time_budget_minutes": {"type": "integer", "minimum": 0},
            "max_concurrent_agents": {"type": "integer", "minimum": 1, "maximum": 20}
          }
        }
      }
    },
    "execution": {
      "type": "object",
      "properties": {
        "agents": {
          "type": "object",
          "properties": {
            "active": {
              "type": "object",
              "patternProperties": {
                "^[a-z][a-z0-9-]*$": {
                  "$ref": "#/$defs/agent_instance"
                }
              }
            },
            "pool": {
              "type": "object",
              "patternProperties": {
                "^[a-z][a-z0-9-]*$": {
                  "$ref": "#/$defs/agent_pool_config"
                }
              }
            }
          }
        },
        "tasks": {
          "type": "object",
          "patternProperties": {
            "^task-[a-z0-9-]+$": {
              "$ref": "#/$defs/task"
            }
          }
        },
        "workflows": {
          "type": "object",
          "properties": {
            "active_sprints": {
              "type": "array",
              "items": {"$ref": "#/$defs/sprint"}
            },
            "epics": {
              "type": "object",
              "patternProperties": {
                "^epic-[a-z0-9-]+$": {
                  "$ref": "#/$defs/epic"
                }
              }
            }
          }
        }
      }
    },
    "communication": {
      "type": "object",
      "properties": {
        "message_queues": {
          "type": "object",
          "patternProperties": {
            "^[a-z][a-z0-9-]*$": {
              "type": "array",
              "items": {"$ref": "#/$defs/message"}
            }
          }
        },
        "channels": {
          "type": "object",
          "properties": {
            "broadcast": {"type": "array", "items": {"$ref": "#/$defs/message"}},
            "emergency": {"type": "array", "items": {"$ref": "#/$defs/message"}},
            "handoffs": {
              "type": "array",
              "items": {"$ref": "#/$defs/handoff"}
            }
          }
        },
        "coordination": {
          "type": "object",
          "properties": {
            "locks": {
              "type": "object",
              "patternProperties": {
                "^.+$": {
                  "$ref": "#/$defs/resource_lock"
                }
              }
            },
            "dependencies": {
              "type": "object",
              "properties": {
                "graph": {"$ref": "#/$defs/dependency_graph"},
                "blocks": {
                  "type": "array",
                  "items": {"$ref": "#/$defs/dependency_block"}
                }
              }
            }
          }
        }
      }
    },
    "observability": {
      "type": "object",
      "properties": {
        "metrics": {
          "type": "object",
          "properties": {
            "performance": {"$ref": "#/$defs/performance_metrics"},
            "utilization": {"$ref": "#/$defs/utilization_metrics"},
            "quality": {"$ref": "#/$defs/quality_metrics"}
          }
        },
        "events": {
          "type": "object",
          "properties": {
            "recent": {
              "type": "array",
              "maxItems": 100,
              "items": {"$ref": "#/$defs/event"}
            },
            "event_stream_offset": {"type": "integer", "minimum": 0}
          }
        },
        "health": {
          "type": "object",
          "properties": {
            "system_status": {
              "type": "string",
              "enum": ["healthy", "degraded", "critical", "recovering"]
            },
            "checks": {
              "type": "object",
              "patternProperties": {
                "^[a-z_]+$": {
                  "$ref": "#/$defs/health_check"
                }
              }
            }
          }
        }
      }
    },
    "persistence": {
      "type": "object",
      "properties": {
        "checkpoint": {
          "type": "object",
          "properties": {
            "last_saved": {"type": "string", "format": "date-time"},
            "sequence": {"type": "integer", "minimum": 0},
            "hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
            "size_bytes": {"type": "integer", "minimum": 0}
          }
        },
        "event_log": {
          "type": "object",
          "properties": {
            "current_offset": {"type": "integer", "minimum": 0},
            "total_events": {"type": "integer", "minimum": 0},
            "log_files": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "filename": {"type": "string"},
                  "start_offset": {"type": "integer"},
                  "end_offset": {"type": "integer"},
                  "size_bytes": {"type": "integer"}
                }
              }
            }
          }
        }
      }
    }
  },
  "required": ["session", "organization", "execution", "communication", "observability", "persistence"],
  "$defs": {
    "team": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "orchestrator": {"type": "string"},
        "members": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "agent_id": {"type": "string"},
              "role": {"type": "string"},
              "capacity": {"type": "integer", "minimum": 1},
              "skills": {"type": "array", "items": {"type": "string"}},
              "status": {"type": "string", "enum": ["available", "busy", "offline"]}
            },
            "required": ["agent_id", "role", "capacity"]
          }
        },
        "settings": {
          "type": "object",
          "properties": {
            "max_parallel": {"type": "integer", "minimum": 1},
            "require_approval": {"type": "boolean"},
            "auto_scaling": {"type": "boolean"}
          }
        }
      },
      "required": ["name", "orchestrator", "members"]
    },
    "project": {
      "type": "object", 
      "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["active", "suspended", "completed"]},
        "teams_assigned": {"type": "array", "items": {"type": "string"}},
        "repository": {
          "type": "object",
          "properties": {
            "main_branch": {"type": "string"},
            "current_branch": {"type": "string"},
            "worktrees": {
              "type": "object",
              "patternProperties": {
                "^.+$": {"type": "string"}
              }
            }
          }
        }
      },
      "required": ["id", "name", "status"]
    },
    "agent_instance": {
      "type": "object",
      "properties": {
        "session_id": {"type": "string"},
        "agent_type": {"type": "string"},
        "spawned_at": {"type": "string", "format": "date-time"},
        "status": {"type": "string", "enum": ["initializing", "idle", "busy", "blocked", "terminating"]},
        "current_task": {"type": ["string", "null"]},
        "assigned_resources": {
          "type": "array",
          "items": {"type": "string"}
        },
        "context": {
          "type": "object",
          "properties": {
            "worktree": {"type": "string"},
            "parent_agent": {"type": ["string", "null"]},
            "child_agents": {"type": "array", "items": {"type": "string"}},
            "memory_usage_mb": {"type": "integer", "minimum": 0},
            "token_usage": {"type": "integer", "minimum": 0}
          }
        },
        "health": {
          "type": "object",
          "properties": {
            "last_heartbeat": {"type": "string", "format": "date-time"},
            "error_count": {"type": "integer", "minimum": 0},
            "performance_score": {"type": "number", "minimum": 0, "maximum": 1}
          }
        }
      },
      "required": ["session_id", "agent_type", "spawned_at", "status"]
    },
    "agent_pool_config": {
      "type": "object",
      "properties": {
        "agent_type": {"type": "string"},
        "min_instances": {"type": "integer", "minimum": 0},
        "max_instances": {"type": "integer", "minimum": 1},
        "scaling_policy": {"type": "string", "enum": ["manual", "demand", "predictive"]},
        "resource_limits": {
          "type": "object",
          "properties": {
            "max_memory_mb": {"type": "integer", "minimum": 1},
            "max_tokens_per_hour": {"type": "integer", "minimum": 1}
          }
        }
      }
    },
    "task": {
      "type": "object",
      "properties": {
        "id": {"type": "string"},
        "type": {"type": "string", "enum": ["feature", "bug", "tech_debt", "documentation", "testing"]},
        "title": {"type": "string"},
        "status": {"type": "string", "enum": ["pending", "assigned", "in_progress", "review", "completed", "blocked", "cancelled"]},
        "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
        "assignee": {"type": ["string", "null"]},
        "dependencies": {"type": "array", "items": {"type": "string"}},
        "blocking": {"type": "array", "items": {"type": "string"}},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "estimated_effort": {"type": "integer", "minimum": 1},
        "actual_effort": {"type": ["integer", "null"], "minimum": 0},
        "artifacts": {"type": "array", "items": {"type": "string"}},
        "context": {
          "type": "object",
          "properties": {
            "epic_id": {"type": ["string", "null"]},
            "sprint_id": {"type": ["string", "null"]},
            "team": {"type": "string"},
            "requirements": {"type": "string"},
            "acceptance_criteria": {"type": "array", "items": {"type": "string"}}
          }
        }
      },
      "required": ["id", "type", "title", "status", "priority", "created_at"]
    },
    "sprint": {
      "type": "object",
      "properties": {
        "id": {"type": "string"},
        "epic_id": {"type": "string"},
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["planning", "active", "review", "completed", "cancelled"]},
        "start_date": {"type": "string", "format": "date"},
        "end_date": {"type": "string", "format": "date"},
        "team_assignments": {
          "type": "object",
          "patternProperties": {
            "^[a-z][a-z0-9-]*$": {
              "type": "array", 
              "items": {"type": "string"}
            }
          }
        },
        "goals": {"type": "array", "items": {"type": "string"}},
        "task_categories": {
          "type": "object",
          "properties": {
            "pending": {"type": "array", "items": {"type": "string"}},
            "in_progress": {"type": "array", "items": {"type": "string"}},
            "completed": {"type": "array", "items": {"type": "string"}},
            "blocked": {"type": "array", "items": {"type": "string"}}
          }
        },
        "metrics": {
          "type": "object",
          "properties": {
            "velocity": {"type": "number", "minimum": 0},
            "completion_rate": {"type": "number", "minimum": 0, "maximum": 1},
            "blocked_ratio": {"type": "number", "minimum": 0, "maximum": 1}
          }
        }
      },
      "required": ["id", "epic_id", "name", "status", "start_date", "end_date"]
    },
    "epic": {
      "type": "object",
      "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "status": {"type": "string", "enum": ["draft", "approved", "in_progress", "completed", "cancelled"]},
        "owner": {"type": "string"},
        "sprints": {"type": "array", "items": {"type": "string"}},
        "features": {"type": "array", "items": {"type": "string"}},
        "success_criteria": {"type": "array", "items": {"type": "string"}},
        "timeline": {
          "type": "object",
          "properties": {
            "estimated_weeks": {"type": "integer", "minimum": 1},
            "actual_weeks": {"type": ["integer", "null"], "minimum": 0}
          }
        }
      },
      "required": ["id", "title", "status", "owner"]
    },
    "message": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "format": "uuid"},
        "timestamp": {"type": "string", "format": "date-time"},
        "from": {"type": "string"},
        "to": {"type": ["string", "array"]},
        "type": {"type": "string", "enum": ["task_assigned", "task_completed", "question", "answer", "handoff", "alert"]},
        "priority": {"type": "string", "enum": ["low", "normal", "high", "critical"]},
        "payload": {},
        "correlation_id": {"type": ["string", "null"]},
        "ttl": {"type": ["integer", "null"]}
      },
      "required": ["id", "timestamp", "from", "to", "type", "priority", "payload"]
    },
    "handoff": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "format": "uuid"},
        "from_agent": {"type": "string"},
        "to_agent": {"type": "string"},
        "task_id": {"type": "string"},
        "artifacts": {"type": "array", "items": {"type": "string"}},
        "status": {"type": "string", "enum": ["pending", "acknowledged", "completed", "rejected"]},
        "created_at": {"type": "string", "format": "date-time"},
        "context": {
          "type": "object",
          "properties": {
            "work_completed": {"type": "string"},
            "next_steps": {"type": "string"},
            "notes": {"type": "string"}
          }
        }
      },
      "required": ["id", "from_agent", "to_agent", "task_id", "status", "created_at"]
    },
    "resource_lock": {
      "type": "object",
      "properties": {
        "resource": {"type": "string"},
        "locked_by": {"type": "string"},
        "locked_at": {"type": "string", "format": "date-time"},
        "expires_at": {"type": "string", "format": "date-time"},
        "lock_type": {"type": "string", "enum": ["exclusive", "shared"]},
        "reason": {"type": "string"}
      },
      "required": ["resource", "locked_by", "locked_at", "lock_type"]
    },
    "dependency_graph": {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "object",
          "patternProperties": {
            "^.+$": {
              "type": "object",
              "properties": {
                "type": {"type": "string", "enum": ["task", "agent", "resource"]},
                "status": {"type": "string"}
              }
            }
          }
        },
        "edges": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "from": {"type": "string"},
              "to": {"type": "string"},
              "type": {"type": "string", "enum": ["blocks", "enables", "requires"]}
            },
            "required": ["from", "to", "type"]
          }
        }
      }
    },
    "dependency_block": {
      "type": "object",
      "properties": {
        "blocked_item": {"type": "string"},
        "blocking_items": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
        "detected_at": {"type": "string", "format": "date-time"},
        "estimated_resolution": {"type": ["string", "null"], "format": "date-time"}
      },
      "required": ["blocked_item", "blocking_items", "reason", "detected_at"]
    },
    "performance_metrics": {
      "type": "object",
      "properties": {
        "session_duration_seconds": {"type": "integer", "minimum": 0},
        "total_tokens_used": {"type": "integer", "minimum": 0},
        "average_response_time_ms": {"type": "number", "minimum": 0},
        "agent_spawn_time_ms": {"type": "number", "minimum": 0},
        "state_query_time_ms": {"type": "number", "minimum": 0},
        "persistence_write_time_ms": {"type": "number", "minimum": 0}
      }
    },
    "utilization_metrics": {
      "type": "object",
      "properties": {
        "agent_utilization_rate": {"type": "number", "minimum": 0, "maximum": 1},
        "memory_usage_mb": {"type": "integer", "minimum": 0},
        "cpu_usage_percent": {"type": "number", "minimum": 0, "maximum": 100},
        "active_connections": {"type": "integer", "minimum": 0},
        "queue_depths": {
          "type": "object",
          "patternProperties": {
            "^.+$": {"type": "integer", "minimum": 0}
          }
        }
      }
    },
    "quality_metrics": {
      "type": "object",
      "properties": {
        "test_coverage_percent": {"type": "number", "minimum": 0, "maximum": 100},
        "code_quality_score": {"type": "number", "minimum": 0, "maximum": 100},
        "task_completion_rate": {"type": "number", "minimum": 0, "maximum": 1},
        "error_rate": {"type": "number", "minimum": 0, "maximum": 1},
        "user_satisfaction_score": {"type": "number", "minimum": 1, "maximum": 5}
      }
    },
    "event": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "format": "uuid"},
        "timestamp": {"type": "string", "format": "date-time"},
        "type": {"type": "string"},
        "source": {"type": "string"},
        "severity": {"type": "string", "enum": ["debug", "info", "warning", "error", "critical"]},
        "data": {},
        "correlation_id": {"type": ["string", "null"]},
        "session_id": {"type": "string"}
      },
      "required": ["id", "timestamp", "type", "source", "severity", "session_id"]
    },
    "health_check": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["pass", "fail", "warn"]},
        "last_checked": {"type": "string", "format": "date-time"},
        "response_time_ms": {"type": "number", "minimum": 0},
        "details": {"type": "string"},
        "threshold": {
          "type": "object",
          "properties": {
            "warning": {"type": "number"},
            "critical": {"type": "number"}
          }
        }
      },
      "required": ["name", "status", "last_checked"]
    }
  }
}
```

## State Lifecycle Management

### Session Creation and Initialization

```python
class SessionStateManager:
    def __init__(self, workspace_path: str, mode: str = "development"):
        self.session_id = str(uuid.uuid4())
        self.workspace_path = Path(workspace_path)
        self.mode = mode
        
        # Initialize state structure
        self.state = self._create_initial_state()
        
        # Setup persistence
        self.state_file = self.workspace_path / ".claude" / "state" / f"session-{self.session_id}.json"
        self.event_log = self.workspace_path / ".claude" / "state" / "events" / f"session-{self.session_id}.jsonl"
        
        # In-memory optimizations
        self._memory_cache = {}
        self._dirty_paths = set()
        self._last_persistence = time.time()
        self._persistence_timer = None
        
        # Recovery setup
        self._setup_crash_recovery()
        
    def _create_initial_state(self) -> Dict:
        """Create the initial state structure"""
        return {
            "session": {
                "id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "mode": self.mode,
                "user_context": {
                    "workspace_path": str(self.workspace_path),
                    "project_name": self.workspace_path.name,
                    "git_branch": self._get_current_branch(),
                    "user_preferences": {
                        "max_parallel_agents": 5,
                        "auto_persistence_interval": 30,
                        "consent_mode": "explicit"
                    }
                },
                "lifecycle": {
                    "status": "initializing",
                    "last_activity": datetime.now().isoformat(),
                    "expiry": (datetime.now() + timedelta(hours=8)).isoformat(),
                    "auto_cleanup": True
                }
            },
            "organization": {
                "teams": {},
                "projects": {},
                "global_settings": {
                    "token_budget": 100000,
                    "time_budget_minutes": 480,
                    "max_concurrent_agents": 10
                }
            },
            "execution": {
                "agents": {"active": {}, "pool": {}},
                "tasks": {},
                "workflows": {"active_sprints": [], "epics": {}}
            },
            "communication": {
                "message_queues": {},
                "channels": {"broadcast": [], "emergency": [], "handoffs": []},
                "coordination": {"locks": {}, "dependencies": {"graph": {"nodes": {}, "edges": []}, "blocks": []}}
            },
            "observability": {
                "metrics": {
                    "performance": {"session_duration_seconds": 0, "total_tokens_used": 0},
                    "utilization": {"agent_utilization_rate": 0.0, "memory_usage_mb": 0},
                    "quality": {"task_completion_rate": 0.0, "error_rate": 0.0}
                },
                "events": {"recent": [], "event_stream_offset": 0},
                "health": {
                    "system_status": "healthy",
                    "checks": {}
                }
            },
            "persistence": {
                "checkpoint": {
                    "last_saved": datetime.now().isoformat(),
                    "sequence": 0,
                    "hash": self._compute_state_hash({}),
                    "size_bytes": 0
                },
                "event_log": {
                    "current_offset": 0,
                    "total_events": 0,
                    "log_files": []
                }
            }
        }
```

### State Updates and Tracking

```python
    def set(self, path: str, value: Any, emit_event: bool = True) -> bool:
        """Set value at JSONPath with automatic dirty tracking"""
        try:
            # Parse JSONPath
            path_segments = self._parse_json_path(path)
            
            # Update in-memory state
            current = self.state
            for segment in path_segments[:-1]:
                current = current.setdefault(segment, {})
            
            old_value = current.get(path_segments[-1])
            current[path_segments[-1]] = value
            
            # Track changes
            self._dirty_paths.add(path)
            self.state["session"]["updated_at"] = datetime.now().isoformat()
            self.state["session"]["lifecycle"]["last_activity"] = datetime.now().isoformat()
            
            # Emit event if requested
            if emit_event:
                self._emit_event("state_updated", {
                    "path": path,
                    "old_value": old_value,
                    "new_value": value,
                    "source": "direct_update"
                })
            
            # Trigger persistence if needed
            self._schedule_persistence()
            
            return True
            
        except Exception as e:
            self._emit_event("state_error", {
                "error": str(e),
                "path": path,
                "operation": "set"
            })
            return False
    
    def get(self, path: str = None, default: Any = None) -> Any:
        """Get value at JSONPath with caching"""
        if path is None:
            return self.state
            
        # Check memory cache first
        if path in self._memory_cache:
            cache_entry = self._memory_cache[path]
            if time.time() - cache_entry["timestamp"] < 1.0:  # 1 second cache
                return cache_entry["value"]
        
        try:
            path_segments = self._parse_json_path(path)
            current = self.state
            
            for segment in path_segments:
                if isinstance(current, dict):
                    current = current.get(segment, default)
                else:
                    return default
                    
                if current is None:
                    return default
            
            # Cache result
            self._memory_cache[path] = {
                "value": current,
                "timestamp": time.time()
            }
            
            return current
            
        except Exception as e:
            self._emit_event("state_error", {
                "error": str(e),
                "path": path,
                "operation": "get"
            })
            return default
```

## Persistence Strategy

### Automatic Persistence Manager

```python
class PersistenceManager:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.state_file = session_manager.state_file
        self.event_log = session_manager.event_log
        
        # Persistence settings
        self.auto_persist_interval = 30  # seconds
        self.force_persist_threshold = 100  # changes
        self.max_state_size_mb = 10
        
        # Compression and optimization
        self.enable_compression = True
        self.enable_incremental = True
        
    def schedule_persistence(self):
        """Schedule persistence based on configurable triggers"""
        changes = len(self.session_manager._dirty_paths)
        time_since_last = time.time() - self.session_manager._last_persistence
        
        should_persist = (
            changes >= self.force_persist_threshold or
            time_since_last >= self.auto_persist_interval or
            self.session_manager.state["session"]["lifecycle"]["status"] == "terminating"
        )
        
        if should_persist:
            asyncio.create_task(self._persist_state())
    
    async def _persist_state(self):
        """Asynchronously persist state to disk"""
        try:
            # Create checkpoint
            checkpoint_data = self._create_checkpoint()
            
            # Write atomically
            temp_file = self.state_file.with_suffix('.tmp')
            with temp_file.open('w') as f:
                if self.enable_compression:
                    json.dump(checkpoint_data, f, separators=(',', ':'))
                else:
                    json.dump(checkpoint_data, f, indent=2)
            
            # Atomic replace
            temp_file.replace(self.state_file)
            
            # Update persistence metadata
            self._update_persistence_metadata(checkpoint_data)
            
            # Clear dirty tracking
            self.session_manager._dirty_paths.clear()
            self.session_manager._last_persistence = time.time()
            
            # Emit success event
            self.session_manager._emit_event("state_persisted", {
                "checkpoint_sequence": checkpoint_data["persistence"]["checkpoint"]["sequence"],
                "size_bytes": len(json.dumps(checkpoint_data))
            })
            
        except Exception as e:
            self.session_manager._emit_event("persistence_error", {
                "error": str(e),
                "operation": "persist_state"
            })
    
    def _create_checkpoint(self) -> Dict:
        """Create a checkpoint with metadata"""
        state_copy = deepcopy(self.session_manager.state)
        
        # Update checkpoint metadata
        checkpoint = state_copy["persistence"]["checkpoint"]
        checkpoint["last_saved"] = datetime.now().isoformat()
        checkpoint["sequence"] += 1
        checkpoint["hash"] = self._compute_state_hash(state_copy)
        checkpoint["size_bytes"] = len(json.dumps(state_copy))
        
        return state_copy
    
    def _compute_state_hash(self, state: Dict) -> str:
        """Compute SHA-256 hash of state for integrity checking"""
        state_json = json.dumps(state, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(state_json.encode()).hexdigest()
```

### Event Sourcing Implementation

```python
class EventStore:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.event_log_file = session_manager.event_log
        self.event_log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Event processing
        self.event_buffer = []
        self.buffer_size = 100
        self.flush_interval = 5.0  # seconds
        
        # Setup flush timer
        self._setup_flush_timer()
    
    def emit_event(self, event_type: str, data: Dict, correlation_id: str = None):
        """Emit event to the event store"""
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "source": "orchestration",
            "severity": self._determine_severity(event_type),
            "data": data,
            "correlation_id": correlation_id,
            "session_id": self.session_manager.session_id
        }
        
        # Add to buffer
        self.event_buffer.append(event)
        
        # Add to recent events in state
        recent = self.session_manager.state["observability"]["events"]["recent"]
        recent.append(event)
        if len(recent) > 100:
            recent.pop(0)
        
        # Flush if buffer is full
        if len(self.event_buffer) >= self.buffer_size:
            asyncio.create_task(self._flush_events())
    
    async def _flush_events(self):
        """Flush event buffer to disk"""
        if not self.event_buffer:
            return
            
        try:
            with self.event_log_file.open('a') as f:
                for event in self.event_buffer:
                    f.write(json.dumps(event, separators=(',', ':')) + '\n')
            
            # Update event log metadata
            self.session_manager.state["persistence"]["event_log"]["total_events"] += len(self.event_buffer)
            self.session_manager.state["persistence"]["event_log"]["current_offset"] += len(self.event_buffer)
            
            self.event_buffer.clear()
            
        except Exception as e:
            # Log error but don't fail the session
            print(f"Event flush error: {e}")
    
    def reconstruct_state_from_events(self, target_timestamp: str = None) -> Dict:
        """Reconstruct state from event log"""
        # Start with initial state
        state = self.session_manager._create_initial_state()
        
        # Replay events
        with self.event_log_file.open('r') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    
                    # Stop if target timestamp reached
                    if target_timestamp and event["timestamp"] > target_timestamp:
                        break
                    
                    # Apply event to state
                    state = self._apply_event_to_state(state, event)
                    
                except json.JSONDecodeError:
                    continue  # Skip malformed lines
        
        return state
    
    def _apply_event_to_state(self, state: Dict, event: Dict) -> Dict:
        """Apply a single event to reconstruct state"""
        event_type = event["type"]
        event_data = event["data"]
        
        if event_type == "state_updated":
            # Apply state update
            path = event_data["path"]
            value = event_data["new_value"]
            self._set_at_path(state, path, value)
            
        elif event_type == "agent_spawned":
            # Add agent to active list
            agent_id = event_data["agent_id"]
            agent_data = event_data["agent_data"]
            state["execution"]["agents"]["active"][agent_id] = agent_data
            
        elif event_type == "task_created":
            # Add task
            task_id = event_data["task_id"]
            task_data = event_data["task_data"]
            state["execution"]["tasks"][task_id] = task_data
            
        # Add more event type handlers as needed...
        
        return state
```

## Crash Recovery and State Reconstruction

### Recovery Manager

```python
class RecoveryManager:
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.state_dir = self.workspace_path / ".claude" / "state"
        
    def detect_crashed_sessions(self) -> List[str]:
        """Detect sessions that crashed without proper cleanup"""
        crashed_sessions = []
        
        for state_file in self.state_dir.glob("session-*.json"):
            try:
                with state_file.open('r') as f:
                    state = json.load(f)
                
                # Check if session was properly terminated
                lifecycle = state.get("session", {}).get("lifecycle", {})
                status = lifecycle.get("status", "unknown")
                last_activity = lifecycle.get("last_activity", "")
                
                # Consider crashed if status is not terminated and last activity is old
                if status != "terminated":
                    last_time = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                    if datetime.now(last_time.tzinfo) - last_time > timedelta(hours=1):
                        crashed_sessions.append(state["session"]["id"])
                        
            except (json.JSONDecodeError, KeyError):
                # Corrupted state file
                session_id = state_file.stem.replace("session-", "")
                crashed_sessions.append(session_id)
        
        return crashed_sessions
    
    def recover_session(self, session_id: str) -> Optional[Dict]:
        """Recover a crashed session using checkpoint and event replay"""
        try:
            # Load last checkpoint
            state_file = self.state_dir / f"session-{session_id}.json"
            
            if state_file.exists():
                with state_file.open('r') as f:
                    checkpoint_state = json.load(f)
            else:
                # No checkpoint, start from scratch
                checkpoint_state = None
            
            # Load event log
            event_log_file = self.state_dir / "events" / f"session-{session_id}.jsonl"
            
            if event_log_file.exists():
                # Replay events since last checkpoint
                recovered_state = self._replay_events_from_checkpoint(
                    checkpoint_state, event_log_file
                )
            else:
                recovered_state = checkpoint_state
            
            if recovered_state:
                # Mark as recovered
                recovered_state["session"]["lifecycle"]["status"] = "recovering"
                recovered_state["session"]["updated_at"] = datetime.now().isoformat()
                
                # Validate state integrity
                if self._validate_state_integrity(recovered_state):
                    return recovered_state
                else:
                    # State is corrupted, attempt partial recovery
                    return self._attempt_partial_recovery(recovered_state)
            
            return None
            
        except Exception as e:
            print(f"Recovery failed for session {session_id}: {e}")
            return None
    
    def _replay_events_from_checkpoint(self, checkpoint_state: Dict, event_log_file: Path) -> Dict:
        """Replay events from checkpoint to recover current state"""
        if not checkpoint_state:
            # No checkpoint, replay all events
            state = {}
        else:
            state = checkpoint_state.copy()
            checkpoint_time = checkpoint_state["persistence"]["checkpoint"]["last_saved"]
        
        # Replay events after checkpoint
        with event_log_file.open('r') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    
                    # Skip events before checkpoint
                    if checkpoint_state and event["timestamp"] <= checkpoint_time:
                        continue
                    
                    # Apply event
                    state = self._apply_event_to_state(state, event)
                    
                except json.JSONDecodeError:
                    continue
        
        return state
    
    def _validate_state_integrity(self, state: Dict) -> bool:
        """Validate that recovered state is consistent and valid"""
        try:
            # Check required top-level keys
            required_keys = ["session", "organization", "execution", "communication", "observability", "persistence"]
            if not all(key in state for key in required_keys):
                return False
            
            # Validate session metadata
            session = state["session"]
            if not all(key in session for key in ["id", "created_at", "mode", "user_context", "lifecycle"]):
                return False
            
            # Check state consistency
            # Example: All tasks referenced in sprint should exist
            for sprint in state["execution"]["workflows"]["active_sprints"]:
                for task_list in sprint.get("task_categories", {}).values():
                    for task_id in task_list:
                        if task_id not in state["execution"]["tasks"]:
                            return False
            
            # Validate hash if available
            checkpoint = state.get("persistence", {}).get("checkpoint", {})
            if "hash" in checkpoint:
                current_hash = self._compute_state_hash(state)
                # Allow hash mismatch due to recovery, but log it
                if current_hash != checkpoint["hash"]:
                    print(f"Warning: State hash mismatch during recovery")
            
            return True
            
        except Exception:
            return False
    
    def cleanup_orphaned_resources(self, session_id: str):
        """Clean up resources from crashed session"""
        state_dir = self.state_dir
        
        # Remove state file
        state_file = state_dir / f"session-{session_id}.json"
        if state_file.exists():
            state_file.unlink()
        
        # Archive event log
        event_log = state_dir / "events" / f"session-{session_id}.jsonl"
        if event_log.exists():
            archive_dir = state_dir / "archive"
            archive_dir.mkdir(exist_ok=True)
            archive_file = archive_dir / f"session-{session_id}-{int(time.time())}.jsonl"
            event_log.rename(archive_file)
        
        # Clean up temporary files
        for temp_file in state_dir.glob(f"session-{session_id}*.tmp"):
            temp_file.unlink()
```

## Performance Optimization Techniques

### Query API with Caching

```python
class QueryAPI:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.query_cache = {}
        self.cache_ttl = 5.0  # seconds
        
    def query(self, jsonpath: str, use_cache: bool = True) -> Any:
        """Execute JSONPath query with caching"""
        cache_key = jsonpath
        
        # Check cache first
        if use_cache and cache_key in self.query_cache:
            cache_entry = self.query_cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                return cache_entry["result"]
        
        # Execute query
        start_time = time.time()
        
        try:
            result = self._execute_jsonpath_query(jsonpath)
            execution_time = (time.time() - start_time) * 1000  # ms
            
            # Cache result
            if use_cache:
                self.query_cache[cache_key] = {
                    "result": result,
                    "timestamp": time.time()
                }
            
            # Update performance metrics
            self._update_query_metrics(execution_time)
            
            return result
            
        except Exception as e:
            self.session_manager._emit_event("query_error", {
                "error": str(e),
                "jsonpath": jsonpath,
                "execution_time_ms": (time.time() - start_time) * 1000
            })
            return None
    
    def _execute_jsonpath_query(self, jsonpath: str) -> Any:
        """Execute JSONPath query against current state"""
        # Simple implementation - could use jsonpath-ng for complex queries
        if jsonpath.startswith('$.'):
            # Remove leading $. and split path
            path = jsonpath[2:].split('.')
            current = self.session_manager.state
            
            for segment in path:
                if isinstance(current, dict):
                    current = current.get(segment)
                elif isinstance(current, list) and segment.isdigit():
                    index = int(segment)
                    current = current[index] if 0 <= index < len(current) else None
                else:
                    return None
                    
                if current is None:
                    break
                    
            return current
        else:
            # Simple path access
            return self.session_manager.get(jsonpath)
    
    def bulk_query(self, queries: List[str]) -> Dict[str, Any]:
        """Execute multiple queries in batch for efficiency"""
        results = {}
        
        # Group queries by common prefixes to optimize
        query_groups = self._group_queries_by_prefix(queries)
        
        for prefix, group_queries in query_groups.items():
            # Pre-fetch common data
            common_data = self.session_manager.get(prefix) if prefix else self.session_manager.state
            
            for query in group_queries:
                # Execute relative to common data
                relative_path = query[len(prefix)+1:] if prefix else query
                results[query] = self._get_from_data(common_data, relative_path)
        
        return results
    
    def _group_queries_by_prefix(self, queries: List[str]) -> Dict[str, List[str]]:
        """Group queries by common prefixes for batch optimization"""
        groups = {}
        
        for query in queries:
            parts = query.split('.')
            # Find longest common prefix with existing groups
            best_prefix = ""
            
            for existing_prefix in groups.keys():
                if query.startswith(existing_prefix):
                    if len(existing_prefix) > len(best_prefix):
                        best_prefix = existing_prefix
            
            if best_prefix:
                groups[best_prefix].append(query)
            else:
                # Create new group
                prefix = '.'.join(parts[:-1]) if len(parts) > 1 else ""
                groups.setdefault(prefix, []).append(query)
        
        return groups
```

### Size Limits and Cleanup Policies

```python
class CleanupManager:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.max_state_size_mb = 50
        self.max_events_per_session = 10000
        self.max_session_age_hours = 48
        self.cleanup_interval = 300  # 5 minutes
        
        # Setup cleanup timer
        self._setup_cleanup_timer()
    
    def _setup_cleanup_timer(self):
        """Setup periodic cleanup"""
        async def cleanup_loop():
            while True:
                await asyncio.sleep(self.cleanup_interval)
                await self._perform_cleanup()
        
        asyncio.create_task(cleanup_loop())
    
    async def _perform_cleanup(self):
        """Perform automatic cleanup based on policies"""
        try:
            # Check state size
            await self._check_state_size()
            
            # Clean old events
            await self._clean_old_events()
            
            # Archive completed tasks
            await self._archive_completed_tasks()
            
            # Clean up orphaned resources
            await self._clean_orphaned_resources()
            
        except Exception as e:
            self.session_manager._emit_event("cleanup_error", {
                "error": str(e)
            })
    
    async def _check_state_size(self):
        """Check if state size exceeds limits"""
        state_json = json.dumps(self.session_manager.state)
        size_mb = len(state_json.encode('utf-8')) / (1024 * 1024)
        
        if size_mb > self.max_state_size_mb:
            # Trigger aggressive cleanup
            await self._aggressive_cleanup()
            
            self.session_manager._emit_event("state_size_warning", {
                "current_size_mb": size_mb,
                "max_size_mb": self.max_state_size_mb
            })
    
    async def _clean_old_events(self):
        """Remove old events from memory"""
        events = self.session_manager.state["observability"]["events"]["recent"]
        
        if len(events) > self.max_events_per_session:
            # Keep only recent events
            events[:] = events[-self.max_events_per_session//2:]
            
            self.session_manager._emit_event("events_pruned", {
                "events_kept": len(events)
            })
    
    async def _archive_completed_tasks(self):
        """Archive completed tasks to reduce state size"""
        tasks = self.session_manager.state["execution"]["tasks"]
        archived_count = 0
        
        # Find old completed tasks
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        tasks_to_archive = []
        for task_id, task in tasks.items():
            if (task.get("status") == "completed" and 
                "updated_at" in task and
                datetime.fromisoformat(task["updated_at"]) < cutoff_time):
                tasks_to_archive.append(task_id)
        
        # Archive tasks
        if tasks_to_archive:
            archive_data = {task_id: tasks.pop(task_id) for task_id in tasks_to_archive}
            await self._write_archive("completed_tasks", archive_data)
            archived_count = len(tasks_to_archive)
        
        if archived_count > 0:
            self.session_manager._emit_event("tasks_archived", {
                "archived_count": archived_count
            })
    
    async def _write_archive(self, archive_type: str, data: Dict):
        """Write archived data to separate file"""
        archive_dir = self.session_manager.workspace_path / ".claude" / "state" / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = archive_dir / f"{archive_type}_{timestamp}.json"
        
        with archive_file.open('w') as f:
            json.dump(data, f, indent=2)
```

## Implementation Examples

### Mode-Specific Initialization

```python
def initialize_development_mode(state_manager: SessionStateManager):
    """Initialize state for development orchestration mode"""
    # Load default teams for development
    development_teams = {
        "engineering": {
            "name": "Engineering Team",
            "orchestrator": "engineering-director", 
            "members": [
                {"agent_id": "engineering-lead", "role": "Technical Lead", "capacity": 1},
                {"agent_id": "engineering-fullstack", "role": "Full Stack Developer", "capacity": 3},
                {"agent_id": "engineering-test", "role": "QA Engineer", "capacity": 2}
            ],
            "settings": {"max_parallel": 5, "require_approval": True}
        }
    }
    
    state_manager.set("organization.teams", development_teams)
    state_manager.set("session.lifecycle.status", "active")
    
    # Initialize default project
    project = {
        "id": "default-project",
        "name": state_manager.workspace_path.name,
        "status": "active",
        "teams_assigned": ["engineering"],
        "repository": {
            "main_branch": "main",
            "current_branch": state_manager.get("session.user_context.git_branch", "main"),
            "worktrees": {}
        }
    }
    
    state_manager.set("organization.projects.default-project", project)

def initialize_leadership_mode(state_manager: SessionStateManager):
    """Initialize state for leadership orchestration mode"""
    # Load all teams for cross-functional leadership
    leadership_teams = {
        "product": {"name": "Product Team", "orchestrator": "product-director", "members": []},
        "engineering": {"name": "Engineering Team", "orchestrator": "engineering-director", "members": []},
        "qa": {"name": "QA Team", "orchestrator": "qa-director", "members": []},
        "devops": {"name": "DevOps Team", "orchestrator": "devops-manager", "members": []},
        "creative": {"name": "Creative Team", "orchestrator": "creative-director", "members": []}
    }
    
    state_manager.set("organization.teams", leadership_teams)
    
    # Initialize epic-level planning structures
    state_manager.set("execution.workflows.epics", {})
    state_manager.set("session.lifecycle.status", "active")
```

### Edge Case Handling

```python
class EdgeCaseHandler:
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    def handle_orphaned_agent(self, agent_id: str):
        """Handle agent that lost connection to orchestrator"""
        agent = self.session_manager.get(f"execution.agents.active.{agent_id}")
        
        if not agent:
            return
        
        # Check if parent agent still exists
        parent_id = agent.get("context", {}).get("parent_agent")
        
        if parent_id and not self.session_manager.get(f"execution.agents.active.{parent_id}"):
            # Parent is gone, reassign or terminate
            self.session_manager._emit_event("orphaned_agent_detected", {
                "agent_id": agent_id,
                "parent_agent": parent_id,
                "current_task": agent.get("current_task")
            })
            
            # Try to reassign task
            current_task = agent.get("current_task")
            if current_task:
                self.session_manager.set(f"execution.tasks.{current_task}.status", "pending")
                self.session_manager.set(f"execution.tasks.{current_task}.assignee", None)
            
            # Remove orphaned agent
            self.session_manager.set(f"execution.agents.active.{agent_id}", None)
    
    def handle_circular_dependency(self, task_id: str):
        """Handle circular dependencies in task graph"""
        # Detect circular dependencies
        graph = self.session_manager.get("communication.coordination.dependencies.graph")
        
        if self._has_circular_dependency(graph, task_id):
            self.session_manager._emit_event("circular_dependency_detected", {
                "task_id": task_id,
                "dependency_chain": self._get_dependency_chain(graph, task_id)
            })
            
            # Break the cycle by removing weakest dependency
            weakest_edge = self._find_weakest_dependency(graph, task_id)
            if weakest_edge:
                self._remove_dependency_edge(graph, weakest_edge)
    
    def handle_state_corruption(self, corruption_type: str, affected_path: str):
        """Handle detected state corruption"""
        self.session_manager._emit_event("state_corruption_detected", {
            "type": corruption_type,
            "path": affected_path,
            "timestamp": datetime.now().isoformat()
        })
        
        if corruption_type == "invalid_reference":
            # Remove invalid references
            self.session_manager.set(affected_path, None)
            
        elif corruption_type == "type_mismatch":
            # Reset to valid default value
            default_value = self._get_default_for_path(affected_path)
            self.session_manager.set(affected_path, default_value)
```

## Conclusion

This v2 state management design provides a robust, scalable, and performant foundation for the orchestration system. Key benefits include:

1. **Complete Session Isolation**: Each Claude Code instance operates independently
2. **High Performance**: In-memory operations with intelligent caching and batching
3. **Automatic Recovery**: Comprehensive crash recovery using event sourcing
4. **Flexible Persistence**: Configurable persistence strategies based on needs
5. **Rich Observability**: Complete audit trail and health monitoring
6. **Scalable Architecture**: Handles complex orchestration scenarios efficiently

The schema supports all orchestration modes while maintaining consistency, provides robust error handling, and includes comprehensive cleanup policies to prevent resource exhaustion.

This design forms the critical infrastructure layer that enables sophisticated multi-agent coordination while ensuring reliability and performance at scale.