"""
Test WhatsApp Manager Route
"""
import requests
import time

print("Testing WhatsApp Manager URL...")
print("=" * 60)

# Wait for server to start
time.sleep(3)

try:
    # Test WhatsApp Manager page
    response = requests.get("http://localhost:5000/whatsapp-manager", timeout=10)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Length: {len(response.text)} characters")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! WhatsApp Manager page is working!")
        print("\nOpen in browser: http://localhost:5000/whatsapp-manager")
        
        # Check if it's HTML
        if "WhatsApp" in response.text:
            print("✅ Page contains 'WhatsApp' - Content is correct!")
        else:
            print("⚠️  Page might not contain expected content")
    elif response.status_code == 404:
        print("\n❌ 404 NOT FOUND!")
        print("\nPossible issues:")
        print("  1. Server is not running")
        print("  2. Route is not registered")
        print("  3. File whatsapp_manager.html is missing")
    else:
        print(f"\n⚠️  Unexpected status code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Cannot connect to server!")
    print("\nPossible issues:")
    print("  1. Server is not running")
    print("  2. Server is on a different port")
    print("  3. Firewall is blocking the connection")
    print("\nSolution:")
    print("  Run: python api_routes.py")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)
