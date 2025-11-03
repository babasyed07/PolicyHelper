import boto3
import json

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
        
        print(f"Calling model with body: {body}")
        
        response = client.invoke_model(
            body=body,
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            contentType='application/json'
        )
        
        result = json.loads(response['body'].read())
        print(f"Response: {result}")
        return result['content'][0]['text']
        
    except Exception as e:
        print(f"Error: {e}")
        raise