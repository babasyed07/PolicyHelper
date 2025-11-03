# Integration Test Instructions

## Purpose
Test interactions between PolicyHelper components to ensure they work together correctly.

## Test Scenarios

### Scenario 1: CLI → Bedrock → Policy Generation
- **Description**: Test complete CLI workflow from input to policy output
- **Setup**: Ensure AWS credentials configured or mock mode available
- **Test Steps**: 
  1. Run: `python policy_helper.py "Allow managers to view accounts"`
  2. Verify policy output format
  3. Check rationale generation
- **Expected Results**: Valid Cedar policy with 3-bullet rationale
- **Cleanup**: None required

### Scenario 2: Web App → Backend Services Integration
- **Description**: Test web interface to backend service integration
- **Setup**: Start web application
- **Test Steps**:
  1. Run: `python web_app.py`
  2. Navigate to http://localhost:5000
  3. Submit policy request through web form
  4. Verify response display
- **Expected Results**: Policy displayed in web interface
- **Cleanup**: Stop web server (Ctrl+C)

### Scenario 3: Schema Parser → Policy Generator Integration
- **Description**: Test schema parsing with policy generation
- **Setup**: Ensure sample_banking_schema.json exists
- **Test Steps**:
  1. Load schema via schema_parser.py
  2. Generate policy using parsed schema context
  3. Verify schema entities referenced in policy
- **Expected Results**: Policy references correct schema entities
- **Cleanup**: None required

## Setup Integration Test Environment

### 1. Start Required Services
```bash
# No external services required - self-contained application
source venv/bin/activate
```

### 2. Configure Service Endpoints
```bash
# Set AWS region for Bedrock
export AWS_DEFAULT_REGION=us-east-1
```

## Run Integration Tests

### 1. Execute Integration Test Suite
```bash
# Test CLI integration
python policy_helper.py "Test policy request"

# Test web integration (in separate terminal)
python web_app.py &
curl -X POST http://localhost:5000/generate -d "requirement=Test policy" -H "Content-Type: application/x-www-form-urlencoded"
```

### 2. Verify Service Interactions
- **Test Scenarios**: CLI, Web, Schema parsing workflows
- **Expected Results**: Consistent policy generation across interfaces
- **Logs Location**: Console output

### 3. Cleanup
```bash
# Stop any running web servers
pkill -f web_app.py
```