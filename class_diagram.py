#!/usr/bin/env python3
"""
Policy Helper - Class Diagram Implementation
Demonstrates the object-oriented design based on the application plan
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

# Enums
class PolicyType(Enum):
    PERMIT = "permit"
    FORBID = "forbid"

class ValidationStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"

class UserDecisionType(Enum):  # NEW
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PENDING = "pending"

class MessageType(Enum):  # NEW
    TEXT = "text"
    POLICY = "policy"
    RECOMMENDATION = "recommendation"

class RecommendationCategory(Enum):  # NEW
    ACCESS_CONTROL = "access_control"
    SECURITY = "security"
    COMPLIANCE = "compliance"

# Data Models
@dataclass
class EntityType:
    name: str
    member_of_types: List[str]
    attributes: Dict[str, str]

@dataclass
class Action:
    name: str
    principal_types: List[str]
    resource_types: List[str]
    context: Optional[Dict] = None

@dataclass
class SchemaContext:
    entities: List[str]
    actions: List[str]
    entity_details: Dict[str, EntityType]
    action_details: Dict[str, Action]

@dataclass
class PolicyRequest:
    requirement: str
    schema_context: SchemaContext
    timestamp: datetime

@dataclass
class ValidationResult:  # NEW
    is_valid: bool
    syntax_errors: List[str]
    test_results: List['TestResult']
    warnings: List[str]

@dataclass
class TestResult:  # NEW
    test_case: str
    expected: str
    actual: str
    passed: bool

@dataclass
class PolicyResponse:
    cedar_policy: str
    rationale: List[str]
    confidence: float
    validation_result: ValidationResult  # ENHANCED
    requires_approval: bool  # NEW

@dataclass
class PolicyRecommendation:  # NEW
    id: str
    title: str
    description: str
    priority: int
    category: RecommendationCategory
    template_policy: str
    rationale: List[str]
    applicable_entities: List[str]
    applicable_actions: List[str]

@dataclass
class ChatSession:  # NEW
    session_id: str
    user_id: Optional[str]
    created_at: datetime
    last_activity: datetime
    context: Dict
    messages: List['ChatMessage']

@dataclass
class ChatMessage:  # NEW
    id: str
    session_id: str
    timestamp: datetime
    sender: str
    content: str
    message_type: MessageType
    metadata: Optional[Dict]

@dataclass
class UserDecision:  # NEW
    decision: UserDecisionType
    timestamp: datetime
    feedback: Optional[str]
    rejection_reason: Optional[str]

@dataclass
class PolicyHistory:
    id: int
    timestamp: datetime
    requirement: str
    policy: str
    rationale: List[str]
    schema_file: str
    user_decision: UserDecision  # NEW
    chat_session_id: Optional[str] = None  # NEW
    validation_result: Optional[ValidationResult] = None  # NEW
    user_feedback: Optional[str] = None

# Abstract Interfaces
class ISchemaParser(ABC):
    @abstractmethod
    def load_schema(self, file_path: str) -> bool:
        pass
    
    @abstractmethod
    def get_context(self) -> SchemaContext:
        pass
    
    @abstractmethod
    def generate_recommendations(self) -> List[PolicyRecommendation]:  # NEW
        pass

class IPolicyGenerator(ABC):
    @abstractmethod
    def generate_policy(self, requirement: str, context: Optional[Dict] = None) -> PolicyResponse:  # ENHANCED
        pass
    
    @abstractmethod
    def generate_with_chat_context(self, requirement: str, session: ChatSession) -> PolicyResponse:  # NEW
        pass

class IPolicyValidator(ABC):  # NEW
    @abstractmethod
    def validate_syntax(self, policy: str) -> bool:
        pass
    
    @abstractmethod
    def validate_against_schema(self, policy: str, schema: SchemaContext) -> ValidationResult:
        pass
    
    @abstractmethod
    def generate_test_cases(self, policy: str, schema: SchemaContext) -> List[TestResult]:
        pass

class IBedrockClient(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass
    
    @abstractmethod
    def generate_with_context(self, prompt: str, context: Dict) -> str:  # NEW
        pass
    
    @abstractmethod
    def generate_recommendations(self, schema: SchemaContext) -> str:  # NEW
        pass
    
    @abstractmethod
    def check_connection(self) -> bool:
        pass

class IHistoryManager(ABC):
    @abstractmethod
    def save_policy(self, request: PolicyRequest, response: PolicyResponse, decision: UserDecision) -> int:  # ENHANCED
        pass
    
    @abstractmethod
    def save_chat_session(self, session: ChatSession) -> bool:  # NEW
        pass
    
    @abstractmethod
    def get_history(self) -> List[PolicyHistory]:
        pass
    
    @abstractmethod
    def get_approved_policies(self) -> List[PolicyHistory]:  # NEW
        pass

class IChatManager(ABC):  # NEW
    @abstractmethod
    def create_session(self, user_id: Optional[str] = None) -> str:
        pass
    
    @abstractmethod
    def add_message(self, session_id: str, message: ChatMessage) -> bool:
        pass
    
    @abstractmethod
    def get_context(self, session_id: str) -> Dict:
        pass
    
    @abstractmethod
    def update_context(self, session_id: str, context: Dict) -> bool:
        pass

class IApprovalWorkflow(ABC):  # NEW
    @abstractmethod
    def present_for_approval(self, policy_response: PolicyResponse) -> str:
        pass
    
    @abstractmethod
    def record_decision(self, policy_id: str, decision: UserDecision) -> bool:
        pass
    
    @abstractmethod
    def get_pending_approvals(self) -> List[PolicyResponse]:
        pass

# Core Classes
class CedarSchemaParser(ISchemaParser):
    def __init__(self):
        self.schema = None
        self.entities = {}
        self.actions = {}
    
    def load_schema(self, file_path: str) -> bool:
        # Implementation in schema_parser.py
        pass
    
    def get_context(self) -> SchemaContext:
        # Implementation in schema_parser.py
        pass
    
    def generate_recommendations(self) -> List[PolicyRecommendation]:  # NEW
        # Generate recommendations based on schema analysis
        pass

class BedrockPolicyGenerator(IPolicyGenerator):
    def __init__(self, schema_parser: ISchemaParser, bedrock_client: IBedrockClient, validator: IPolicyValidator):
        self.schema_parser = schema_parser
        self.bedrock_client = bedrock_client
        self.validator = validator  # NEW
    
    def generate_policy(self, requirement: str, context: Optional[Dict] = None) -> PolicyResponse:  # ENHANCED
        # Implementation in policy_generator.py
        pass
    
    def generate_with_chat_context(self, requirement: str, session: ChatSession) -> PolicyResponse:  # NEW
        # Generate policy with conversational context
        pass

class CedarPolicyValidator(IPolicyValidator):  # NEW
    def __init__(self):
        pass
    
    def validate_syntax(self, policy: str) -> bool:
        # Cedar syntax validation
        pass
    
    def validate_against_schema(self, policy: str, schema: SchemaContext) -> ValidationResult:
        # Schema compliance validation
        pass
    
    def generate_test_cases(self, policy: str, schema: SchemaContext) -> List[TestResult]:
        # Generate and run test cases
        pass

class AWSBedrockClient(IBedrockClient):
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.client = None
    
    def generate_text(self, prompt: str) -> str:
        # Implementation in bedrock_client.py
        pass
    
    def generate_with_context(self, prompt: str, context: Dict) -> str:  # NEW
        # Generate with conversational context
        pass
    
    def generate_recommendations(self, schema: SchemaContext) -> str:  # NEW
        # Generate policy recommendations from schema
        pass
    
    def check_connection(self) -> bool:
        # AWS connectivity check
        pass

class JSONHistoryManager(IHistoryManager):
    def __init__(self, file_path: str = 'policy_history.json'):
        self.file_path = file_path
        self.history = []
        self.chat_sessions = {}  # NEW
    
    def save_policy(self, request: PolicyRequest, response: PolicyResponse, decision: UserDecision) -> int:  # ENHANCED
        # Implementation in history_manager.py
        pass
    
    def save_chat_session(self, session: ChatSession) -> bool:  # NEW
        # Save chat session data
        pass
    
    def get_history(self) -> List[PolicyHistory]:
        # Implementation in history_manager.py
        pass
    
    def get_approved_policies(self) -> List[PolicyHistory]:  # NEW
        # Return only approved policies
        pass

class ChatManager(IChatManager):  # NEW
    def __init__(self, history_manager: IHistoryManager):
        self.history_manager = history_manager
        self.active_sessions = {}
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        # Create new chat session
        pass
    
    def add_message(self, session_id: str, message: ChatMessage) -> bool:
        # Add message to session
        pass
    
    def get_context(self, session_id: str) -> Dict:
        # Get conversation context
        pass
    
    def update_context(self, session_id: str, context: Dict) -> bool:
        # Update conversation context
        pass

class ApprovalWorkflow(IApprovalWorkflow):  # NEW
    def __init__(self, history_manager: IHistoryManager):
        self.history_manager = history_manager
        self.pending_approvals = {}
    
    def present_for_approval(self, policy_response: PolicyResponse) -> str:
        # Present policy for user approval
        pass
    
    def record_decision(self, policy_id: str, decision: UserDecision) -> bool:
        # Record user's approval decision
        pass
    
    def get_pending_approvals(self) -> List[PolicyResponse]:
        # Get policies awaiting approval
        pass

# Enhanced Application Controllers
class CLIController:
    def __init__(self, policy_generator: IPolicyGenerator, history_manager: IHistoryManager, 
                 approval_workflow: IApprovalWorkflow, schema_parser: ISchemaParser):
        self.policy_generator = policy_generator
        self.history_manager = history_manager
        self.approval_workflow = approval_workflow  # NEW
        self.schema_parser = schema_parser  # NEW
    
    def process_requirement(self, requirement: str, schema_file: str) -> None:
        # Enhanced CLI workflow with validation and approval
        pass
    
    def show_recommendations(self, schema_file: str) -> None:  # NEW
        # Display schema-based recommendations
        pass

class WebController:
    def __init__(self, policy_generator: IPolicyGenerator, history_manager: IHistoryManager,
                 chat_manager: IChatManager, approval_workflow: IApprovalWorkflow, 
                 schema_parser: ISchemaParser):
        self.policy_generator = policy_generator
        self.history_manager = history_manager
        self.chat_manager = chat_manager  # NEW
        self.approval_workflow = approval_workflow  # NEW
        self.schema_parser = schema_parser  # NEW
    
    def chat_endpoint(self, session_id: str, message: str) -> Dict:  # NEW
        # Handle chat messages with context
        pass
    
    def generate_policy_endpoint(self, requirement: str, session_id: Optional[str] = None) -> Dict:  # ENHANCED
        # Enhanced policy generation with validation
        pass
    
    def approve_policy_endpoint(self, policy_id: str, decision: str, feedback: Optional[str] = None) -> Dict:  # NEW
        # Handle policy approval/rejection
        pass
    
    def get_recommendations_endpoint(self) -> List[Dict]:  # NEW
        # Return schema-based recommendations
        pass
    
    def get_history_endpoint(self) -> List[Dict]:
        # Return approved policies only
        pass

# Enhanced Factory Pattern for Dependency Injection
class PolicyHelperFactory:
    @staticmethod
    def create_cli_app(schema_file: str) -> CLIController:
        schema_parser = CedarSchemaParser()
        schema_parser.load_schema(schema_file)
        
        bedrock_client = AWSBedrockClient()
        policy_validator = CedarPolicyValidator()  # NEW
        policy_generator = BedrockPolicyGenerator(schema_parser, bedrock_client, policy_validator)  # ENHANCED
        history_manager = JSONHistoryManager()
        approval_workflow = ApprovalWorkflow(history_manager)  # NEW
        
        return CLIController(policy_generator, history_manager, approval_workflow, schema_parser)  # ENHANCED
    
    @staticmethod
    def create_web_app(schema_file: str) -> WebController:
        schema_parser = CedarSchemaParser()
        schema_parser.load_schema(schema_file)
        
        bedrock_client = AWSBedrockClient()
        policy_validator = CedarPolicyValidator()  # NEW
        policy_generator = BedrockPolicyGenerator(schema_parser, bedrock_client, policy_validator)  # ENHANCED
        history_manager = JSONHistoryManager()
        chat_manager = ChatManager(history_manager)  # NEW
        approval_workflow = ApprovalWorkflow(history_manager)  # NEW
        
        return WebController(policy_generator, history_manager, chat_manager, approval_workflow, schema_parser)  # ENHANCED

# Enhanced Usage Example
if __name__ == "__main__":
    # CLI Application with recommendations
    cli_app = PolicyHelperFactory.create_cli_app('sample_banking_schema.json')
    cli_app.show_recommendations('sample_banking_schema.json')  # NEW
    cli_app.process_requirement("Deny Account Holder from creating transactions >= 5000", "sample_banking_schema.json")
    
    # Web Application with chat
    web_app = PolicyHelperFactory.create_web_app('sample_banking_schema.json')
    session_id = web_app.chat_manager.create_session()  # NEW
    result = web_app.chat_endpoint(session_id, "Allow managers to view all accounts")  # NEW
    approval_result = web_app.approve_policy_endpoint("policy_123", "accepted")  # NEW