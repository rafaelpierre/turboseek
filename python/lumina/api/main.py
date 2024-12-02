from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, AsyncGenerator
import asyncio

# Define the payload structure
class Message(BaseModel):
    role: str
    content: str | List[str]

class InferPayload(BaseModel):
    model: str
    messages: List[Message]
    stream: bool

app = FastAPI()


# Async generator to simulate streaming
async def mock_streaming_response(messages: List[Message]) -> AsyncGenerator[str, None]:
    for i, message in enumerate(messages):
        # Simulate processing each message
        yield f"Chunk {i + 1}: Response to '{message.content}'\n"
        await asyncio.sleep(1)  # Simulate delay

@app.post("/infer")
async def root(payload: InferPayload):
   # Log received data
    try:
        print(f"Received payload: {payload}")
        
        # Extract relevant data
        model = payload.model
        messages = payload.messages
        stream = payload.stream
        
        if stream:
            # Return a streaming response
            return StreamingResponse(
                mock_streaming_response(messages),
                media_type="text/plain",
                status_code = 202
            )
        else:
            # Return a full response
            response_content = f"Full response for model: {model}, messages: {messages}"
            return {"model": model, "stream": False, "response": response_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))