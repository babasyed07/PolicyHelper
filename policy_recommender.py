from typing import Dict, List
import json

class PolicyRecommender:
    def __init__(self, schema_context: Dict):
        self.schema_context = schema_context
        self.banking_patterns = {
            'high_value_transactions': {
                'priority': 'HIGH',
                'template': 'forbid (principal == User::"AccountHolder", action == Action::"CreateTransaction", resource) when { resource.amount >= {threshold} };',
                'rationale': [
                    '• Prevents unauthorized high-value transactions above threshold',
                    '• Reduces fraud risk by requiring additional authorization',
                    '• Complies with banking regulations for large transactions'
                ]
            },
            'account_access_control': {
                'priority': 'MEDIUM',
                'template': 'permit (principal == User::"{role}", action == Action::"ViewAccount", resource) when { resource.ownerId == principal.userId };',
                'rationale': [
                    '• Ensures users can only access their own accounts',
                    '• Implements principle of least privilege',
                    '• Protects customer privacy and data security'
                ]
            },
            'manager_override': {
                'priority': 'MEDIUM',
                'template': 'permit (principal == User::"Manager", action, resource);',
                'rationale': [
                    '• Allows managers to override standard restrictions',
                    '• Enables exception handling for business needs',
                    '• Maintains audit trail for management actions'
                ]
            },
            'after_hours_restrictions': {
                'priority': 'LOW',
                'template': 'forbid (principal, action == Action::"CreateTransaction", resource) when { context.time > "18:00" && context.time < "08:00" };',
                'rationale': [
                    '• Restricts transactions during non-business hours',
                    '• Reduces risk of unauthorized after-hours activity',
                    '• Aligns with operational security policies'
                ]
            }
        }
    
    def generate_recommendations(self) -> List[Dict]:
        """Generate policy recommendations based on schema and banking patterns"""
        recommendations = []
        
        entities = self.schema_context.get('entities', [])
        actions = self.schema_context.get('actions', [])
        
        # High-value transaction protection
        if 'Transaction' in entities and 'CreateTransaction' in actions:
            recommendations.append({
                'id': 'high_value_tx',
                'title': 'High-Value Transaction Protection',
                'priority': 'HIGH',
                'description': 'Prevent unauthorized large transactions',
                'template': self.banking_patterns['high_value_transactions']['template'],
                'rationale': self.banking_patterns['high_value_transactions']['rationale'],
                'parameters': {'threshold': 5000}
            })
        
        # Account access control
        if 'Account' in entities and 'ViewAccount' in actions:
            recommendations.append({
                'id': 'account_access',
                'title': 'Account Access Control',
                'priority': 'MEDIUM',
                'description': 'Restrict account access to owners only',
                'template': self.banking_patterns['account_access_control']['template'],
                'rationale': self.banking_patterns['account_access_control']['rationale'],
                'parameters': {'role': 'AccountHolder'}
            })
        
        # Manager override capabilities
        if 'User' in entities:
            recommendations.append({
                'id': 'manager_override',
                'title': 'Manager Override Policy',
                'priority': 'MEDIUM',
                'description': 'Allow managers to override restrictions',
                'template': self.banking_patterns['manager_override']['template'],
                'rationale': self.banking_patterns['manager_override']['rationale'],
                'parameters': {}
            })
        
        return recommendations
    
    def customize_recommendation(self, recommendation_id: str, parameters: Dict) -> str:
        """Customize a recommendation template with specific parameters"""
        recommendations = self.generate_recommendations()
        
        for rec in recommendations:
            if rec['id'] == recommendation_id:
                template = rec['template']
                for key, value in parameters.items():
                    template = template.replace(f'{{{key}}}', str(value))
                return template
        
        return None