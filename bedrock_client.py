import boto3
import json
import os

def generate_text(prompt):
    try:
        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
        
        response = client.invoke_model(
            body=body,
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            contentType='application/json'
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
        
    except Exception as e:
        # Fallback for demo without AWS credentials
        return generate_mock_policy(prompt)

def generate_mock_policy(prompt):
    """Generate mock policy for demo purposes when AWS is not available"""
    return """POLICY:
forbid(
  principal,
  action == Action::"CreateTransaction",
  resource
)
when {
  resource.amount >= 5000
};

RATIONALE:
• Prevents high-value transactions above $5000 threshold
• Reduces fraud risk by requiring additional authorization for large transactions
• Aligns with banking regulations requiring enhanced controls for significant monetary transfers"""