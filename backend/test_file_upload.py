"""
Test script for file upload PRD API endpoint
"""

import requests
import os

def test_file_upload_api():
    """Test the file upload PRD API endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/api/prd/file"
    
    # Create a test file
    test_content = """
    This is a test PRD document.
    
    Product Requirements Document for Test System
    
    Overview:
    This system will provide compliance detection capabilities for user data.
    
    Features:
    1. Data Collection - Collect user data for analysis
    2. Compliance Checking - Check data against regulations
    3. Reporting - Generate compliance reports
    
    Technical Requirements:
    - API integration
    - Database storage
    - User authentication
    - Audit logging
    """
    
    # Create test file
    with open("test_prd.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        # Prepare form data
        with open("test_prd.txt", "rb") as f:
            files = {"file": ("test_prd.txt", f, "text/plain")}
            data = {
                "Name": "Test PRD from File",
                "Status": "Draft"
            }
            
            # Make request
            response = requests.post(url, files=files, data=data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 201:
                print("✅ File upload API test passed!")
                return True
            else:
                print("❌ File upload API test failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error testing file upload API: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists("test_prd.txt"):
            os.remove("test_prd.txt")

if __name__ == "__main__":
    print("🧪 Testing File Upload PRD API")
    print("=" * 40)
    
    success = test_file_upload_api()
    
    if success:
        print("\n🎉 File upload API test completed successfully!")
    else:
        print("\n❌ File upload API test failed!")
