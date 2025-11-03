#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from policy_generator import PolicyGenerator
from history_manager import HistoryManager
import os

app = Flask(__name__)
generator = PolicyGenerator('sample_banking_schema.json')
history = HistoryManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_policy():
    try:
        requirement = request.json.get('requirement', '')
        if not requirement:
            return jsonify({'error': 'Requirement is required'}), 400
        
        response = generator.generate_policy(requirement)
        parsed = generator.parse_response(response)
        
        # Save to history
        index = history.save_policy(requirement, parsed['policy'], parsed['rationale'])
        
        return jsonify({
            'policy': parsed['policy'],
            'rationale': parsed['rationale'],
            'saved_index': index
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def get_history():
    return jsonify(history.get_history())

if __name__ == '__main__':
    app.run(debug=True, port=5000)