from bedrock_client import generate_text
from schema_parser import SchemaParser
from policy_validator import PolicyValidator
from policy_recommender import PolicyRecommender
import json

class PolicyGenerator:
    def __init__(self, schema_path=None):
        self.parser = SchemaParser()
        self.validator = PolicyValidator()
        if schema_path:
            self.parser.load_schema(schema_path)
            self.recommender = PolicyRecommender(self.parser.get_schema_context())
    
    def generate_policy(self, requirement, conversation_context=""):
        schema_context = self.parser.get_schema_context()
        
        # Enhanced prompt with conversation context
        prompt = f"""You are a Cedar policy expert for banking applications.

Schema Context:
- Available Entities: {schema_context['entities']}
- Available Actions: {schema_context['actions']}

{f'Previous Conversation:{conversation_context}' if conversation_context else ''}

Current Requirement: {requirement}

Generate a Cedar policy using correct syntax:

Correct Cedar Policy Format:
- Use: permit() or forbid()
- Principal: principal (for any) or principal == EntityType::"id"
- Action: action == Action::"ActionName"
- Resource: resource (for any) or resource == EntityType::"id"
- Conditions: when {{ condition }}

Example:
forbid(
  principal,
  action == Action::"CreateTransaction",
  resource
)
when {{
  resource.amount >= 5000
}};

Generate response in this format:

POLICY:
[Cedar policy code here]

RATIONALE:
• [reason 1]
• [reason 2]
• [reason 3]"""

        return generate_text(prompt)
    
    def generate_and_validate_policy(self, requirement, conversation_context=""):
        """Generate policy with validation before returning"""
        response = self.generate_policy(requirement, conversation_context)
        parsed = self.parse_response(response)
        
        # Validate the generated policy
        schema_context = self.parser.get_schema_context()
        is_valid, errors = self.validator.validate_policy(parsed['policy'], schema_context)
        
        # Generate test cases
        test_cases = self.validator.generate_test_cases(parsed['policy'])
        
        return {
            'policy': parsed['policy'],
            'rationale': parsed['rationale'],
            'validation': {
                'is_valid': is_valid,
                'errors': errors,
                'test_cases': test_cases
            }
        }
    
    def get_recommendations(self):
        """Get policy recommendations based on schema"""
        if hasattr(self, 'recommender'):
            return self.recommender.generate_recommendations()
        return []
    
    def parse_response(self, response):
        lines = response.strip().split('\n')
        policy_section = []
        rationale_section = []
        current_section = None
        
        for line in lines:
            if line.strip() == 'POLICY:':
                current_section = 'policy'
                continue
            elif line.strip() == 'RATIONALE:':
                current_section = 'rationale'
                continue
            
            if current_section == 'policy' and line.strip():
                policy_section.append(line)
            elif current_section == 'rationale' and line.strip():
                rationale_section.append(line.strip())
        
        return {
            'policy': '\n'.join(policy_section),
            'rationale': rationale_section
        }