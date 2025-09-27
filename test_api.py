#!/usr/bin/env python3
"""
Test script for Glacier Care API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False
    return True

def test_analyze_endpoint():
    """Test the analyze endpoint with sample medical report"""
    print("\nTesting analyze endpoint...")
    
    sample_report = """
    PATIENT: John Doe
    DATE: 2024-01-15
    
    LABORATORY RESULTS:
    - Hemoglobin: 9.8 g/dL (Reference: 12-16 g/dL)
    - Blood Sugar (Fasting): 95 mg/dL (Reference: 70-100 mg/dL)
    - Total Cholesterol: 180 mg/dL (Reference: <200 mg/dL)
    - LDL Cholesterol: 120 mg/dL (Reference: <100 mg/dL)
    - HDL Cholesterol: 45 mg/dL (Reference: >40 mg/dL)
    
    MEDICATIONS:
    - Metformin 500mg twice daily
    - Lisinopril 10mg once daily
    
    IMPRESSION:
    Patient shows mild anemia with low hemoglobin levels. Blood sugar and cholesterol levels are within normal limits. Continue current medications and follow up in 3 months.
    """
    
    payload = {
        "reportText": sample_report,
        "filename": "test_report.txt"
    }
    
    try:
        print("Sending analysis request...")
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                print("✅ Analysis completed successfully!")
                data = result["data"]
                print(f"Risk Level: {data['riskLevel']}")
                print(f"Key Findings: {len(data['keyFindings'])} items")
                print(f"Recommendations: {len(data['recommendations'])} items")
                print(f"Medications: {len(data['medicationDetails'])} items")
                
                # Print first key finding
                if data['keyFindings']:
                    print(f"First finding: {data['keyFindings'][0]}")
                
                return True
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return False

def test_error_handling():
    """Test error handling with invalid input"""
    print("\nTesting error handling...")
    
    # Test empty report
    payload = {"reportText": ""}
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        if response.status_code == 400:
            print("✅ Empty report validation works")
        else:
            print(f"❌ Empty report validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing empty report: {str(e)}")
    
    # Test missing field
    payload = {"filename": "test.txt"}
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        if response.status_code == 400:
            print("✅ Missing field validation works")
        else:
            print(f"❌ Missing field validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing missing field: {str(e)}")

def main():
    """Run all tests"""
    print("🧪 Glacier Care API Tests")
    print("=" * 40)
    
    # Test health check
    if not test_health_check():
        print("\n❌ Cannot proceed with tests. Please start the server first:")
        print("python app.py")
        return
    
    # Test analyze endpoint
    test_analyze_endpoint()
    
    # Test error handling
    test_error_handling()
    
    print("\n🎉 Tests completed!")

if __name__ == "__main__":
    main()
