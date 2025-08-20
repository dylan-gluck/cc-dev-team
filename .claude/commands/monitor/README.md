# Monitor Command Suite

A comprehensive real-time observability and monitoring system for the Claude Code development team orchestration platform.

## Overview

The `/monitor` command family provides real-time visibility into system performance, agent activity, task progress, and team utilization. All commands integrate with the `.claude/scripts/observability.py` backend for live data.

## Available Commands

### Core Monitoring
- **`/monitor`** - Main dashboard with system overview
- **`/monitor status`** - Current system health and status
- **`/monitor live`** - Live monitoring with auto-refresh

### Specialized Views
- **`/monitor agents`** - Agent performance and utilization
- **`/monitor metrics`** - KPIs and performance metrics
- **`/monitor events`** - Real-time event stream
- **`/monitor sprint`** - Sprint progress and burndown
- **`/monitor teams`** - Team capacity and utilization

## Quick Start

### Basic Monitoring
```bash
# View main dashboard
/monitor

# Check system status
/monitor status

# Start live monitoring (5-second refresh)
/monitor live 5
```

### Team Monitoring
```bash
# View all agents
/monitor agents

# Check specific team
/monitor agents engineering

# Team utilization
/monitor teams
```

### Sprint Tracking
```bash
# Current sprint progress
/monitor sprint

# Detailed sprint metrics
/monitor sprint --detailed
```

### Performance Analysis
```bash
# Performance KPIs
/monitor metrics performance

# Quality metrics
/monitor metrics quality

# Productivity stats
/monitor metrics productivity
```

## Features

### Real-Time Updates
- Auto-refresh at configurable intervals
- Live event streaming
- Real-time metric calculation
- Dynamic status indicators

### Rich Visualizations
- Color-coded health indicators
- Progress bars and charts
- Burndown graphs
- Utilization heatmaps

### Alert System
- Critical issue highlighting
- Threshold-based warnings
- Trend analysis
- Predictive alerts

### Export Capabilities
- JSON data export
- CSV reports
- PDF summaries
- API integration

## Status Indicators

### Health Status
- 🟢 **Healthy** - Operating normally
- 🟡 **Warning** - Attention needed
- 🔴 **Critical** - Immediate action required
- 🔵 **Info** - Informational
- ⚫ **Offline** - Not available

### Performance Indicators
- ✅ **On Target** - Meeting goals
- ⚠️ **At Risk** - Below target
- ❌ **Failed** - Not meeting requirements
- 📈 **Improving** - Positive trend
- 📉 **Declining** - Negative trend

## Integration Points

### Data Sources
- Observability script (`observability.py`)
- Event logs
- Agent state files
- Task databases
- Sprint tracking

### Export Formats
- **Console** - Rich formatted tables
- **JSON** - Structured data
- **CSV** - Spreadsheet compatible
- **Markdown** - Documentation
- **API** - External systems

## Use Cases

### Daily Operations
1. Morning health check with `/monitor status`
2. Sprint progress review with `/monitor sprint`
3. Team capacity planning with `/monitor teams`
4. Performance review with `/monitor metrics`

### Issue Investigation
1. Check system status for anomalies
2. Review event stream for errors
3. Analyze agent performance
4. Identify bottlenecks

### Capacity Planning
1. Monitor team utilization trends
2. Forecast resource needs
3. Identify scaling requirements
4. Balance workloads

## Keyboard Shortcuts (Live Mode)

- **Space** - Pause/Resume updates
- **R** - Force refresh
- **F** - Toggle fullscreen
- **↑/↓** - Scroll events
- **1-8** - Toggle panels
- **S** - Save snapshot
- **E** - Export data
- **Q** - Quit

## Configuration

### Refresh Intervals
- **Fast** (1-2s) - Critical monitoring
- **Normal** (5s) - Standard monitoring
- **Slow** (10-30s) - Resource conservation
- **Adaptive** - Auto-adjust based on activity

### Panel Selection
Customize which panels to display:
```bash
/monitor live 5 "system,agents,tasks"
```

### Filter Options
Filter by team, status, or time range:
```bash
/monitor agents engineering
/monitor events ERROR
/monitor metrics --last-24h
```

## Troubleshooting

### Common Issues

**No Data Displayed**
- Verify observability script is working
- Check data source connections
- Ensure proper permissions

**High Resource Usage**
- Reduce refresh rate
- Limit active panels
- Use filtered views

**Display Problems**
- Resize terminal window
- Check terminal compatibility
- Update Rich library

## Best Practices

1. **Regular Monitoring**
   - Start each day with `/monitor status`
   - Keep `/monitor live` running during critical operations
   - Review `/monitor metrics` weekly

2. **Alert Response**
   - Address critical alerts immediately
   - Investigate warning trends
   - Document resolution steps

3. **Performance Optimization**
   - Use appropriate refresh rates
   - Filter unnecessary data
   - Export for offline analysis

## Technical Details

### Backend Architecture
- Python-based observability script
- Rich library for formatting
- Real-time data aggregation
- Efficient state management

### Performance
- Optimized for minimal overhead
- Cached computations
- Batch data fetching
- Progressive rendering

## Future Enhancements

- Machine learning predictions
- Anomaly detection
- Custom dashboard layouts
- Mobile app integration
- Historical trend analysis
- Automated remediation

## Support

For issues or feature requests related to monitoring commands:
1. Check this documentation
2. Review the observability script logs
3. Test individual components
4. Report issues with error details

## Related Commands

- `/orchestrate` - Manage agent orchestration
- `/task` - Task management
- `/sprint` - Sprint planning
- `/team` - Team coordination