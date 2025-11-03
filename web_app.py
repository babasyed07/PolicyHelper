#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, session
from policy_generator import PolicyGenerator
from history_manager import HistoryManager
from approval_manager import ApprovalManager
from chat_session import ChatManager
from schema_validator import SchemaValidator
import os
import uuid
import json

app = Flask(__name__)
app.secret_key = 'policy-helper-secret-key'
generator = PolicyGenerator('sample_banking_schema.json')
history = HistoryManager()
approval_manager = ApprovalManager()
chat_manager = ChatManager()
schema_validator = SchemaValidator()

@app.route('/')
def index():
    return render_template('enhanced_index.html')

@app.route('/recommendations')
def get_recommendations():
    """Get policy recommendations based on schema"""
    try:
        recommendations = generator.get_recommendations()
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/start', methods=['POST'])
def start_chat():
    """Start new chat session"""
    session_id = chat_manager.create_session()
    session['chat_id'] = session_id
    return jsonify({'session_id': session_id})

@app.route('/chat/message', methods=['POST'])
def chat_message():
    """Process chat message"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = session.get('chat_id')
        
        if not session_id:
            return jsonify({'error': 'No active chat session'}), 400
        
        chat_session = chat_manager.get_session(session_id)
        if not chat_session:
            return jsonify({'error': 'Chat session not found'}), 404
        
        # Add user message to session
        chat_session.add_message('user', message)
        
        # Get conversation context
        context = chat_session.get_conversation_context()
        
        # Generate policy with context
        result = generator.generate_and_validate_policy(message, context)
        
        # Add assistant response to session
        chat_session.add_message('assistant', f"Policy: {result['policy']}")
        
        return jsonify({
            'policy': result['policy'],
            'rationale': result['rationale'],
            'validation': result['validation'],
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload-schema', methods=['POST'])
def upload_schema():
    """Upload Cedar schema JSON"""
    try:
        schema_data = request.json.get('schema', '')
        if not schema_data:
            return jsonify({'error': 'Schema is required'}), 400
        
        # Validate schema using dedicated validator
        is_valid, error_msg, extracted_data = schema_validator.validate_schema(schema_data)
        
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Save uploaded schema
        with open('uploaded_schema.json', 'w') as f:
            if isinstance(schema_data, str):
                f.write(schema_data)
            else:
                json.dump(schema_data, f, indent=2)
        
        # Reload generator with new schema
        global generator
        generator = PolicyGenerator('uploaded_schema.json')
        
        return jsonify({
            'status': 'Schema uploaded successfully',
            'entities': extracted_data.get('entities', []),
            'actions': extracted_data.get('actions', [])
        })
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate_policy():
    try:
        requirement = request.json.get('requirement', '')
        if not requirement:
            return jsonify({'error': 'Requirement is required'}), 400
        
        # Generate and validate policy
        result = generator.generate_and_validate_policy(requirement)
        
        return jsonify({
            'policy': result['policy'],
            'rationale': result['rationale'],
            'validation': result['validation']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/approve', methods=['POST'])
def approve_policy():
    """Approve a generated policy"""
    try:
        policy_data = request.json
        feedback = policy_data.get('feedback', '')
        
        approval_id = approval_manager.approve_policy(policy_data, feedback)
        
        # Also save to history for backward compatibility
        history.save_policy(
            policy_data.get('requirement', ''),
            policy_data.get('policy', ''),
            policy_data.get('rationale', [])
        )
        
        return jsonify({
            'status': 'approved',
            'approval_id': approval_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reject', methods=['POST'])
def reject_policy():
    """Reject a generated policy"""
    try:
        policy_data = request.json
        reason = policy_data.get('reason', 'No reason provided')
        
        rejection_id = approval_manager.reject_policy(policy_data, reason)
        
        return jsonify({
            'status': 'rejected',
            'rejection_id': rejection_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def get_stats():
    """Get approval statistics"""
    return jsonify(approval_manager.get_approval_stats())

@app.route('/history')
def get_history():
    return jsonify(history.get_history())

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)