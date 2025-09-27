#!/usr/bin/env python3
"""
Startup script for Medical Report Analyzer API
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly configured"""
    load_dotenv()
    
    # Check for Gemini API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ GEMINI_API_KEY not configured!")
        print("Please edit .env file and add your Gemini API key.")
        print("Get your key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✅ Environment configured successfully!")
    return True

def main():
    """Main startup function"""
    print("🏥 Starting Medical Report Analyzer API...")
    print("=" * 45)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        from app import app
        print("🚀 Server starting on http://localhost:5000")
        print("📊 Health check: http://localhost:5000/health")
        print("🔍 API docs: See README_BACKEND.md")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 45)
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        )
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
