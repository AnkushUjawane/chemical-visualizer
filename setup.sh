#!/bin/bash

echo "=========================================="
echo "Chemical Equipment Visualizer - Setup"
echo "=========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python 3 found"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi
echo "✓ Node.js found"

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi
echo "✓ npm found"

echo ""
echo "Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    export PATH="$(pwd)/venv/bin:$PATH"
    pip install -r requirements.txt
else
    echo "✓ Virtual environment exists"
fi

export PATH="$(pwd)/venv/bin:$PATH"
python manage.py migrate --no-input
echo "✓ Database migrations complete"

cd ..

echo ""
echo "Setting up Web Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
else
    echo "✓ npm packages already installed"
fi

cd ..

echo ""
echo "Setting up Desktop App..."
cd desktop

if ! python3 -c "import PyQt5" &> /dev/null; then
    echo "Installing desktop dependencies..."
    pip install -r requirements.txt
else
    echo "✓ Desktop dependencies already installed"
fi

cd ..

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend && ./start.sh"
echo ""
echo "2. Web Frontend (Terminal 2):"
echo "   cd frontend && npm start"
echo ""
echo "3. Desktop App (Terminal 3):"
echo "   cd desktop && python app.py"
echo ""
echo "Sample data: sample_equipment_data.csv"
echo ""
echo "See README.md for detailed instructions"
echo "=========================================="
