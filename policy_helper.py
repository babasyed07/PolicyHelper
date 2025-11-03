#!/usr/bin/env python3
import sys
import os
from policy_generator import PolicyGenerator
from history_manager import HistoryManager

def main():
    if len(sys.argv) < 2:
        print("Usage: python policy_helper.py '<requirement>' [schema_file]")
        print("Example: python policy_helper.py 'Deny Account Holder from creating transactions >= 5000'")
        sys.exit(1)
    
    requirement = sys.argv[1]
    schema_file = sys.argv[2] if len(sys.argv) > 2 else 'sample_banking_schema.json'
    
    if not os.path.exists(schema_file):
        print(f"Schema file {schema_file} not found. Using default schema.")
        schema_file = 'sample_banking_schema.json'
    
    try:
        generator = PolicyGenerator(schema_file)
        history = HistoryManager()
        
        print(f"\n🔍 Processing requirement: {requirement}")
        print("📋 Generating Cedar policy...\n")
        
        response = generator.generate_policy(requirement)
        parsed = generator.parse_response(response)
        
        print("CEDAR POLICY:")
        print(parsed['policy'])
        print("\nRATIONALE:")
        for rationale in parsed['rationale']:
            print(rationale)
        
        # Save to history
        index = history.save_policy(requirement, parsed['policy'], parsed['rationale'])
        print(f"\n💾 Saved as policy #{index}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()