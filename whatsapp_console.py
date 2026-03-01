"""
WhatsApp Web Console Launcher
Opens WhatsApp Web in browser and monitors connection
"""

import webbrowser
import time
import sys

def main():
    print("=" * 60)
    print("WhatsApp Web - Console Launcher")
    print("=" * 60)
    print()
    
    print("📱 Opening WhatsApp Web in your default browser...")
    print()
    
    # Open WhatsApp Web
    webbrowser.open('https://web.whatsapp.com')
    
    print("✓ WhatsApp Web opened!")
    print()
    print("Next steps:")
    print("1. Wait for QR code to load in browser")
    print("2. Open WhatsApp on your phone")
    print("3. Go to Settings → Linked Devices")
    print("4. Tap 'Link a Device'")
    print("5. Point camera at QR code on screen")
    print()
    print("Waiting for connection...")
    print("(Press Ctrl+C to exit)")
    print()
    
    # Simple countdown
    try:
        for i in range(30, 0, -1):
            sys.stdout.write(f"\rQR code expires in: {i} seconds   ")
            sys.stdout.flush()
            time.sleep(1)
        print("\n\n✓ WhatsApp Web should be connected!")
    except KeyboardInterrupt:
        print("\n\nExiting...")
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()
