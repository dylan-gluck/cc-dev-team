---
description: Fix failing tests and resolve code review issues
argument-hint: [optional: specific test suite or issue]
---

## Test Fixing & Issue Resolution

Fix test failures and resolve issues for: ${ARGUMENTS:-"all failing tests"}

### Workflow

Use the fullstack-eng agent to:

1. **Identify Failures**
   - Run test suites to identify failures
   - Analyze error messages and stack traces
   - Categorize issues by type and severity

2. **Fix Test Failures**
   - Debug failing unit tests
   - Fix integration test issues
   - Resolve E2E test failures
   - Update tests for code changes
   - Add missing test coverage

3. **Address Review Feedback**
   - Fix critical security issues first
   - Resolve performance problems
   - Address code quality issues
   - Update documentation gaps
   - Implement suggested improvements

4. **Iterative Testing**
   - Run tests after each fix
   - Verify no regression
   - Ensure all tests pass
   - Check coverage metrics
   - Validate performance

### Fix Priority
1. Security vulnerabilities (immediate)
2. Failing tests (high)
3. Performance issues (high)
4. Code quality issues (medium)
5. Documentation (medium)
6. Suggestions (low)

### Validation Steps
After fixes:
- All tests must pass
- No new issues introduced
- Coverage maintained or improved
- Performance benchmarks met
- Documentation updated

### Deliverables
- All tests passing
- Issues resolved per priority
- Updated documentation
- Fix summary report
- Clean test execution log

Continue iterating until all tests pass and critical issues are resolved.