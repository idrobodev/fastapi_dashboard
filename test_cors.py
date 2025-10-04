#!/usr/bin/env python3
"""
Script to test CORS configuration
"""
import requests
import sys

def test_cors():
    """Test CORS configuration"""
    base_url = "http://localhost:8081"
    origin = "http://localhost:3001"
    
    print("Testing CORS configuration...")
    print(f"Base URL: {base_url}")
    print(f"Origin: {origin}")
    print("-" * 50)
    
    try:
        # Test 1: OPTIONS preflight request
        print("\n1. Testing OPTIONS preflight request...")
        headers = {
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type"
        }
        response = requests.options(f"{base_url}/api/health", headers=headers)
        print(f"   Status Code: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
        print(f"   Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'NOT SET')}")
        print(f"   Access-Control-Allow-Credentials: {response.headers.get('Access-Control-Allow-Credentials', 'NOT SET')}")
        
        if response.status_code == 200:
            print("   ✓ OPTIONS request successful")
        else:
            print("   ✗ OPTIONS request failed")
            return False
        
        # Test 2: GET request with Origin header
        print("\n2. Testing GET request with Origin header...")
        headers = {"Origin": origin}
        response = requests.get(f"{base_url}/api/health", headers=headers)
        print(f"   Status Code: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        print(f"   Access-Control-Allow-Credentials: {response.headers.get('Access-Control-Allow-Credentials', 'NOT SET')}")
        
        if response.status_code == 200 and response.headers.get('Access-Control-Allow-Origin') == origin:
            print("   ✓ GET request successful with correct CORS headers")
        else:
            print("   ✗ GET request failed or missing CORS headers")
            return False
        
        # Test 3: POST request with Origin header
        print("\n3. Testing POST request with Origin header...")
        headers = {
            "Origin": origin,
            "Content-Type": "application/json"
        }
        response = requests.options(f"{base_url}/api/participantes", headers=headers)
        print(f"   Status Code: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        
        if response.status_code == 200:
            print("   ✓ POST preflight successful")
        else:
            print("   ✗ POST preflight failed")
            return False
        
        print("\n" + "=" * 50)
        print("✓ All CORS tests passed!")
        print("=" * 50)
        return True
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the server.")
        print("   Make sure the FastAPI server is running on port 8081")
        print("   Run: uvicorn main:app --host 0.0.0.0 --port 8081")
        return False
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_cors()
    sys.exit(0 if success else 1)
