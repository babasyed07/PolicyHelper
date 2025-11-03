#!/usr/bin/env python3
from bedrock_client import generate_text

try:
    response = generate_text("Hello, can you respond with just 'Connection successful'?")
    print("✓ Bedrock connection successful!")
    print(f"Response: {response}")
except Exception as e:
    print(f"✗ Connection failed: {e}")