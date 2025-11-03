#!/usr/bin/env python3
import sys
import os
from policy_generator import PolicyGenerator
from history_manager import HistoryManager
from approval_manager import ApprovalManager

def main():
    if len(sys.argv) < 2:
        print("Usage: python policy_helper.py '<requirement>' [schema_file] [--recommendations]")
        print("Example: python policy_helper.py 'Deny Account Holder from creating transactions >= 5000'")
        print("         python policy_helper.py --recommendations")
        sys.exit(1)
    
    # Handle recommendations flag
    if sys.argv[1] == '--recommendations':
        show_recommendations()
        return
    
    requirement = sys.argv[1]
    schema_file = sys.argv[2] if len(sys.argv) > 2 else 'sample_banking_schema.json'
    
    if not os.path.exists(schema_file):
        print(f"Schema file {schema_file} not found. Using default schema.")
        schema_file = 'sample_banking_schema.json'
    
    try:
        generator = PolicyGenerator(schema_file)
        history = HistoryManager()
        approval_manager = ApprovalManager()
        
        print(f"\n🔍 Processing requirement: {requirement}")
        print("📋 Generating and validating Cedar policy...\n")
        
        # Generate with validation
        result = generator.generate_and_validate_policy(requirement)
        
        # Display validation status
        if result['validation']['is_valid']:
            print("✅ VALIDATION: Policy is syntactically correct and schema-compliant")
        else:
            print("⚠️  VALIDATION ERRORS:")
            for error in result['validation']['errors']:
                print(f"   • {error}")
        
        print("\nCEDAR POLICY:")
        print(result['policy'])
        print("\nRATIONALE:")
        for rationale in result['rationale']:
            print(rationale)
        
        # Show test cases
        if result['validation']['test_cases']:
            print("\nTEST SCENARIOS:")
            for i, test in enumerate(result['validation']['test_cases'][:3], 1):
                print(f"   {i}. {test['description']}")
        
        # Interactive approval
        print("\n" + "="*50)
        choice = input("Approve this policy? (y/n/feedback): ").lower().strip()
        
        if choice == 'y':
            approval_id = approval_manager.approve_policy({
                'requirement': requirement,
                'policy': result['policy'],
                'rationale': result['rationale'],
                'validation': result['validation']
            })
            
            # Also save to history
            history_id = history.save_policy(requirement, result['policy'], result['rationale'])
            
            print(f"✅ Policy approved and saved (ID: {approval_id}, History: {history_id})")
            
        elif choice == 'n':
            reason = input("Rejection reason: ")
            rejection_id = approval_manager.reject_policy({
                'requirement': requirement,
                'policy': result['policy'],
                'rationale': result['rationale'],
                'validation': result['validation']
            }, reason)
            
            print(f"❌ Policy rejected (ID: {rejection_id}). Feedback recorded for improvement.")
            
        elif choice == 'feedback':
            feedback = input("Your feedback: ")
            approval_id = approval_manager.approve_policy({
                'requirement': requirement,
                'policy': result['policy'],
                'rationale': result['rationale'],
                'validation': result['validation']
            }, feedback)
            
            history_id = history.save_policy(requirement, result['policy'], result['rationale'])
            print(f"✅ Policy approved with feedback (ID: {approval_id}, History: {history_id})")
        
        # Show stats
        stats = approval_manager.get_approval_stats()
        print(f"\n📊 Stats: {stats['approved']}/{stats['total_policies']} approved ({stats['approval_rate']:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def show_recommendations():
    """Show policy recommendations based on schema"""
    try:
        generator = PolicyGenerator('sample_banking_schema.json')
        recommendations = generator.get_recommendations()
        
        print("\n🎯 POLICY RECOMMENDATIONS")
        print("="*50)
        
        for i, rec in enumerate(recommendations, 1):
            priority_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            print(f"\n{i}. {rec['title']} {priority_icon.get(rec['priority'], '')}")
            print(f"   Priority: {rec['priority']}")
            print(f"   Description: {rec['description']}")
            print("   Rationale:")
            for rationale in rec['rationale']:
                print(f"     {rationale}")
        
        print(f"\n💡 Found {len(recommendations)} recommendations based on your schema.")
        print("   Use the web interface to generate policies from these recommendations.")
        
    except Exception as e:
        print(f"❌ Error loading recommendations: {e}")

if __name__ == "__main__":
    main()