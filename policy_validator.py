import re
import json
from typing import Dict, List, Tuple, Optional

class PolicyValidator:
    def __init__(self):
        self.cedar_keywords = ['permit', 'forbid', 'principal', 'action', 'resource', 'when', 'unless']
        self.operators = ['==', '!=', '>', '<', '>=', '<=', 'in', 'has']
    
    def validate_policy(self, policy: str, schema_context: Dict) -> Tuple[bool, List[str]]:
        """Validate Cedar policy syntax and schema compliance"""
        errors = []
        
        # Basic syntax validation
        syntax_valid, syntax_errors = self._validate_syntax(policy)
        errors.extend(syntax_errors)
        
        # Schema compliance validation
        schema_valid, schema_errors = self._validate_schema_compliance(policy, schema_context)
        errors.extend(schema_errors)
        
        return len(errors) == 0, errors
    
    def _validate_syntax(self, policy: str) -> Tuple[bool, List[str]]:
        """Validate basic Cedar syntax"""
        errors = []
        
        # Check for required keywords
        if not re.search(r'\b(permit|forbid)\b', policy):
            errors.append("Policy must start with 'permit' or 'forbid'")
        
        # Check for balanced parentheses
        if policy.count('(') != policy.count(')'):
            errors.append("Unbalanced parentheses in policy")
        
        # Check for balanced braces
        if policy.count('{') != policy.count('}'):
            errors.append("Unbalanced braces in policy")
        
        # Check for semicolon termination
        if not policy.strip().endswith(';'):
            errors.append("Policy must end with semicolon")
        
        return len(errors) == 0, errors
    
    def _validate_schema_compliance(self, policy: str, schema_context: Dict) -> Tuple[bool, List[str]]:
        """Validate policy against schema entities and actions"""
        errors = []
        
        # Extract entities and actions from policy
        entities = re.findall(r'(\w+)::"(\w+)"', policy)
        actions = re.findall(r'Action::"(\w+)"', policy)
        
        # Validate entities
        for entity_type, entity_name in entities:
            if entity_type not in schema_context.get('entities', []):
                errors.append(f"Unknown entity type: {entity_type}")
        
        # Validate actions
        for action in actions:
            if action not in schema_context.get('actions', []):
                errors.append(f"Unknown action: {action}")
        
        return len(errors) == 0, errors
    
    def generate_test_cases(self, policy: str) -> List[Dict]:
        """Generate test scenarios for policy validation"""
        test_cases = []
        
        # Extract conditions from policy
        conditions = re.findall(r'(\w+\.\w+)\s*([><=!]+)\s*(\w+)', policy)
        
        for attr, op, value in conditions:
            # Generate positive test case
            test_cases.append({
                'description': f'Test {attr} {op} {value} - should match policy',
                'principal': 'User::"TestUser"',
                'action': 'Action::"TestAction"',
                'resource': f'{{{attr}: {value}}}',
                'expected': 'permit' in policy.lower()
            })
            
            # Generate negative test case
            opposite_value = str(int(value) - 1) if value.isdigit() else 'different_value'
            test_cases.append({
                'description': f'Test {attr} != {value} - should not match policy',
                'principal': 'User::"TestUser"',
                'action': 'Action::"TestAction"',
                'resource': f'{{{attr}: {opposite_value}}}',
                'expected': not ('permit' in policy.lower())
            })
        
        return test_cases