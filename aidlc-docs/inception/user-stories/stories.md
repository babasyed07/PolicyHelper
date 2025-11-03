# Policy Helper - User Stories

## Primary User Personas

### Business Analyst (Sarah)
- **Role**: Defines access control requirements
- **Technical Level**: Low-Medium
- **Primary Interface**: Web chatbot
- **Goals**: Quick policy generation from natural language

### Security Engineer (Mike)
- **Role**: Reviews and validates policies
- **Technical Level**: High
- **Primary Interface**: CLI + Web
- **Goals**: Ensure policy correctness and security compliance

### Developer (Alex)
- **Role**: Integrates policies into applications
- **Technical Level**: High
- **Primary Interface**: CLI
- **Goals**: Batch processing and automation

## User Stories

### Epic 1: Schema Management
**US-001**: Schema Upload
```
As a Security Engineer
I want to upload my Cedar schema JSON file
So that Policy Helper understands my application's entities and actions
```
**Status**: ✅ IMPLEMENTED
**Acceptance Criteria**:
- [x] CLI accepts schema file parameter
- [x] Web interface uses default schema
- [x] Schema parsing validates JSON structure
- [x] Entity and action extraction works

**US-002**: Schema Validation
```
As a Security Engineer  
I want to validate my Cedar schema before use
So that I can catch schema errors early
```
**Status**: 🔄 PARTIAL (basic parsing only)

### Epic 2: Policy Generation
**US-003**: Natural Language Input
```
As a Business Analyst
I want to describe access rules in plain English
So that I can generate policies without learning Cedar syntax
```
**Status**: ✅ IMPLEMENTED
**Acceptance Criteria**:
- [x] CLI accepts requirement string
- [x] Web interface has text input
- [x] Bedrock processes natural language
- [x] Context from schema included in prompts

**US-004**: Policy Output
```
As a Business Analyst
I want to receive valid Cedar policy code
So that I can use it in my application
```
**Status**: ✅ IMPLEMENTED
**Acceptance Criteria**:
- [x] Cedar policy syntax generated
- [x] 3-bullet rationale provided
- [x] Formatted output in both interfaces

### Epic 3: Policy Review
**US-005**: Policy Validation
```
As a Security Engineer
I want to validate generated policies
So that I can ensure they are syntactically correct
```
**Status**: ❌ NOT IMPLEMENTED

**US-006**: Rationale Review
```
As a Security Engineer
I want to see detailed rationale for policies
So that I can validate business logic
```
**Status**: ✅ IMPLEMENTED
**Acceptance Criteria**:
- [x] 3-bullet explanations provided
- [x] Business impact described
- [x] Security implications noted

### Epic 4: History Management
**US-007**: Save Policy History
```
As a Team Member
I want to save generated policies
So that I can track changes and reuse patterns
```
**Status**: ✅ IMPLEMENTED
**Acceptance Criteria**:
- [x] Automatic saving after generation
- [x] Timestamp and requirement stored
- [x] JSON persistence working

**US-008**: Browse History
```
As a Team Member
I want to browse previous policies
So that I can find and reuse existing work
```
**Status**: ✅ IMPLEMENTED
**Acceptance Criteria**:
- [x] History viewer utility
- [x] List and detail views
- [x] Search by index

### Epic 5: Export and Integration
**US-009**: Export Policies
```
As a Developer
I want to export policies in different formats
So that I can integrate them into my build process
```
**Status**: ❌ NOT IMPLEMENTED

**US-010**: Batch Processing
```
As a Developer
I want to process multiple requirements at once
So that I can automate policy generation
```
**Status**: ❌ NOT IMPLEMENTED

## Story Mapping

### MVP (Completed) ✅
- Schema ingestion (US-001)
- Natural language input (US-003)
- Policy output (US-004)
- Rationale review (US-006)
- Save history (US-007)
- Browse history (US-008)

### Phase 2 (Enhancement)
- Schema validation (US-002)
- Policy validation (US-005)
- Export policies (US-009)

### Phase 3 (Advanced)
- Batch processing (US-010)
- Advanced search
- User authentication
- API integration