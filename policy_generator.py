from bedrock_client import generate_text
from schema_parser import SchemaParser
import json

class PolicyGenerator:
    def __init__(self, schema_path=None):
        self.parser = SchemaParser()
        if schema_path:
            self.parser.load_schema(schema_path)
    
    def generate_policy(self, requirement):
        schema_context = self.parser.get_schema_context()
        
        prompt = f"""You are a Cedar policy expert for banking applications.

Schema Context:
- Available Entities: {schema_context['entities']}
- Available Actions: {schema_context['actions']}

Requirement: {requirement}

Generate a Cedar policy and rationale in this exact format:

POLICY:
[Cedar policy code here]

RATIONALE:
• [reason 1]
• [reason 2]
• [reason 3]

Make sure the policy uses correct Cedar syntax and references entities/actions from the schema."""

        return generate_text(prompt)
    
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