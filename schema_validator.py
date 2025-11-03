import json
from typing import Dict, Tuple, List

class SchemaValidator:
    """Validates Cedar schema JSON structure"""
    
    def validate_schema(self, schema_data) -> Tuple[bool, str, Dict]:
        """
        Validate Cedar schema and extract entities/actions
        Returns: (is_valid, error_message, extracted_data)
        """
        try:
            # Handle string input
            if isinstance(schema_data, str):
                schema_data = json.loads(schema_data)
            
            # Find the actual schema data (handle namespaced schemas)
            actual_schema = self._extract_schema_data(schema_data)
            
            # Validate structure
            entities = actual_schema.get('entityTypes', {})
            actions = actual_schema.get('actions', {})
            
            if not entities and not actions:
                return False, "Schema must contain 'entityTypes' or 'actions'", {}
            
            return True, "", {
                'entities': list(entities.keys()),
                'actions': list(actions.keys()),
                'entityTypes': entities,
                'actions': actions
            }
            
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}", {}
        except Exception as e:
            return False, f"Schema validation error: {str(e)}", {}
    
    def _extract_schema_data(self, schema_data: Dict) -> Dict:
        """Extract actual schema from potentially namespaced structure"""
        # Direct schema format: {"entityTypes": {...}, "actions": {...}}
        if 'entityTypes' in schema_data or 'actions' in schema_data:
            return schema_data
        
        # Namespaced format: {"SecureBank": {"entityTypes": {...}, "actions": {...}}}
        if len(schema_data) == 1:
            namespace_key = list(schema_data.keys())[0]
            nested_data = schema_data[namespace_key]
            if isinstance(nested_data, dict) and ('entityTypes' in nested_data or 'actions' in nested_data):
                return nested_data
        
        # Return as-is if no clear structure found
        return schema_data