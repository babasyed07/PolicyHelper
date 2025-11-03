# Unit Test Execution

## Run Unit Tests

### 1. Execute All Unit Tests
```bash
# Run existing test files
python run_tests.py
python test_connection.py
python test_enhanced_features.py
python test_offline.py
```

### 2. Review Test Results
- **Expected**: All tests pass, 0 failures
- **Test Coverage**: Core functionality covered
- **Test Report Location**: Console output

### 3. Fix Failing Tests
If tests fail:
1. Review test output in console
2. Identify failing test cases
3. Fix code issues
4. Rerun tests until all pass

## Individual Test Execution

### Connection Tests
```bash
python test_connection.py
# Tests AWS Bedrock connectivity and fallback to mock
```

### Enhanced Features Tests
```bash
python test_enhanced_features.py
# Tests policy validation, recommendations, and approval workflow
```

### Offline Tests
```bash
python test_offline.py
# Tests mock policy generation without AWS dependencies
```