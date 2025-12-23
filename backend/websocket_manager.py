# WebSocket Manager for Real-Time AI Assistant
# Handles connection lifecycle, streaming responses, and session management

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional, Any
import json
import logging
import uuid
from datetime import datetime
from cache_manager import cache_manager
from models import AssistantRequest, AssistantMode, TaskType

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections and message routing"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str, user_id: str = "anonymous"):
        """Accept and register WebSocket connection"""
        await websocket.accept()
        
        self.active_connections[session_id] = websocket
        self.connection_metadata[session_id] = {
            "user_id": user_id,
            "connected_at": datetime.utcnow().isoformat(),
            "message_count": 0,
            "mode": "strategist"
        }
        
        # Store session in Redis
        await cache_manager.store_session(session_id, self.connection_metadata[session_id])
        
        logger.info(f"✅ WebSocket connected: {session_id} (user: {user_id})")
        
        # Send welcome message
        await self.send_message(session_id, {
            "type": "connected",
            "session_id": session_id,
            "message": "🤖 **ActionEDx AI Assistant Connected**\n\nI'm your AI Innovation Assistant. I can help you with:\n\n- 9-Pillar Strategy Audits\n- Tri-Core Loop Execution Planning\n- House of Hearts Peer Reviews\n- Learning Path Generation\n- Real-time Collaboration\n\nHow can I help you execute your innovation journey today?",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        
        if session_id in self.connection_metadata:
            del self.connection_metadata[session_id]
        
        logger.info(f"❌ WebSocket disconnected: {session_id}")
    
    async def send_message(self, session_id: str, message: Dict[str, Any]):
        """Send message to specific connection"""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(message)
            except Exception as e:
                logger.error(f"Send message error: {e}")
                self.disconnect(session_id)
    
    async def stream_chunk(self, session_id: str, chunk: str, chunk_number: int = 0):
        """Stream a chunk of text to client"""
        await self.send_message(session_id, {
            "type": "stream_chunk",
            "chunk_number": chunk_number,
            "content": chunk,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def stream_start(self, session_id: str, task_type: str, model: str):
        """Signal start of streaming response"""
        await self.send_message(session_id, {
            "type": "stream_start",
            "task_type": task_type,
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def stream_end(self, session_id: str, metadata: Dict[str, Any] = None):
        """Signal end of streaming response"""
        await self.send_message(session_id, {
            "type": "stream_end",
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def send_error(self, session_id: str, error_message: str, error_type: str = "general"):
        """Send error message to client"""
        await self.send_message(session_id, {
            "type": "error",
            "error_type": error_type,
            "message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def send_typing_indicator(self, session_id: str, is_typing: bool = True):
        """Send typing indicator"""
        await self.send_message(session_id, {
            "type": "typing",
            "is_typing": is_typing,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def increment_message_count(self, session_id: str):
        """Track message count for session"""
        if session_id in self.connection_metadata:
            self.connection_metadata[session_id]["message_count"] += 1
            await cache_manager.update_session(session_id, {
                "message_count": self.connection_metadata[session_id]["message_count"]
            })
    
    def get_active_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    def get_connection_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get connection metadata"""
        return self.connection_metadata.get(session_id)
    
    async def broadcast(self, message: Dict[str, Any], exclude_sessions: List[str] = None):
        """Broadcast message to all active connections"""
        exclude = exclude_sessions or []
        
        for session_id in list(self.active_connections.keys()):
            if session_id not in exclude:
                await self.send_message(session_id, message)
    
    async def send_system_message(self, session_id: str, message: str):
        """Send system message to client"""
        await self.send_message(session_id, {
            "type": "system",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })


# Singleton instance
connection_manager = ConnectionManager()
