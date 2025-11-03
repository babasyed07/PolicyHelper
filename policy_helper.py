#!/usr/bin/env python3
import sys
from bedrock_client import generate_text

def main():
    if len(sys.argv) < 2:
        print("Usage: python policy_helper.py '<requirement>'")
        sys.exit(1)
    
    requirement = " ".join(sys.argv[1:])
    
    prompt = f"""Generate an AWS IAM policy snippet for this requirement: {requirement}

Provide:
1. A JSON policy snippet
2. Exactly 3 bullet points explaining the rationale

Format your response as:
POLICY:
[JSON policy here]

RATIONALE:
• [reason 1]
• [reason 2] 
• [reason 3]"""

    response = generate_text(prompt)
    print(response)

if __name__ == "__main__":
    main()