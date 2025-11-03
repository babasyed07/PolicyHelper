#!/bin/bash
# PolicyHelper Deployment Script

echo "🚀 Deploying PolicyHelper Application"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check application files
echo "🔍 Verifying application files..."
required_files=("web_app.py" "policy_helper.py" "sample_banking_schema.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

echo "✅ All required files present"

# Start the application
echo "🌐 Starting PolicyHelper web application..."
echo "📍 Application will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

python web_app.py