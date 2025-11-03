#!/usr/bin/env python3
import boto3

try:
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    print(f"✓ AWS credentials configured for: {identity['Arn']}")
    
    # Check Bedrock access
    bedrock = boto3.client('bedrock', region_name='us-east-1')
    models = bedrock.list_foundation_models()
    print("✓ Bedrock service accessible")
    
except Exception as e:
    print(f"✗ AWS setup issue: {e}")