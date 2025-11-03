# Policy Helper - Application Plan & Modeling

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │  Web Interface  │    │  CLI Interface  │
│                 │    │                 │    │                 │
│ • Requirements  │    │ • Flask App     │    │ • Command Line  │
│ • Schema Files  │    │ • HTML/JS UI    │    │ • Batch Process │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │    Policy Generator       │
                    │                           │
                    │ • Requirement Processing  │
                    │ • Schema Context Builder  │
                    │ • Prompt Engineering      │
                    └─────────────┬─────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
┌─────────▼───────┐    ┌─────────▼───────┐    ┌─────────▼───────┐
│ Schema Parser   │    │ Bedrock Client  │    │ History Manager │
│                 │    │                 │    │                 │
│ • JSON Parsing  │    │ • AWS API Calls │    │ • JSON Storage  │
│ • Entity Extract│    │ • Model Invoke  │    │ • CRUD Ops      │
│ • Action Extract│    │ • Response Parse│    │ • Timestamps    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Models

### 1. Cedar Schema Model
```python
CedarSchema {
    entityTypes: Dict[str, EntityType]
    actions: Dict[str, Action]
    commonTypes: Dict[str, Type]
}

EntityType {
    memberOfTypes: List[str]
    shape: RecordType
}

Action {
    appliesTo: {
        principalTypes: List[str]
        resourceTypes: List[str]
        context: Optional[RecordType]
    }
}
```

### 2. Policy Generation Model
```python
PolicyRequest {
    requirement: str
    schema_context: SchemaContext
    timestamp: datetime
}

PolicyResponse {
    cedar_policy: str
    rationale: List[str]
    confidence: float
    validation_status: bool
}

SchemaContext {
    entities: List[str]
    actions: List[str]
    entity_details: Dict
    action_details: Dict
}
```

### 3. History Model
```python
PolicyHistory {
    id: int
    timestamp: datetime
    requirement: str
    policy: str
    rationale: List[str]
    schema_file: str
    user_feedback: Optional[str]
}
```

## Component Design

### 1. Schema Parser Component
```
Responsibilities:
- Parse Cedar schema JSON files
- Extract entity types and actions
- Validate schema structure
- Provide context for policy generation

Interface:
- load_schema(file_path) -> bool
- get_entities() -> List[str]
- get_actions() -> List[str]
- get_context() -> SchemaContext
```

### 2. Policy Generator Component
```
Responsibilities:
- Process natural language requirements
- Build prompts with schema context
- Call Amazon Bedrock API
- Parse and validate responses

Interface:
- generate_policy(requirement, schema) -> PolicyResponse
- validate_policy(policy) -> bool
- parse_response(raw_response) -> PolicyResponse
```

### 3. Bedrock Client Component
```
Responsibilities:
- Manage AWS authentication
- Handle API rate limiting
- Process model responses
- Error handling and retries

Interface:
- generate_text(prompt) -> str
- configure_model(model_id, params) -> bool
- check_connection() -> bool
```

### 4. History Manager Component
```
Responsibilities:
- Persist policy generation history
- Provide search and retrieval
- Export capabilities
- Data cleanup

Interface:
- save_policy(request, response) -> int
- get_history() -> List[PolicyHistory]
- search_policies(query) -> List[PolicyHistory]
- export_history(format) -> str
```

## Application Flow

### CLI Workflow
```
1. Parse command line arguments
2. Load schema file (default or specified)
3. Initialize components
4. Process requirement through generator
5. Display formatted output
6. Save to history
7. Exit with status code
```

### Web Workflow
```
1. Start Flask application
2. Load default schema
3. Serve HTML interface
4. Handle AJAX requests:
   - POST /generate -> process requirement
   - GET /history -> return saved policies
   - GET /schema -> return current schema
5. Return JSON responses
```

## Error Handling Strategy

### Input Validation
- Requirement text: non-empty, reasonable length
- Schema files: valid JSON, Cedar format
- File paths: existence, permissions

### AWS Integration
- Credential validation
- Network connectivity
- API rate limits
- Model availability

### Response Processing
- Parse errors in generated policies
- Malformed JSON responses
- Missing rationale sections
- Invalid Cedar syntax

## Security Considerations

### Data Protection
- No sensitive data in logs
- Secure credential storage
- Input sanitization
- Output validation

### Access Control
- File system permissions
- AWS IAM policies
- Web interface authentication (future)
- API rate limiting

## Performance Requirements

### Response Times
- CLI: < 10 seconds end-to-end
- Web: < 5 seconds for policy generation
- History: < 1 second for retrieval

### Scalability
- Support 100+ concurrent web users
- Handle schemas with 50+ entities
- Store 10,000+ policy history entries

### Resource Usage
- Memory: < 512MB baseline
- Disk: < 100MB for application
- Network: Bedrock API calls only

## Testing Strategy

### Unit Tests
- Schema parser validation
- Policy response parsing
- History CRUD operations
- Error handling paths

### Integration Tests
- End-to-end CLI workflow
- Web interface functionality
- AWS Bedrock connectivity
- File system operations

### User Acceptance Tests
- Business analyst workflows
- Security engineer reviews
- Developer integration scenarios
- Performance benchmarks

## Deployment Plan

### Phase 1: Local Development
- CLI interface working
- Basic web interface
- File-based history storage
- Sample schema included

### Phase 2: Enhanced Features
- Advanced error handling
- Policy validation
- Export capabilities
- Improved UI/UX

### Phase 3: Production Ready
- Database storage
- User authentication
- Monitoring and logging
- CI/CD pipeline

## Monitoring & Observability

### Metrics
- Policy generation success rate
- Average response time
- Error frequency by type
- User adoption metrics

### Logging
- Request/response pairs
- Error details with context
- Performance measurements
- User interaction patterns

### Alerting
- AWS API failures
- High error rates
- Performance degradation
- Security incidents