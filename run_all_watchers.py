#!/usr/bin/env python
"""
CLI Command to Run All Watchers
Personal AI Employee System
"""

import subprocess
import time
import sys
import os

def print_header(text):
    print("=" * 70)
    print(f"  {text}")
    print("=" * 70)
    print()

def start_watcher(name, command):
    print(f"🚀 Starting {name}...")
    try:
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        time.sleep(2)
        print(f"✅ {name} started!")
        print()
        return True
    except Exception as e:
        print(f"❌ Error starting {name}: {e}")
        print()
        return False

def main():
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print_header("PERSONAL AI EMPLOYEE - ALL WATCHERS")
    
    print("Starting all watchers and services...\n")
    
    # Start watchers
    watchers = [
        ("Gmail Watcher", "python AI_Employee_System\\Watchers\\start_gmail_watcher.py"),
        ("File Watcher", "python AI_Employee_System\\Watchers\\start_file_watcher.py"),
        ("WhatsApp Watcher", "python AI_Employee_System\\Watchers\\start_whatsapp_watcher.py"),
        ("MCP Server", "python run_mcp_server.py"),
    ]
    
    success_count = 0
    for name, command in watchers:
        if start_watcher(name, command):
            success_count += 1
    
    # Print summary
    print()
    print_header("ALL WATCHERS STARTED!")
    print(f"✅ Services Running: {success_count}/{len(watchers)}")
    print()
    print("Services:")
    for name, _ in watchers:
        print(f"  ✓ {name}")
    print()
    print("Access URLs:")
    print("  Dashboard:    http://localhost:5000")
    print("  MCP API:      http://localhost:5000/api/mcp/servers")
    print("  Agent Skills: http://localhost:5000/agent-skills")
    print()
    print("To stop watchers:")
    print("  - Close each console window")
    print("  - Or press Ctrl+C in each window")
    print("=" * 70)
    print()
    
    # Keep script running
    try:
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\nStopping all watchers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
