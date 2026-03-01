#!/usr/bin/env python
"""
WhatsApp Watcher CLI
Run WhatsApp Watcher individually
Personal AI Employee System
"""

import subprocess
import sys
import os

def main():
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=" * 70)
    print("  WHATSAPP WATCHER - Personal AI Employee")
    print("=" * 70)
    print()
    print("Starting WhatsApp Watcher...")
    print()
    
    try:
        # Start WhatsApp watcher
        subprocess.run([
            sys.executable,
            "AI_Employee_System\\Watchers\\start_whatsapp_watcher.py"
        ])
    except KeyboardInterrupt:
        print("\n\nStopping WhatsApp Watcher...")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("=" * 70)
    print("WhatsApp Watcher stopped.")
    print("=" * 70)

if __name__ == "__main__":
    main()
