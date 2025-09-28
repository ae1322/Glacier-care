#!/usr/bin/env python3
"""
Installation script for enhanced scanner packages
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all enhanced scanner packages"""
    print("🔧 Installing Enhanced Scanner Packages for Glacier Care")
    print("=" * 60)
    
    packages = [
        "Pillow==10.1.0",
        "pytesseract==0.3.10", 
        "opencv-python==4.8.1.78",
        "pdf2image==1.16.3",
        "easyocr==1.7.0",
        "pymupdf==1.23.8"
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package in packages:
        print(f"\n📦 Installing {package}...")
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Installation Summary: {success_count}/{total_packages} packages installed successfully")
    
    if success_count == total_packages:
        print("🎉 All packages installed successfully!")
        print("\n📋 Next steps:")
        print("1. Install Tesseract OCR on your system:")
        print("   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - macOS: brew install tesseract")
        print("   - Linux: sudo apt-get install tesseract-ocr")
        print("2. Restart your Flask server")
        print("3. Test the enhanced scanner functionality")
    else:
        print("⚠️  Some packages failed to install. Check the errors above.")
        print("You may need to install system dependencies first.")
    
    print("\n🏔️ Glacier Care Enhanced Scanner is ready!")

if __name__ == "__main__":
    main()
