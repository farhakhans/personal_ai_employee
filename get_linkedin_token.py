"""
LinkedIn Token Generator - Get Your Access Token
================================================
Yeh script LinkedIn OAuth flow complete karti hai aur access token leti hai.

Usage:
1. Pehle LinkedIn Developer Portal se Client ID aur Client Secret lein
2. Yeh script run karein
3. Browser mein authorization complete karein
4. Token .env file mein automatically save ho jayega
"""

import os
import sys
import webbrowser
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

# Load existing .env
load_dotenv()

# LinkedIn OAuth URLs
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "w_member_social r_liteprofile"

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    """Handle OAuth callback from LinkedIn"""
    
    def do_GET(self):
        global auth_code
        
        # Parse the callback URL
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head>
                <title>LinkedIn Authorization Complete</title>
                <style>
                    body { font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #0077b5, #00a0dc); color: white; }
                    .success { background: white; color: #0077b5; padding: 30px; border-radius: 10px; display: inline-block; }
                </style>
            </head>
            <body>
                <div class="success">
                    <h1>✅ Authorization Successful!</h1>
                    <p>You can close this window and return to the console.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Authorization failed')
        
        # Shutdown server after handling request
        threading.Thread(target=self.server.shutdown).start()

def get_linkedin_token(client_id, client_secret):
    """Get LinkedIn access token using OAuth flow"""
    global auth_code
    auth_code = None
    
    print("\n" + "="*60)
    print("LINKEDIN TOKEN GENERATOR")
    print("="*60)
    
    # Step 1: Open authorization URL in browser
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    
    auth_url = f"{AUTH_URL}?response_type={auth_params['response_type']}&client_id={auth_params['client_id']}&redirect_uri={auth_params['redirect_uri']}&scope={auth_params['scope']}"
    
    print("\n📋 Step 1: Opening LinkedIn authorization page...")
    print(f"   URL: {auth_url[:100]}...")
    
    webbrowser.open(auth_url)
    
    # Step 2: Start local server to receive callback
    print("\n⏳ Step 2: Waiting for authorization...")
    print("   Please authorize the app in your browser.")
    
    with socketserver.TCPServer(("", 8080), OAuthHandler) as httpd:
        httpd.handle_request()
    
    if not auth_code:
        print("\n❌ Authorization failed. No code received.")
        return None
    
    print("\n✅ Authorization code received!")
    
    # Step 3: Exchange code for access token
    print("\n📋 Step 3: Exchanging code for access token...")
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        response = requests.post(TOKEN_URL, data=token_data)
        result = response.json()
        
        if response.status_code == 200 and 'access_token' in result:
            access_token = result['access_token']
            expires_in = result.get('expires_in', 5183999)  # ~60 days
            
            print("\n✅ SUCCESS! Access token received!")
            print(f"   Token: {access_token[:20]}...{access_token[-10:]}")
            print(f"   Expires in: {expires_in // 86400} days")
            
            # Get person URN
            print("\n📋 Getting your Person URN...")
            headers = {'Authorization': f'Bearer {access_token}'}
            profile_response = requests.get(
                'https://api.linkedin.com/v2/me',
                headers=headers
            )
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                person_urn = profile.get('id', '')
                print(f"✅ Person URN: {person_urn}")
                
                # Save to .env
                save_to_env(access_token, person_urn)
                
                return access_token, person_urn
            else:
                print(f"❌ Failed to get profile: {profile_response.text}")
                return access_token, None
        else:
            print(f"\n❌ Token request failed: {result}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def save_to_env(access_token, person_urn):
    """Save credentials to .env file"""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    # Read existing content
    existing_content = ""
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # Update or add values
    new_lines = []
    updated = {
        'LINKEDIN_ACCESS_TOKEN': False,
        'LINKEDIN_PERSON_URN': False
    }
    
    for line in existing_content.split('\n'):
        if line.startswith('LINKEDIN_ACCESS_TOKEN='):
            new_lines.append(f'LINKEDIN_ACCESS_TOKEN={access_token}')
            updated['LINKEDIN_ACCESS_TOKEN'] = True
        elif line.startswith('LINKEDIN_PERSON_URN='):
            new_lines.append(f'LINKEDIN_PERSON_URN={person_urn}')
            updated['LINKEDIN_PERSON_URN'] = True
        else:
            new_lines.append(line)
    
    # Add missing values
    if not updated['LINKEDIN_ACCESS_TOKEN']:
        new_lines.append(f'LINKEDIN_ACCESS_TOKEN={access_token}')
    if not updated['LINKEDIN_PERSON_URN'] and person_urn:
        new_lines.append(f'LINKEDIN_PERSON_URN={person_urn}')
    
    # Write back
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"\n💾 Credentials saved to .env file!")
    print(f"   📁 Location: {env_file}")

def main():
    """Main function"""
    print("\n🔐 LinkedIn Token Generator")
    print("="*60)
    print("\nYeh script LinkedIn OAuth flow complete karti hai.")
    print("\nPehle LinkedIn Developer Portal se credentials lein:")
    print("1. https://www.linkedin.com/developers/ par jayein")
    print("2. App create karein")
    print("3. Client ID aur Client Secret note karein")
    print("="*60)
    
    # Check if credentials already in .env
    client_id = os.getenv('LINKEDIN_CLIENT_ID', '')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', '')
    
    if not client_id or not client_secret:
        print("\n📝 Enter your LinkedIn App credentials:")
        client_id = input("\nClient ID: ").strip()
        client_secret = input("Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("\n❌ Client ID aur Client Secret zaroori hain!")
        print("\nAlternative: Direct token generate karein:")
        print(f"\nYeh URL browser mein open karein:")
        print(f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri=https://localhost&scope=w_member_social")
        return
    
    # Get token
    result = get_linkedin_token(client_id, client_secret)
    
    if result:
        access_token, person_urn = result
        print("\n" + "="*60)
        print("✅ TOKEN GENERATION COMPLETE!")
        print("="*60)
        print("\nAb aap LinkedIn par post kar sakte hain!")
        print("\nTest karein:")
        print("  1. Flask server start karein: python api_routes.py")
        print("  2. Browser mein jayein: http://localhost:5000/test-linkedin")
        print("  3. 'Test Connection' click karein")
        print("  4. Post likh kar 'Post to LinkedIn' click karein")
        print("="*60)
    else:
        print("\n❌ Token generation failed.")
        print("\nManual setup ke liye yeh URL try karein:")
        print(f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri=https://localhost&scope=w_member_social")

if __name__ == "__main__":
    import threading
    main()
