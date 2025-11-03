# Policy Helper - Enhanced Application Plan & Modeling

## Enhanced System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │ Enhanced Web UI │    │  CLI Interface  │
│                 │    │                 │    │                 │
│ • Requirements  │    │ • Chat Interface│    │ • Command Line  │
│ • Schema Files  │    │ • Accept/Reject │    │ • Batch Process │
│ • Chat Messages │    │ • Recommendations│    │ • Validation    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │  Enhanced Policy Engine   │
                    │                           │
                    │ • Policy Generation       │
                    │ • Recommendation Engine   │
                    │ • Chat Management         │
                    │ • Approval Workflow       │
                    └─────────────┬─────────────┘
                                 │
    ┌─────────────────────────────┼─────────────────────────────┐
    │                             │                             │
┌───▼────┐  ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐  ┌───▼────┐
│Schema  │  │ Bedrock   │  │ Policy    │  │ Chat      │  │History │
│Parser  │  │ Client    │  │ Validator │  │ Manager   │  │Manager │
│        │  │           │  │           │  │           │  │        │
│•Parsing│  │•AI Calls  │  │•Syntax    │  │•Context   │  │•Storage│
│•Recomm │  │•Prompts   │  │•Testing   │  │•Sessions  │  │•Approval│
└────────┘  └───────────┘  └───────────┘  └───────────┘  └────────┘
```

## Enhanced Data Models

### 1. Cedar Schema Model (Existing)
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

### 2. Enhanced Policy Models
```python
PolicyRequest {
    requirement: str
    schema_context: SchemaContext
    chat_session_id: Optional[str]  # NEW
    timestamp: datetime
}

PolicyResponse {
    cedar_policy: str
    rationale: List[str]
    confidence: float
    validation_result: ValidationResult  # ENHANCED
    requires_approval: bool  # NEW
}

ValidationResult {  # NEW
    is_valid: bool
    syntax_errors: List[str]
    test_results: List[TestResult]
    warnings: List[str]
}

TestResult {  # NEW
    test_case: str
    expected: str
    actual: str
    passed: bool
}
```

### 3. Policy Recommendation Models (NEW)
```python
PolicyRecommendation {
    id: str
    title: str
    description: str
    priority: int  # 1-5
    category: str  # "access_control", "security", "compliance"
    template_policy: str
    rationale: List[str]
    applicable_entities: List[str]
    applicable_actions: List[str]
}

RecommendationSet {
    schema_hash: str
    recommendations: List[PolicyRecommendation]
    generated_at: datetime
}
```

### 4. Chat Session Models (NEW)
```python
ChatSession {
    session_id: str
    user_id: Optional[str]
    created_at: datetime
    last_activity: datetime
    context: Dict  # Conversation context
    messages: List[ChatMessage]
}

ChatMessage {
    id: str
    session_id: str
    timestamp: datetime
    sender: str  # "user" or "assistant"
    content: str
    message_type: str  # "text", "policy", "recommendation"
    metadata: Optional[Dict]
}
```

### 5. Enhanced History Model
```python
PolicyHistory {
    id: int
    timestamp: datetime
    requirement: str
    policy: str
    rationale: List[str]
    schema_file: str
    user_decision: UserDecision  # NEW
    chat_session_id: Optional[str]  # NEW
    validation_result: ValidationResult  # NEW
}

UserDecision {  # NEW
    decision: str  # "accepted", "rejected", "pending"
    timestamp: datetime
    feedback: Optional[str]
    rejection_reason: Optional[str]
}
```

## Enhanced Component Design

### 1. Enhanced Schema Parser Component
```
Responsibilities:
- Parse Cedar schema JSON files
- Extract entity types and actions
- Generate policy recommendations  # NEW
- Validate schema structure
- Provide context for policy generation

Interface:
- load_schema(file_path) -> bool
- get_entities() -> List[str]
- get_actions() -> List[str]
- get_context() -> SchemaContext
- generate_recommendations() -> RecommendationSet  # NEW
```

### 2. Enhanced Policy Generator Component
```
Responsibilities:
- Process natural language requirements
- Build prompts with schema context
- Handle conversational context  # NEW
- Call Amazon Bedrock API
- Parse and validate responses

Interface:
- generate_policy(requirement, schema, context) -> PolicyResponse
- generate_with_chat_context(requirement, session) -> PolicyResponse  # NEW
- validate_policy(policy) -> ValidationResult  # ENHANCED
- parse_response(raw_response) -> PolicyResponse
```

### 3. Policy Validator Component (NEW)
```
Responsibilities:
- Validate Cedar policy syntax
- Test policies against schema
- Generate test cases
- Report validation results

Interface:
- validate_syntax(policy) -> bool
- validate_against_schema(policy, schema) -> ValidationResult
- generate_test_cases(policy, schema) -> List[TestCase]
- run_tests(policy, test_cases) -> List[TestResult]
```

### 4. Chat Manager Component (NEW)
```
Responsibilities:
- Manage chat sessions
- Maintain conversation context
- Handle multi-turn conversations
- Store chat history

Interface:
- create_session(user_id) -> str
- add_message(session_id, message) -> bool
- get_context(session_id) -> Dict
- update_context(session_id, context) -> bool
- get_session_history(session_id) -> List[ChatMessage]
```

### 5. Approval Workflow Component (NEW)
```
Responsibilities:
- Manage policy approval process
- Track user decisions
- Handle accept/reject workflow
- Collect feedback

Interface:
- present_for_approval(policy_response) -> str
- record_decision(policy_id, decision, feedback) -> bool
- get_pending_approvals() -> List[PolicyResponse]
- get_approval_stats() -> Dict
```

### 6. Enhanced Bedrock Client Component
```
Responsibilities:
- Manage AWS authentication
- Handle conversational prompts  # NEW
- Handle API rate limiting
- Process model responses
- Error handling and retries

Interface:
- generate_text(prompt) -> str
- generate_with_context(prompt, context) -> str  # NEW
- generate_recommendations(schema) -> str  # NEW
- configure_model(model_id, params) -> bool
- check_connection() -> bool
```

### 7. Enhanced History Manager Component
```
Responsibilities:
- Persist policy generation history
- Track approval decisions  # NEW
- Store chat sessions  # NEW
- Provide search and retrieval
- Export capabilities
- Data cleanup

Interface:
- save_policy(request, response, decision) -> int  # ENHANCED
- save_chat_session(session) -> bool  # NEW
- get_history() -> List[PolicyHistory]
- get_approved_policies() -> List[PolicyHistory]  # NEW
- search_policies(query) -> List[PolicyHistory]
- export_history(format) -> str
```

## Enhanced Application Flows

### Enhanced CLI Workflow
```
1. Parse command line arguments
2. Load schema file (default or specified)
3. Generate recommendations (if --recommend flag)  # NEW
4. Initialize components with validation  # ENHANCED
5. Process requirement through generator
6. Validate generated policy  # NEW
7. Present for approval (if interactive mode)  # NEW
8. Display formatted output
9. Save to history with decision  # ENHANCED
10. Exit with status code
```

### Enhanced Web Workflow
```
1. Start Flask application
2. Load default schema
3. Generate initial recommendations  # NEW
4. Serve enhanced chat interface  # ENHANCED
5. Handle AJAX requests:
   - POST /chat -> handle chat messages  # NEW
   - POST /generate -> process requirement with validation  # ENHANCED
   - POST /approve -> handle policy approval  # NEW
   - POST /reject -> handle policy rejection  # NEW
   - GET /recommendations -> return schema recommendations  # NEW
   - GET /history -> return approved policies only  # ENHANCED
   - GET /sessions -> return chat sessions  # NEW
6. Return JSON responses with validation results
```

### New: Schema Ingestion Workflow
```
1. User uploads/specifies schema file
2. Parse and validate schema structure
3. Generate policy recommendations automatically
4. Present recommendations with priorities
5. Allow user to select recommendations for generation
6. Generate detailed policies for selected recommendations
7. Present for approval workflow
```

### New: Chat Conversation Workflow
```
1. Create or resume chat session
2. User sends message/requirement
3. Extract context from conversation history
4. Generate policy with conversational context
5. Validate policy before presentation
6. Present policy with approval options
7. Handle user feedback and refinement requests
8. Update conversation context
9. Continue iterative refinement
```

### New: Policy Approval Workflow
```
1. Generate policy (via any method)
2. Validate policy syntax and logic
3. Present policy with validation results
4. Show Accept/Reject buttons with rationale
5. If Accept: Save to history with approval timestamp
6. If Reject: Collect feedback, discard policy
7. Update approval statistics
8. Optionally regenerate based on feedback
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

## Enhanced Testing Strategy

### Unit Tests
- Schema parser validation
- Policy response parsing
- Policy validation logic  # NEW
- Chat session management  # NEW
- Recommendation generation  # NEW
- Approval workflow logic  # NEW
- History CRUD operations
- Error handling paths

### Integration Tests
- End-to-end CLI workflow with validation  # ENHANCED
- Enhanced web chat interface  # ENHANCED
- Policy approval workflow  # NEW
- Recommendation generation flow  # NEW
- AWS Bedrock connectivity
- File system operations
- Chat session persistence  # NEW

### User Acceptance Tests
- Business analyst chat workflows  # ENHANCED
- Security engineer policy validation  # ENHANCED
- Recommendation usefulness testing  # NEW
- Approval workflow usability  # NEW
- Developer integration scenarios
- Performance benchmarks

### New: Policy Validation Tests
- Cedar syntax validation accuracy
- Schema compliance testing
- Test case generation quality
- Validation performance benchmarks

## Enhanced Deployment Plan

### Phase 1: Core Enhancements (Current)
- Policy validation integration
- Basic recommendation engine
- Simple approval workflow
- Enhanced web interface with chat

### Phase 2: Advanced Features
- Full conversational chat interface
- Comprehensive policy testing
- Advanced recommendation algorithms
- Approval workflow with feedback collection

### Phase 3: Production Ready
- Database storage for sessions and approvals
- User authentication and authorization
- Advanced chat context management
- Monitoring and analytics
- CI/CD pipeline with validation tests

## Enhanced Monitoring & Observability

### Enhanced Metrics
- Policy generation success rate
- Policy validation accuracy  # NEW
- Recommendation relevance scores  # NEW
- Approval vs rejection rates  # NEW
- Chat session engagement metrics  # NEW
- Average response time
- Error frequency by type
- User adoption metrics

### Enhanced Logging
- Request/response pairs
- Policy validation results  # NEW
- User approval decisions  # NEW
- Chat conversation flows  # NEW
- Recommendation generation  # NEW
- Error details with context
- Performance measurements
- User interaction patterns

### Enhanced Alerting
- AWS API failures
- Policy validation failures  # NEW
- High rejection rates  # NEW
- Chat session errors  # NEW
- High error rates
- Performance degradation
- Security incidents