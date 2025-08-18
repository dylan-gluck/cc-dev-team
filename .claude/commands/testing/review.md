---
description: Conduct comprehensive code review and testing of recent changes
argument-hint: [optional: specific feature/area]
---

## Code Review & Testing

Conduct thorough review and testing of: ${ARGUMENTS:-"all recent changes"}

### Workflow

Use the tech-lead agent to:

1. **Code Review**
   - Review all recent changes with git diff
   - Check code consistency and style
   - Validate architectural decisions
   - Identify security vulnerabilities
   - Check performance implications
   - Verify error handling

2. **Test Validation**
   - Run all test suites
   - Check test coverage metrics
   - Validate E2E test scenarios
   - Review test quality
   - Identify missing test cases

3. **Cross-Agent Validation**
   - Verify UI/backend integration
   - Check API contract consistency
   - Validate data model alignment
   - Ensure documentation accuracy
   - Confirm error handling consistency

4. **Security Audit**
   - Check for SQL injection risks
   - Validate input sanitization
   - Review authentication/authorization
   - Check for exposed secrets
   - Validate CORS configuration

5. **Performance Review**
   - Check query optimization
   - Review caching strategies
   - Validate pagination implementation
   - Check for memory leaks
   - Review bundle sizes

### Deliverables
- Comprehensive review report
- List of critical issues (must fix)
- List of warnings (should fix)
- List of suggestions (nice to have)
- Security audit results
- Performance analysis
- Approval decision

### Approval Criteria
Code is approved only when:
- No critical security issues
- All tests passing
- Performance benchmarks met
- Documentation complete
- Code follows standards

If issues are found, provide specific requirements for fixes before re-review.