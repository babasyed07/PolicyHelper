#!/usr/bin/env python3
# Test without AWS credentials
from schema_parser import SchemaParser

# Test schema parsing
parser = SchemaParser()
parser.load_schema('sample_banking_schema.json')
context = parser.get_schema_context()

print("✅ Schema loaded successfully!")
print(f"Entities: {context['entities']}")
print(f"Actions: {context['actions']}")

# Test mock policy generation
mock_response = """POLICY:
forbid (
  principal == User::"AccountHolder",
  action == Action::"CreateTransaction",
  resource
) when {
  resource.amount >= 5000
};

RATIONALE:
• Prevents account holders from initiating high-value transactions above $5000 threshold
• Reduces fraud risk by requiring additional authorization for large transactions
• Aligns with banking regulations requiring enhanced controls for significant monetary transfers"""

from policy_generator import PolicyGenerator
generator = PolicyGenerator('sample_banking_schema.json')
parsed = generator.parse_response(mock_response)

print("\n✅ Policy parsing works!")
print("Policy:", parsed['policy'])
print("Rationale:", parsed['rationale'])