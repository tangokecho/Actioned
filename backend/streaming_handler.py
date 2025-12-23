# Advanced Streaming Handler for ActionEDx AI Backend
# Token-by-token streaming for AI responses

import asyncio
from typing import AsyncGenerator, Optional, Dict, Any, List
from emergentintegrations.llm.openai import LlmChat, UserMessage
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class StreamingHandler:
    """Handles token-by-token streaming from AI models"""
    
    def __init__(self):
        self.active_streams: Dict[str, bool] = {}
    
    async def stream_ai_response(
        self,
        llm_chat: LlmChat,
        user_message: UserMessage,
        stream_id: str,
        buffer_size: int = 5
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream AI response token by token
        
        Args:
            llm_chat: LLM chat instance
            user_message: User message to send
            stream_id: Unique stream identifier
            buffer_size: Number of tokens to buffer before yielding
        
        Yields:
            Dict with chunk data, metadata, and timing
        """
        
        self.active_streams[stream_id] = True
        start_time = time.time()
        total_tokens = 0
        chunk_number = 0
        buffer = []
        
        try:
            # Check if SDK supports streaming
            if hasattr(llm_chat, 'stream_message'):
                # Native streaming support
                async for token in llm_chat.stream_message(user_message):
                    if not self.active_streams.get(stream_id, False):
                        logger.info(f"Stream {stream_id} cancelled")
                        break
                    
                    buffer.append(token)
                    total_tokens += 1
                    
                    # Yield when buffer is full
                    if len(buffer) >= buffer_size:
                        chunk = ''.join(buffer)
                        chunk_number += 1
                        
                        yield {
                            \"type\": \"chunk\",
                            \"chunk_number\": chunk_number,
                            \"content\": chunk,
                            \"tokens_in_chunk\": len(buffer),
                            \"total_tokens\": total_tokens,
                            \"elapsed_seconds\": time.time() - start_time,
                            \"timestamp\": datetime.utcnow().isoformat()
                        }
                        
                        buffer = []
                        
                        # Small delay to prevent overwhelming the client
                        await asyncio.sleep(0.01)
                
                # Yield remaining buffer
                if buffer:
                    chunk = ''.join(buffer)
                    chunk_number += 1
                    
                    yield {
                        \"type\": \"chunk\",
                        \"chunk_number\": chunk_number,
                        \"content\": chunk,
                        \"tokens_in_chunk\": len(buffer),
                        \"total_tokens\": total_tokens,
                        \"elapsed_seconds\": time.time() - start_time,
                        \"timestamp\": datetime.utcnow().isoformat()
                    }
            
            else:
                # Fallback: Non-streaming response with simulated streaming
                logger.info(f"Stream {stream_id}: Using simulated streaming")
                
                response = await llm_chat.send_message(user_message)
                
                # Simulate streaming by yielding words
                words = response.split()
                for i, word in enumerate(words):
                    if not self.active_streams.get(stream_id, False):
                        break
                    
                    buffer.append(word + \" \")
                    total_tokens += 1
                    
                    if len(buffer) >= buffer_size:
                        chunk = ''.join(buffer)
                        chunk_number += 1
                        
                        yield {
                            \"type\": \"chunk\",
                            \"chunk_number\": chunk_number,
                            \"content\": chunk,
                            \"tokens_in_chunk\": len(buffer),
                            \"total_tokens\": total_tokens,
                            \"elapsed_seconds\": time.time() - start_time,
                            \"timestamp\": datetime.utcnow().isoformat()
                        }
                        
                        buffer = []
                        await asyncio.sleep(0.05)  # Simulate network delay
                
                # Final buffer
                if buffer:
                    chunk = ''.join(buffer)
                    chunk_number += 1
                    
                    yield {
                        \"type\": \"chunk\",
                        \"chunk_number\": chunk_number,
                        \"content\": chunk,
                        \"tokens_in_chunk\": len(buffer),
                        \"total_tokens\": total_tokens,
                        \"elapsed_seconds\": time.time() - start_time,
                        \"timestamp\": datetime.utcnow().isoformat()
                    }
            
            # Final metadata
            yield {
                \"type\": \"complete\",
                \"total_chunks\": chunk_number,
                \"total_tokens\": total_tokens,
                \"elapsed_seconds\": time.time() - start_time,
                \"timestamp\": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Streaming error for {stream_id}: {e}")
            yield {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        finally:
            # Clean up
            if stream_id in self.active_streams:
                del self.active_streams[stream_id]
    
    async def cancel_stream(self, stream_id: str):
        """Cancel an active stream"""
        if stream_id in self.active_streams:
            self.active_streams[stream_id] = False
            logger.info(f"Stream {stream_id} cancellation requested")
    
    def is_streaming(self, stream_id: str) -> bool:
        \"\"\"Check if stream is active\"\"\"
        return self.active_streams.get(stream_id, False)
    
    def get_active_streams(self) -> List[str]:
        \"\"\"Get list of active stream IDs\"\"\"
        return [sid for sid, active in self.active_streams.items() if active]
    
    async def stream_with_progress(
        self,
        llm_chat: LlmChat,
        user_message: UserMessage,
        stream_id: str,
        estimated_tokens: int = 500
    ) -> AsyncGenerator[Dict[str, Any], None]:
        \"\"\"
        Stream with progress estimation
        
        Yields progress percentage based on estimated token count
        \"\"\"
        
        tokens_received = 0
        
        async for chunk_data in self.stream_ai_response(llm_chat, user_message, stream_id):
            if chunk_data[\"type\"] == \"chunk\":
                tokens_received += chunk_data[\"tokens_in_chunk\"]
                progress = min(95, int((tokens_received / estimated_tokens) * 100))
                
                chunk_data[\"progress_percent\"] = progress
            
            elif chunk_data[\"type\"] == \"complete\":
                chunk_data[\"progress_percent\"] = 100
            
            yield chunk_data


# Singleton instance
streaming_handler = StreamingHandler()
