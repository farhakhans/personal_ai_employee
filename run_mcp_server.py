"""
Run MCP Server for Personal AI Employee
Model Context Protocol Server - Silver Tier
"""

import sys
import os

# Set encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'AI_Employee_System'))

from MCP_Servers.mcp_server_framework import MCPServerRegistry, EmailMCPServer, ApprovalMCPServer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)

logger = logging.getLogger("MCPServer")

print("=" * 70)
print("PERSONAL AI EMPLOYEE - MCP SERVER")
print("=" * 70)
print("")
print("Starting MCP Server...")
print("")

# Initialize registry
registry = MCPServerRegistry()

# Register Silver tier servers
registry.register_silver_servers()

print("✅ MCP Servers Registered:")
print("")
for name, caps in registry.list_servers().items():
    print(f"  📌 {name}")
    print(f"     Description: {caps['description']}")
    print(f"     Capabilities: {', '.join(caps['capabilities'])}")
    print("")

print("=" * 70)
print("MCP Server is running!")
print("")
print("Available Servers:")
for name in registry.servers.keys():
    print(f"  - {name}")
print("")
print("Press Ctrl+C to stop the server")
print("=" * 70)

# Keep server running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n\n🛑 MCP Server stopped by user")
    sys.exit(0)
