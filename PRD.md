# Policy Helper - Product Requirements Document

## Executive Summary

Policy Helper is an AI-powered tool that converts plain English access control requirements into Cedar policy snippets with explanatory rationales for banking applications.

## Problem Statement

Writing Cedar policies requires deep technical knowledge of policy syntax and banking domain expertise. Business stakeholders struggle to translate access control requirements into proper Cedar policy format, leading to:
- Misconfigured access controls
- Security vulnerabilities
- Development delays
- Communication gaps between business and technical teams

## Solution Overview

An intelligent assistant that bridges the gap between business requirements and technical Cedar policy implementation using Amazon Bedrock's natural language processing capabilities.

## Core Features

### 1. Cedar Schema Ingestion
- **Input**: JSON format Cedar schema for banking applications
- **Processing**: Parse and understand entity types, actions, and relationships
- **Output**: Internal schema representation for policy generation context

### 2. Natural Language to Cedar Policy Translation
- **Input**: Plain English requirements (e.g., "Deny Account Holder from creating transactions >= 5000")
- **Processing**: Use Amazon Bedrock to interpret intent and generate Cedar policy
- **Output**: Valid Cedar policy snippet with explanatory notes

### 3. Policy Generation & Reasoning
- **Cedar Policy Block**: Syntactically correct Cedar policy
- **Rationale Notes**: 3-bullet explanation of policy logic and business impact
- **Validation**: Ensure policy aligns with ingested schema

### 4. User Interfaces
- **CLI Interface**: Command-line tool for developer workflows
- **Web Chatbot**: Browser-based interface for business users
- **Both interfaces**: Call Amazon Bedrock for AI-powered policy generation

### 5. History & Management
- **Save History**: Store generated policies and requirements
- **Regenerate**: Re-process requirements with different parameters
- **Export**: Output policies in various formats

## Technical Requirements

### Core Components
1. **Schema Parser**: JSON Cedar schema ingestion and validation
2. **Bedrock Client**: Amazon Bedrock integration for NLP processing
3. **Policy Generator**: Cedar policy syntax generation and validation
4. **Storage Layer**: History persistence (JSON/SQLite)
5. **CLI Interface**: Command-line application
6. **Web Interface**: Simple chatbot UI

### Dependencies
- Python 3.8+
- boto3 (AWS SDK)
- Cedar policy validation library
- Flask/FastAPI (web interface)
- SQLite (history storage)

## User Stories

### Primary Users
- **Business Analysts**: Define access control requirements in natural language
- **Security Engineers**: Review and validate generated policies
- **Developers**: Integrate policies into banking applications

### User Workflows

#### Story 1: Schema Setup
```
As a security engineer
I want to upload my banking Cedar schema
So that Policy Helper understands my application's entities and actions
```

#### Story 2: Policy Generation
```
As a business analyst
I want to describe access rules in plain English
So that I can get valid Cedar policies without learning syntax
```

#### Story 3: Policy Review
```
As a security engineer
I want to see rationale for generated policies
So that I can validate business logic and security implications
```

#### Story 4: History Management
```
As a team member
I want to save and retrieve previous policy generations
So that I can track changes and reuse common patterns
```

## Success Metrics

### Functional Metrics
- **Policy Accuracy**: 95% of generated policies are syntactically valid
- **Schema Compatibility**: 100% compliance with ingested Cedar schema
- **Response Time**: <5 seconds for policy generation

### User Experience Metrics
- **Adoption Rate**: 80% of team members use tool within 30 days
- **Time Savings**: 70% reduction in policy creation time
- **Error Reduction**: 50% fewer policy-related security issues

## Implementation Phases

### Phase 1: Core Engine (Week 1-2)
- Cedar schema parser
- Bedrock integration
- Basic policy generation
- CLI interface

### Phase 2: Enhanced Features (Week 3)
- History storage
- Policy validation
- Improved prompting
- Error handling

### Phase 3: Web Interface (Week 4)
- Web chatbot UI
- User authentication
- Export capabilities
- Documentation

## Risk Mitigation

### Technical Risks
- **Bedrock API Limits**: Implement rate limiting and caching
- **Policy Validation**: Use Cedar validation libraries
- **Schema Complexity**: Start with simple banking schemas

### Business Risks
- **Accuracy Concerns**: Provide clear disclaimers about AI-generated content
- **Security Impact**: Require human review for production policies
- **Adoption Barriers**: Provide comprehensive documentation and examples

## Success Criteria

### Minimum Viable Product (MVP)
- ✅ Ingest Cedar schema JSON
- ✅ Convert natural language to Cedar policy
- ✅ Generate 3-bullet rationale
- ✅ CLI interface functional
- ✅ Basic history storage

### Enhanced Product (Current Enhancements)
- 🔄 Schema-based policy recommendations
- 🔄 Accept/Reject approval workflow
- 🔄 Conversational chat interface
- 🔄 Comprehensive policy validation
- 🔄 Policy testing before presentation

### Full Product
- ✅ Web chatbot interface
- 🔄 Advanced policy validation (Enhanced)
- ✅ Export capabilities
- ✅ Comprehensive error handling
- ✅ Production-ready security measures
- 🔄 User decision tracking and analytics

## Appendix

### Example Input/Output

**Input Schema**: Banking Cedar schema with Account, Transaction, User entities

**Input Requirement**: "Deny Account Holder from creating transactions >= 5000"

**Output Policy**:
```cedar
forbid (
  principal == User::"AccountHolder",
  action == Action::"CreateTransaction",
  resource
) when {
  resource.amount >= 5000
};
```

**Output Rationale**:
• Prevents account holders from initiating high-value transactions above $5000 threshold
• Reduces fraud risk by requiring additional authorization for large transactions  
• Aligns with banking regulations requiring enhanced controls for significant monetary transfers

## Enhancement Notes

### 1. Schema Ingestion → Policy Recommendations
Once the Cedar schema in JSON format is ingested, the system should automatically generate policy recommendations based on:
- Common banking access control patterns
- Entity-action relationships in the schema
- Security best practices for financial applications
- Regulatory compliance requirements

Recommendations will be presented with priority levels and rationale, allowing users to select which policies to generate in detail.

### 2. Accept/Reject Policy Workflow
The user should be able to Accept the Cedar Policy and Save it, or have the ability to Reject it:
- **Accept**: Policy is saved to history with approval timestamp and user confirmation
- **Reject**: Policy is discarded, optional feedback collected for improvement
- **Approval Tracking**: System maintains statistics on approval/rejection rates
- **Feedback Loop**: Rejection feedback used to improve future policy generation

### 3. Natural Language Chat Interface
Users should be able to give business intent in Natural language to the Chat to generate Cedar policies:
- **Conversational Context**: Multi-turn conversations with context retention
- **Iterative Refinement**: Users can refine policies through follow-up questions
- **Session Management**: Chat sessions persist during user interaction
- **Context Awareness**: System remembers previous exchanges within session

### 4. Policy Testing and Validation
The Cedar Policy generated in steps 2 or 3 should be tested and validated before it presents to the user:
- **Syntax Validation**: Verify Cedar policy syntax correctness
- **Schema Compliance**: Ensure policy aligns with loaded schema entities and actions
- **Test Case Generation**: Automatically generate test scenarios based on policy logic
- **Validation Reporting**: Present clear pass/fail status with detailed feedback
- **Quality Gate**: Only validated policies are presented to users for approval