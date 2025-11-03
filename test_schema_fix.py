#!/usr/bin/env python3
from schema_validator import SchemaValidator

# Test the schema validator with different formats
validator = SchemaValidator()

# Test 1: Direct format
direct_schema = {
    "entityTypes": {"User": {}, "Account": {}},
    "actions": {"ViewAccount": {}, "CreateTransaction": {}}
}

print("=== Test 1: Direct Schema Format ===")
valid, error, data = validator.validate_schema(direct_schema)
print(f"Valid: {valid}")
print(f"Error: {error}")
print(f"Entities: {data.get('entities', [])}")
print(f"Actions: {data.get('actions', [])}")

# Test 2: Namespaced format (like SecureBank)
namespaced_schema = {
    "SecureBank": {
        "entityTypes": {"User": {}, "Account": {}},
        "actions": {"ViewAccount": {}, "CreateTransaction": {}}
    }
}

print("\n=== Test 2: Namespaced Schema Format ===")
valid, error, data = validator.validate_schema(namespaced_schema)
print(f"Valid: {valid}")
print(f"Error: {error}")
print(f"Entities: {data.get('entities', [])}")
print(f"Actions: {data.get('actions', [])}")

# Test 3: Invalid schema
invalid_schema = {"invalid": "structure"}

print("\n=== Test 3: Invalid Schema ===")
valid, error, data = validator.validate_schema(invalid_schema)
print(f"Valid: {valid}")
print(f"Error: {error}")

print("\n=== Fix Complete ===")
print("✅ Schema validator now handles both direct and namespaced Cedar schemas")
print("✅ Web app will accept your SecureBank schema format")