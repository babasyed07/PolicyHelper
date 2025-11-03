from typing import Dict, List, Optional
from datetime import datetime
import json
import os

class ApprovalManager:
    def __init__(self, approval_file='policy_approvals.json'):
        self.approval_file = approval_file
        self.approvals = self._load_approvals()
    
    def _load_approvals(self):
        if os.path.exists(self.approval_file):
            with open(self.approval_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_approvals(self):
        with open(self.approval_file, 'w') as f:
            json.dump(self.approvals, f, indent=2)
    
    def approve_policy(self, policy_data: Dict, user_feedback: str = "") -> int:
        """Approve a policy and save it"""
        approval_entry = {
            'id': len(self.approvals),
            'timestamp': datetime.now().isoformat(),
            'status': 'APPROVED',
            'requirement': policy_data.get('requirement', ''),
            'policy': policy_data.get('policy', ''),
            'rationale': policy_data.get('rationale', []),
            'validation': policy_data.get('validation', {}),
            'user_feedback': user_feedback
        }
        
        self.approvals.append(approval_entry)
        self._save_approvals()
        return approval_entry['id']
    
    def reject_policy(self, policy_data: Dict, rejection_reason: str) -> int:
        """Reject a policy with reason"""
        rejection_entry = {
            'id': len(self.approvals),
            'timestamp': datetime.now().isoformat(),
            'status': 'REJECTED',
            'requirement': policy_data.get('requirement', ''),
            'policy': policy_data.get('policy', ''),
            'rationale': policy_data.get('rationale', []),
            'validation': policy_data.get('validation', {}),
            'rejection_reason': rejection_reason
        }
        
        self.approvals.append(rejection_entry)
        self._save_approvals()
        return rejection_entry['id']
    
    def get_approval_stats(self) -> Dict:
        """Get approval/rejection statistics"""
        total = len(self.approvals)
        approved = len([a for a in self.approvals if a['status'] == 'APPROVED'])
        rejected = len([a for a in self.approvals if a['status'] == 'REJECTED'])
        
        return {
            'total_policies': total,
            'approved': approved,
            'rejected': rejected,
            'approval_rate': (approved / total * 100) if total > 0 else 0
        }
    
    def get_approved_policies(self) -> List[Dict]:
        """Get all approved policies"""
        return [a for a in self.approvals if a['status'] == 'APPROVED']
    
    def get_rejection_feedback(self) -> List[str]:
        """Get all rejection reasons for improvement"""
        return [a.get('rejection_reason', '') for a in self.approvals if a['status'] == 'REJECTED' and a.get('rejection_reason')]