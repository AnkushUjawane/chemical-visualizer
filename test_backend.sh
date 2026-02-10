#!/bin/bash

echo "Testing Backend API..."
cd backend
export PATH="$(pwd)/venv/bin:$PATH"

# Start server in background
python manage.py runserver > /dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "Server started (PID: $SERVER_PID)"

# Test registration
echo "Testing user registration..."
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' \
  -s | grep -q "successfully" && echo "✓ Registration works" || echo "✗ Registration failed"

# Test login
echo "Testing user login..."
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' \
  -s | grep -q "successful" && echo "✓ Login works" || echo "✗ Login failed"

# Test CSV upload
echo "Testing CSV upload..."
curl -X POST http://localhost:8000/api/upload/ \
  -u testuser:testpass123 \
  -F "file=@../sample_equipment_data.csv" \
  -s | grep -q "total_count" && echo "✓ CSV upload works" || echo "✗ CSV upload failed"

# Test datasets retrieval
echo "Testing datasets retrieval..."
curl -X GET http://localhost:8000/api/datasets/ \
  -u testuser:testpass123 \
  -s | grep -q "filename" && echo "✓ Datasets retrieval works" || echo "✗ Datasets retrieval failed"

# Stop server
kill $SERVER_PID
echo "Server stopped"

echo ""
echo "Backend tests complete!"
