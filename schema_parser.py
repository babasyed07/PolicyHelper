import json

class SchemaParser:
    def __init__(self):
        self.schema = None
        self.entities = {}
        self.actions = {}
    
    def load_schema(self, schema_path):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        self._parse_entities()
        self._parse_actions()
    
    def _parse_entities(self):
        # Handle different schema structures
        schema_data = self.schema
        
        # If schema has a namespace wrapper (like "SecureBank"), unwrap it
        if len(self.schema) == 1 and 'entityTypes' not in self.schema:
            namespace_key = list(self.schema.keys())[0]
            schema_data = self.schema[namespace_key]
        
        if 'entityTypes' in schema_data:
            for entity_name, entity_def in schema_data['entityTypes'].items():
                self.entities[entity_name] = entity_def
    
    def _parse_actions(self):
        # Handle different schema structures
        schema_data = self.schema
        
        # If schema has a namespace wrapper (like "SecureBank"), unwrap it
        if len(self.schema) == 1 and 'actions' not in self.schema:
            namespace_key = list(self.schema.keys())[0]
            schema_data = self.schema[namespace_key]
        
        if 'actions' in schema_data:
            for action_name, action_def in schema_data['actions'].items():
                self.actions[action_name] = action_def
    
    def get_schema_context(self):
        return {
            'entities': list(self.entities.keys()),
            'actions': list(self.actions.keys()),
            'entity_details': self.entities,
            'action_details': self.actions
        }