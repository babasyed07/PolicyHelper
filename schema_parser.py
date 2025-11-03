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
        if 'entityTypes' in self.schema:
            for entity_name, entity_def in self.schema['entityTypes'].items():
                self.entities[entity_name] = entity_def
    
    def _parse_actions(self):
        if 'actions' in self.schema:
            for action_name, action_def in self.schema['actions'].items():
                self.actions[action_name] = action_def
    
    def get_schema_context(self):
        return {
            'entities': list(self.entities.keys()),
            'actions': list(self.actions.keys()),
            'entity_details': self.entities,
            'action_details': self.actions
        }