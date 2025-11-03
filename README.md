# Policy Helper

AI-powered tool that converts plain English access control requirements into Cedar policy snippets for banking applications.

## Features

- 📋 Cedar schema ingestion (JSON format)
- 🤖 Natural language to Cedar policy conversion via Amazon Bedrock
- 💡 3-bullet rationale explanations
- 💻 CLI interface for developers
- 🌐 Web chatbot interface
- 📚 Policy history management

## Setup

1. **Install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure AWS credentials:**
```bash
aws configure
# OR set environment variables:
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## Usage

### CLI Interface

```bash
# Basic usage with sample schema
python policy_helper.py "Deny Account Holder from creating transactions >= 5000"

# With custom schema
python policy_helper.py "Allow managers to view all accounts" custom_schema.json
```

### Web Interface

```bash
python web_app.py
# Open http://localhost:5000
```

### View History

```bash
# List all policies
python history_viewer.py

# View specific policy
python history_viewer.py 0
```

## Example

**Input:** "Deny Account Holder from creating transactions >= 5000"

**Output:**
```cedar
forbid (
  principal == User::"AccountHolder",
  action == Action::"CreateTransaction",
  resource
) when {
  resource.amount >= 5000
};
```

**Rationale:**
• Prevents account holders from initiating high-value transactions above $5000 threshold
• Reduces fraud risk by requiring additional authorization for large transactions
• Aligns with banking regulations requiring enhanced controls for significant monetary transfers

## Files

- `policy_helper.py` - CLI interface
- `web_app.py` - Web interface
- `bedrock_client.py` - Amazon Bedrock integration
- `schema_parser.py` - Cedar schema parser
- `policy_generator.py` - Policy generation engine
- `history_manager.py` - History persistence
- `sample_banking_schema.json` - Example Cedar schema