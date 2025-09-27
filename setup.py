#!/usr/bin/env python3
"""
Setup script for Medical Report Analyzer API
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def setup_environment():
    """Setup environment file"""
    env_file = ".env"
    env_example = "env.example"
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            print(f"Creating {env_file} from {env_example}...")
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print(f"✅ {env_file} created! Please edit it with your Gemini API key.")
        else:
            print(f"❌ {env_example} not found!")
            return False
    else:
        print(f"✅ {env_file} already exists!")
    
    return True

def check_gemini_key():
    """Check if Gemini API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⚠️  Warning: GEMINI_API_KEY not configured!")
        print("Please edit .env file and add your Gemini API key.")
        return False
    else:
        print("✅ Gemini API key is configured!")
        return True

def main():
    """Main setup function"""
    print("🏥 Medical Report Analyzer API Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Check API key
    if not check_gemini_key():
        print("\n📝 Next steps:")
        print("1. Get your Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Edit .env file and replace 'your_gemini_api_key_here' with your actual key")
        print("3. Run: python app.py")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("Run 'python app.py' to start the server.")

if __name__ == "__main__":
    main()
