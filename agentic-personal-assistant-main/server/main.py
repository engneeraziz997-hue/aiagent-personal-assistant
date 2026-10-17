import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from agent import run_agent
from ingest import ingest_data

load_dotenv()

app = FastAPI(title="Agentic Personal Assistant Backend (Python)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = "default"

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message required")

    try:
        answer = run_agent(message=request.message, session_id=request.sessionId)
        output = answer.get("output", "") if isinstance(answer, dict) else str(answer)

        if not output or output.strip() == "":
            return {
                "answer": "I apologize, but I couldn't generate a proper response. Could you please rephrase your question?"
            }

        return {"answer": output}
    except Exception as err:
        print("❌ Error in chat endpoint:", err)
        raise HTTPException(status_code=500, detail=str(err))

@app.post("/api/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Missing PDF file")

    if not file.filename.lower().endswith(".pdf") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    suffix = os.path.splitext(file.filename)[1] or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_path = temp_file.name
        content = await file.read()
        temp_file.write(content)

    try:
        ingest_data(temp_path)
        return {"ok": True}
    except Exception as err:
        print("❌ Error in ingest endpoint:", err)
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

if __name__ == "__main__":
    import uvicorn
    print("🚀 Server running on port 3001")
    uvicorn.run(app, host="0.0.0.0", port=3001)
