from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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

@app.get("/generate/")  # Change to GET
async def generate_code(prompt: str):  # Accept prompt as a query parameter
    try:
        # Run Ollama and stream output
        process = subprocess.Popen(
            ["ollama", "run", "deepseek-coder", prompt],  # Use prompt directly
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        async def stream_output():
            for line in iter(process.stdout.readline, ""):
                yield f"data: {line}\n\n"
            process.stdout.close()
            process.wait()

        return StreamingResponse(stream_output(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))