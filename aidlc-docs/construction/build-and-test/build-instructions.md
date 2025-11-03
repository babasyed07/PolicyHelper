# Build Instructions

## Prerequisites
- **Build Tool**: Python 3.8+ with pip
- **Dependencies**: boto3, flask
- **Environment Variables**: AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION)
- **System Requirements**: macOS/Linux/Windows, 512MB RAM, 100MB disk space

## Build Steps

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment Variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### 3. Build All Units
```bash
# No compilation needed for Python - verify imports
python -c "import policy_helper, web_app, bedrock_client, schema_parser, policy_generator, history_manager"
echo "Build successful - all modules importable"
```

### 4. Verify Build Success
- **Expected Output**: "Build successful - all modules importable"
- **Build Artifacts**: Python bytecode files (.pyc) in __pycache__/
- **Common Warnings**: None expected

## Troubleshooting

### Build Fails with Dependency Errors
- **Cause**: Missing pip packages or Python version mismatch
- **Solution**: Ensure Python 3.8+, activate virtual environment, reinstall requirements

### Build Fails with Import Errors
- **Cause**: Missing modules or incorrect PYTHONPATH
- **Solution**: Verify all .py files exist, check for syntax errors