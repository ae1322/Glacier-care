#!/usr/bin/env python3
"""
Simple script to run the Glacier Care API
"""

import os
import sys

# Set the API key directly
os.environ['GEMINI_API_KEY'] = 'AIzaSyDoic239xATtrO8BSsl2jvrudumFUJHs84'

# Import and run the Flask app
try:
    from app import app
    print("🏥 Glacier Care API")
    print("=" * 40)
    print("✅ Gemini API Key: Configured")
    print("🚀 Starting server on http://localhost:5000")
    print("📊 Health check: http://localhost:5000/health")
    print("🔍 Analyze endpoint: http://localhost:5000/analyze")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 40)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
