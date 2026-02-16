"""
MCP (Model Context Protocol) COORDINATOR
═══════════════════════════════════════════════════════════════════════════

Central coordinator for MCP servers.
Claude Code uses MCP servers as "hands" to interact with external systems.

Supported MCP Servers:
  1. Filesystem MCP - Read/write/list files in vault
  2. Email MCP - Send, draft, search emails
  3. Browser MCP - Navigate web, fill forms (payment portals)
  4. Calendar MCP - Create, update events
  5. Slack MCP - Send messages, read channels
  6. WhatsApp MCP - Send/post on WhatsApp & social
  7. Payment MCP - Process payments, check balances
  8. Approval MCP - Human-in-the-loop approval workflow

Each MCP server is a capability that Claude can invoke.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod


class MCPServerType(Enum):
    """Available MCP server types."""
    FILESYSTEM = "filesystem"
    EMAIL = "email"
    BROWSER = "browser"
    CALENDAR = "calendar"
    SLACK = "slack"
    WHATSAPP = "whatsapp"
    PAYMENT = "payment"
    APPROVAL = "approval"


@dataclass
class MCPRequest:
    """Request to invoke an MCP server capability."""
    server_type: MCPServerType
    capability: str
    params: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'server_type': self.server_type.value,
            'capability': self.capability,
            'params': self.params,
            'description': self.description,
            'timestamp': self.timestamp,
        }


@dataclass
class MCPResponse:
    """Response from MCP server invocation."""
    success: bool
    result: Any = None
    error: Optional[str] = None
    server_type: str = ""
    capability: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class MCPServer(ABC):
    """Abstract base class for MCP servers."""
    
    def __init__(self, server_type: MCPServerType, config: Optional[Dict] = None):
        self.server_type = server_type
        self.config = config or {}
        self.logger = logging.getLogger(f"MCP.{server_type.value}")
        self.capabilities: List[str] = []
    
    @abstractmethod
    def invoke(self, capability: str, params: Dict) -> MCPResponse:
        """Invoke a capability on this MCP server."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of available capabilities."""
        pass


class FilesystemMCP(MCPServer):
    """Filesystem MCP - Read/write/list files in vault."""
    
    def __init__(self, vault_path: Path):
        super().__init__(MCPServerType.FILESYSTEM, {'vault_path': str(vault_path)})
        self.vault_path = Path(vault_path)
        self.capabilities = [
            'read_file',
            'write_file',
            'list_directory',
            'delete_file',
            'move_file',
            'file_exists',
            'get_file_info',
        ]
    
    def invoke(self, capability: str, params: Dict) -> MCPResponse:
        """Invoke filesystem capability."""
        try:
            if capability == 'read_file':
                return self._read_file(params)
            elif capability == 'write_file':
                return self._write_file(params)
            elif capability == 'list_directory':
                return self._list_directory(params)
            elif capability == 'delete_file':
                return self._delete_file(params)
            elif capability == 'move_file':
                return self._move_file(params)
            elif capability == 'file_exists':
                return self._file_exists(params)
            elif capability == 'get_file_info':
                return self._get_file_info(params)
            else:
                return MCPResponse(False, error=f"Unknown capability: {capability}")
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _read_file(self, params: Dict) -> MCPResponse:
        """Read file from vault."""
        path = self.vault_path / params.get('path', '')
        if not path.exists():
            return MCPResponse(False, error=f"File not found: {path}")
        
        try:
            content = path.read_text()
            return MCPResponse(True, result={'content': content, 'path': str(path)})
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _write_file(self, params: Dict) -> MCPResponse:
        """Write file to vault."""
        path = self.vault_path / params.get('path', '')
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            path.write_text(params.get('content', ''))
            return MCPResponse(True, result={'path': str(path), 'size': path.stat().st_size})
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _list_directory(self, params: Dict) -> MCPResponse:
        """List directory contents."""
        path = self.vault_path / params.get('path', '')
        if not path.exists():
            return MCPResponse(False, error=f"Directory not found: {path}")
        
        try:
            items = [
                {'name': f.name, 'type': 'dir' if f.is_dir() else 'file'}
                for f in sorted(path.iterdir())
            ]
            return MCPResponse(True, result={'items': items, 'path': str(path)})
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _delete_file(self, params: Dict) -> MCPResponse:
        """Delete file from vault."""
        path = self.vault_path / params.get('path', '')
        if not path.exists():
            return MCPResponse(False, error=f"File not found: {path}")
        
        try:
            path.unlink()
            return MCPResponse(True, result={'path': str(path), 'deleted': True})
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _move_file(self, params: Dict) -> MCPResponse:
        """Move file to different location."""
        old_path = self.vault_path / params.get('from', '')
        new_path = self.vault_path / params.get('to', '')
        
        if not old_path.exists():
            return MCPResponse(False, error=f"File not found: {old_path}")
        
        try:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.rename(new_path)
            return MCPResponse(True, result={'from': str(old_path), 'to': str(new_path)})
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _file_exists(self, params: Dict) -> MCPResponse:
        """Check if file exists."""
        path = self.vault_path / params.get('path', '')
        exists = path.exists()
        return MCPResponse(True, result={'exists': exists, 'path': str(path)})
    
    def _get_file_info(self, params: Dict) -> MCPResponse:
        """Get file metadata."""
        path = self.vault_path / params.get('path', '')
        if not path.exists():
            return MCPResponse(False, error=f"File not found: {path}")
        
        try:
            stat = path.stat()
            return MCPResponse(True, result={
                'path': str(path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'is_file': path.is_file(),
                'is_dir': path.is_dir(),
            })
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def get_capabilities(self) -> List[str]:
        """Return available capabilities."""
        return self.capabilities


class EmailMCP(MCPServer):
    """Email MCP - Send, draft, search emails."""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(MCPServerType.EMAIL, config)
        self.capabilities = [
            'send_email',
            'draft_email',
            'search_emails',
            'get_draft',
            'delete_draft',
        ]
    
    def invoke(self, capability: str, params: Dict) -> MCPResponse:
        """Invoke email capability."""
        try:
            if capability == 'send_email':
                return self._send_email(params)
            elif capability == 'draft_email':
                return self._draft_email(params)
            elif capability == 'search_emails':
                return self._search_emails(params)
            elif capability == 'get_draft':
                return self._get_draft(params)
            elif capability == 'delete_draft':
                return self._delete_draft(params)
            else:
                return MCPResponse(False, error=f"Unknown capability: {capability}")
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _send_email(self, params: Dict) -> MCPResponse:
        """Send email (requires approval in real implementation)."""
        # In real implementation, would use Gmail API
        # This is a mock implementation
        return MCPResponse(True, result={
            'to': params.get('to'),
            'subject': params.get('subject'),
            'status': 'sent',
            'requires_approval': True,
        })
    
    def _draft_email(self, params: Dict) -> MCPResponse:
        """Create draft email (safe, no approval needed)."""
        return MCPResponse(True, result={
            'to': params.get('to'),
            'subject': params.get('subject'),
            'body': params.get('body'),
            'status': 'draft',
        })
    
    def _search_emails(self, params: Dict) -> MCPResponse:
        """Search existing emails."""
        # Mock implementation
        return MCPResponse(True, result={
            'query': params.get('query'),
            'results': [],
            'count': 0,
        })
    
    def _get_draft(self, params: Dict) -> MCPResponse:
        """Get draft email."""
        return MCPResponse(True, result={'draft_id': params.get('draft_id')})
    
    def _delete_draft(self, params: Dict) -> MCPResponse:
        """Delete draft email."""
        return MCPResponse(True, result={'draft_id': params.get('draft_id'), 'deleted': True})
    
    def get_capabilities(self) -> List[str]:
        """Return available capabilities."""
        return self.capabilities


class BrowserMCP(MCPServer):
    """Browser MCP - Navigate web, fill forms."""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(MCPServerType.BROWSER, config)
        self.capabilities = [
            'navigate_to',
            'fill_form',
            'click_element',
            'get_page_content',
            'wait_for_element',
        ]
    
    def invoke(self, capability: str, params: Dict) -> MCPResponse:
        """Invoke browser capability."""
        try:
            if capability == 'navigate_to':
                return self._navigate_to(params)
            elif capability == 'fill_form':
                return self._fill_form(params)
            elif capability == 'click_element':
                return self._click_element(params)
            elif capability == 'get_page_content':
                return self._get_page_content(params)
            elif capability == 'wait_for_element':
                return self._wait_for_element(params)
            else:
                return MCPResponse(False, error=f"Unknown capability: {capability}")
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _navigate_to(self, params: Dict) -> MCPResponse:
        """Navigate to URL."""
        return MCPResponse(True, result={
            'url': params.get('url'),
            'status': 'navigated',
            'requires_approval': True,
        })
    
    def _fill_form(self, params: Dict) -> MCPResponse:
        """Fill form fields."""
        return MCPResponse(True, result={
            'fields_filled': len(params.get('fields', {})),
            'requires_approval': True,
        })
    
    def _click_element(self, params: Dict) -> MCPResponse:
        """Click element on page."""
        return MCPResponse(True, result={
            'element': params.get('selector'),
            'clicked': True,
            'requires_approval': True,
        })
    
    def _get_page_content(self, params: Dict) -> MCPResponse:
        """Get page content (read-only, safe)."""
        return MCPResponse(True, result={
            'content': 'Page content here',
            'requires_approval': False,
        })
    
    def _wait_for_element(self, params: Dict) -> MCPResponse:
        """Wait for element to appear."""
        return MCPResponse(True, result={
            'selector': params.get('selector'),
            'found': True,
            'requires_approval': False,
        })
    
    def get_capabilities(self) -> List[str]:
        """Return available capabilities."""
        return self.capabilities


class CalendarMCP(MCPServer):
    """Calendar MCP - Create, update events."""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(MCPServerType.CALENDAR, config)
        self.capabilities = [
            'create_event',
            'update_event',
            'delete_event',
            'list_events',
            'get_event',
        ]
    
    def invoke(self, capability: str, params: Dict) -> MCPResponse:
        """Invoke calendar capability."""
        try:
            if capability == 'create_event':
                return self._create_event(params)
            elif capability == 'update_event':
                return self._update_event(params)
            elif capability == 'delete_event':
                return self._delete_event(params)
            elif capability == 'list_events':
                return self._list_events(params)
            elif capability == 'get_event':
                return self._get_event(params)
            else:
                return MCPResponse(False, error=f"Unknown capability: {capability}")
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _create_event(self, params: Dict) -> MCPResponse:
        """Create calendar event."""
        return MCPResponse(True, result={
            'event_id': 'evt_123',
            'title': params.get('title'),
            'start': params.get('start'),
            'end': params.get('end'),
            'created': True,
        })
    
    def _update_event(self, params: Dict) -> MCPResponse:
        """Update calendar event."""
        return MCPResponse(True, result={
            'event_id': params.get('event_id'),
            'updated': True,
        })
    
    def _delete_event(self, params: Dict) -> MCPResponse:
        """Delete calendar event."""
        return MCPResponse(True, result={
            'event_id': params.get('event_id'),
            'deleted': True,
        })
    
    def _list_events(self, params: Dict) -> MCPResponse:
        """List calendar events."""
        return MCPResponse(True, result={
            'events': [],
            'count': 0,
        })
    
    def _get_event(self, params: Dict) -> MCPResponse:
        """Get event details."""
        return MCPResponse(True, result={
            'event_id': params.get('event_id'),
            'title': 'Event Title',
        })
    
    def get_capabilities(self) -> List[str]:
        """Return available capabilities."""
        return self.capabilities


class ApprovalMCP(MCPServer):
    """Approval MCP - Human-in-the-loop workflow."""
    
    def __init__(self, vault_path: Path):
        super().__init__(MCPServerType.APPROVAL, {'vault_path': str(vault_path)})
        self.vault_path = Path(vault_path)
        self.capabilities = [
            'request_approval',
            'check_approval_status',
            'list_pending_approvals',
            'approve_request',
            'reject_request',
        ]
    
    def invoke(self, capability: str, params: Dict) -> MCPResponse:
        """Invoke approval capability."""
        try:
            if capability == 'request_approval':
                return self._request_approval(params)
            elif capability == 'check_approval_status':
                return self._check_approval_status(params)
            elif capability == 'list_pending_approvals':
                return self._list_pending_approvals(params)
            elif capability == 'approve_request':
                return self._approve_request(params)
            elif capability == 'reject_request':
                return self._reject_request(params)
            else:
                return MCPResponse(False, error=f"Unknown capability: {capability}")
        except Exception as e:
            return MCPResponse(False, error=str(e))
    
    def _request_approval(self, params: Dict) -> MCPResponse:
        """Request approval for action."""
        approval_id = f"APPROVAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create approval file
        approval_file = self.vault_path / "Pending_Approval" / f"{approval_id}.md"
        approval_file.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"""# Approval Required: {params.get('action', 'Action')}

**Requested By:** Claude Code
**Timestamp:** {datetime.now().isoformat()}
**Approval ID:** {approval_id}

## Action Details

{params.get('description', 'No description')}

## Parameters

```json
{json.dumps(params.get('params', {}), indent=2)}
```

## Status
- [ ] Approved
- [ ] Rejected

## Reviewer Notes
Add your notes here before approving/rejecting.
"""
        
        approval_file.write_text(content)
        
        return MCPResponse(True, result={
            'approval_id': approval_id,
            'status': 'pending',
            'file': str(approval_file),
        })
    
    def _check_approval_status(self, params: Dict) -> MCPResponse:
        """Check approval status."""
        approval_id = params.get('approval_id')
        
        # Check if file exists in Approved folder
        approved_file = self.vault_path / "Approved" / f"{approval_id}.md"
        pending_file = self.vault_path / "Pending_Approval" / f"{approval_id}.md"
        
        if approved_file.exists():
            return MCPResponse(True, result={'status': 'approved'})
        elif pending_file.exists():
            return MCPResponse(True, result={'status': 'pending'})
        else:
            return MCPResponse(True, result={'status': 'unknown'})
    
    def _list_pending_approvals(self, params: Dict) -> MCPResponse:
        """List pending approvals."""
        pending_dir = self.vault_path / "Pending_Approval"
        
        if not pending_dir.exists():
            return MCPResponse(True, result={'approvals': [], 'count': 0})
        
        approvals = [f.name for f in pending_dir.glob("APPROVAL_*.md")]
        return MCPResponse(True, result={
            'approvals': approvals,
            'count': len(approvals),
        })
    
    def _approve_request(self, params: Dict) -> MCPResponse:
        """Move approval to Approved folder."""
        approval_id = params.get('approval_id')
        pending_file = self.vault_path / "Pending_Approval" / f"{approval_id}.md"
        approved_file = self.vault_path / "Approved" / f"{approval_id}.md"
        
        if not pending_file.exists():
            return MCPResponse(False, error=f"Approval not found: {approval_id}")
        
        approved_file.parent.mkdir(parents=True, exist_ok=True)
        pending_file.rename(approved_file)
        
        return MCPResponse(True, result={'approval_id': approval_id, 'approved': True})
    
    def _reject_request(self, params: Dict) -> MCPResponse:
        """Delete pending approval."""
        approval_id = params.get('approval_id')
        pending_file = self.vault_path / "Pending_Approval" / f"{approval_id}.md"
        
        if not pending_file.exists():
            return MCPResponse(False, error=f"Approval not found: {approval_id}")
        
        pending_file.unlink()
        
        return MCPResponse(True, result={'approval_id': approval_id, 'rejected': True})
    
    def get_capabilities(self) -> List[str]:
        """Return available capabilities."""
        return self.capabilities


class MCPCoordinator:
    """Coordinator for all MCP servers."""
    
    def __init__(self, vault_path: Path):
        """Initialize MCP coordinator with vault."""
        self.vault_path = Path(vault_path)
        self.logger = logging.getLogger("MCPCoordinator")
        
        # Initialize all MCP servers
        self.servers: Dict[MCPServerType, MCPServer] = {
            MCPServerType.FILESYSTEM: FilesystemMCP(vault_path),
            MCPServerType.EMAIL: EmailMCP(),
            MCPServerType.BROWSER: BrowserMCP(),
            MCPServerType.CALENDAR: CalendarMCP(),
            MCPServerType.APPROVAL: ApprovalMCP(vault_path),
        }
        
        # Track all invocations
        self.invocations_log: List[Dict] = []
    
    def invoke(self, request: MCPRequest) -> MCPResponse:
        """Invoke MCP capability."""
        self.logger.info(f"Invoking: {request.server_type.value}.{request.capability}")
        
        server = self.servers.get(request.server_type)
        if not server:
            return MCPResponse(False, error=f"Unknown server: {request.server_type.value}")
        
        # Check if approval needed
        if self._requires_approval(request):
            return self._request_approval_for(request)
        
        # Invoke capability
        response = server.invoke(request.capability, request.params)
        response.server_type = request.server_type.value
        response.capability = request.capability
        
        # Log invocation
        self._log_invocation(request, response)
        
        return response
    
    def _requires_approval(self, request: MCPRequest) -> bool:
        """Check if request requires approval."""
        # Read-only operations don't need approval
        read_only_capabilities = {
            'read_file', 'list_directory', 'file_exists', 'get_file_info',
            'search_emails', 'get_page_content', 'wait_for_element',
            'list_events', 'get_event',
        }
        
        return request.capability not in read_only_capabilities
    
    def _request_approval_for(self, request: MCPRequest) -> MCPResponse:
        """Request approval for sensitive operation."""
        approval_server = self.servers[MCPServerType.APPROVAL]
        
        approval_response = approval_server.invoke('request_approval', {
            'action': f"{request.server_type.value}.{request.capability}",
            'description': request.description,
            'params': request.params,
        })
        
        return MCPResponse(
            success=False,
            error="Approval required",
            result={'approval_id': approval_response.result.get('approval_id')}
        )
    
    def _log_invocation(self, request: MCPRequest, response: MCPResponse):
        """Log MCP invocation."""
        try:
            log_file = self.vault_path / "System" / "mcp_invocations.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'request': request.to_dict(),
                'response': response.to_dict(),
            }
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            self.logger.error(f"Could not log invocation: {e}")
    
    def get_server_capabilities(self) -> Dict[str, List[str]]:
        """Get all available capabilities."""
        return {
            server_type.value: server.get_capabilities()
            for server_type, server in self.servers.items()
        }
    
    def describe_servers(self) -> str:
        """Get human-readable description of all servers."""
        description = "# Available MCP Servers\n\n"
        
        for server_type, server in self.servers.items():
            capabilities = server.get_capabilities()
            description += f"## {server_type.value.upper()}\n"
            description += f"Capabilities: {', '.join(capabilities)}\n\n"
        
        return description


# Demo / Testing
if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(message)s'
    )
    
    # Create coordinator
    vault_path = Path("./Vault")
    coordinator = MCPCoordinator(vault_path)
    
    print("\n" + "="*70)
    print("MCP COORDINATOR - Demo")
    print("="*70)
    
    # Show available servers
    print("\n📋 Available MCP Servers:")
    print(coordinator.describe_servers())
    
    # Example: List vault contents
    print("\n🔍 Example: List Vault Contents")
    request = MCPRequest(
        server_type=MCPServerType.FILESYSTEM,
        capability='list_directory',
        params={'path': 'Inbox'},
        description='List files in Inbox folder'
    )
    
    response = coordinator.invoke(request)
    print(f"Response: {response.to_dict()}\n")
    
    # Example: Draft email (no approval needed)
    print("✉️  Example: Draft Email")
    request = MCPRequest(
        server_type=MCPServerType.EMAIL,
        capability='draft_email',
        params={
            'to': 'client@example.com',
            'subject': 'Project Update',
            'body': 'Here is your update...'
        },
        description='Draft response to client'
    )
    
    response = coordinator.invoke(request)
    print(f"Response: {response.to_dict()}\n")
