from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/generate/")
async def generate_code(websocket: WebSocket):
    await websocket.accept()
    try:
        # Receive prompt from the client
        prompt = await websocket.receive_text()

        # Run Ollama and stream output
        process = subprocess.Popen(
            ["ollama", "run", "deepseek-coder", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Stream output to the client
        for line in iter(process.stdout.readline, ""):
            await websocket.send_text(line)
        process.stdout.close()
        process.wait()

    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()