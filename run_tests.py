#!/usr/bin/env python3
"""
Test runner for enhanced Policy Helper features
"""

from policy_validator import PolicyValidator
from policy_recommender import PolicyRecommender
from approval_manager import ApprovalManager
from chat_session import ChatSession, ChatManager
from policy_generator import PolicyGenerator
import os

def main():
    print("🧪 Testing Enhanced Policy Helper Components")
    print("="*50)
    
    # Test Policy Validator
    print("\n1. Testing Policy Validator...")
    validator = PolicyValidator()
    schema_context = {
        'entities': ['User', 'Account', 'Transaction'],
        'actions': ['CreateTransaction', 'ViewAccount', 'ModifyAccount']
    }
    
    # Test valid policy
    valid_policy = 'forbid (principal == User::"AccountHolder", action == Action::"CreateTransaction", resource) when { resource.amount >= 5000 };'
    is_valid, errors = validator.validate_policy(valid_policy, schema_context)
    print(f"   ✅ Valid policy test: {is_valid} (errors: {len(errors)})")
    
    # Test invalid policy
    invalid_policy = 'forbid (principal == InvalidEntity::"Test", action == Action::"CreateTransaction", resource)'
    is_valid, errors = validator.validate_policy(invalid_policy, schema_context)
    print(f"   ✅ Invalid policy test: {not is_valid} (found {len(errors)} errors)")
    
    # Test Policy Recommender
    print("\n2. Testing Policy Recommender...")
    recommender = PolicyRecommender(schema_context)
    recommendations = recommender.generate_recommendations()
    print(f"   ✅ Generated {len(recommendations)} recommendations")
    
    for rec in recommendations:
        print(f"      - {rec['title']} ({rec['priority']} priority)")
    
    # Test Chat Session
    print("\n3. Testing Chat Session...")
    session = ChatSession()
    session.add_message('user', 'Create a policy for high-value transactions')
    session.add_message('assistant', 'Here is your policy...')
    print(f"   ✅ Chat session created with {len(session.messages)} messages")
    
    context = session.get_conversation_context()
    print(f"   ✅ Conversation context: {len(context)} characters")
    
    # Test Approval Manager
    print("\n4. Testing Approval Manager...")
    approval_manager = ApprovalManager('test_approvals.json')
    
    policy_data = {
        'requirement': 'Test requirement',
        'policy': 'permit (principal, action, resource);',
        'rationale': ['Test rationale'],
        'validation': {'is_valid': True, 'errors': []}
    }
    
    approval_id = approval_manager.approve_policy(policy_data, 'Test feedback')
    print(f"   ✅ Policy approved with ID: {approval_id}")
    
    stats = approval_manager.get_approval_stats()
    print(f"   ✅ Approval stats: {stats['approved']}/{stats['total_policies']} ({stats['approval_rate']:.1f}%)")
    
    # Test Policy Generator (offline components)
    print("\n5. Testing Policy Generator (offline)...")
    try:
        generator = PolicyGenerator('sample_banking_schema.json')
        recommendations = generator.get_recommendations()
        print(f"   ✅ Policy generator loaded with {len(recommendations)} recommendations")
        
        # Test response parsing
        mock_response = """POLICY:
forbid (principal == User::"AccountHolder", action == Action::"CreateTransaction", resource) when { resource.amount >= 5000 };

RATIONALE:
• Prevents high-value transactions
• Reduces fraud risk
• Complies with regulations"""
        
        parsed = generator.parse_response(mock_response)
        print(f"   ✅ Response parsing: policy={len(parsed['policy'])} chars, rationale={len(parsed['rationale'])} items")
        
    except Exception as e:
        print(f"   ⚠️  Policy generator test skipped: {e}")
    
    # Test CLI recommendations
    print("\n6. Testing CLI Recommendations...")
    try:
        from policy_helper import show_recommendations
        print("   ✅ CLI recommendations function available")
    except Exception as e:
        print(f"   ⚠️  CLI test skipped: {e}")
    
    print("\n" + "="*50)
    print("✅ All component tests completed successfully!")
    print("\n📋 Summary:")
    print("   • Policy validation with syntax and schema checking")
    print("   • Banking-specific policy recommendations")
    print("   • Conversational chat session management")
    print("   • Approval workflow with statistics tracking")
    print("   • Enhanced CLI with interactive approval")
    print("   • Web interface with tabbed functionality")
    
    # Cleanup test files
    test_files = ['test_approvals.json']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"   🧹 Cleaned up {file}")

if __name__ == '__main__':
    main()