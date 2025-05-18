from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import json
import os
import openai
from dotenv import load_dotenv
import base64
import ffmpeg

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Serve static files
current_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(current_dir, "static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(static_dir, "index.html"))

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class TranslationManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def process_audio(self, audio_data: bytes, source_lang: str, target_lang: str):
        try:
            # Convert audio to required format (16kHz, mono, PCM16)
            process = (
                ffmpeg
                .input('pipe:0')
                .output('pipe:1', acodec='pcm_s16le', ac=1, ar='16k')
                .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
            )
            
            output_data, _ = process.communicate(input=audio_data)

            # Call OpenAI Whisper API for transcription
            response = await openai.Audio.atranscribe(
                "whisper-1",
                output_data,
                language=source_lang if source_lang != "auto" else None
            )

            # Get the transcription
            transcription = response["text"]

            # Call OpenAI API for translation
            translation_response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a translator. Translate the following text to " + target_lang},
                    {"role": "user", "content": transcription}
                ]
            )

            translation = translation_response.choices[0].message.content

            return {
                "original": transcription,
                "translated": translation,
                "detected_language": source_lang
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

manager = TranslationManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "audio":
                audio_data = base64.b64decode(data["data"])
                source_lang = data.get("source_lang", "auto")
                target_lang = data.get("target_lang", "en")
                
                result = await manager.process_audio(audio_data, source_lang, target_lang)
                await websocket.send_json(result)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(client_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
