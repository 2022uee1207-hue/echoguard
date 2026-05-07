from tts import TextToSpeech
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from llm import SimpleLLM
from stt import SpeechToText
import os
os.makedirs("../audio", exist_ok=True)

app = FastAPI()

# initialize models
llm = SimpleLLM()
stt = SpeechToText(model_size="tiny")
tts = TextToSpeech()


# greeting route
@app.get("/greeting")
async def greeting():

    return JSONResponse({
        "message": "Hello Kunal. I am EchoGuard. How was your day?"
    })


# test chat route
@app.get("/chat")
async def chat():

    response = llm.get_response("Hello")

    return JSONResponse({
        "response": response
    })


# audio upload route
@app.post("/upload")
async def upload_audio(audio: UploadFile = File(...)):

    temp_path = "temp_audio.webm"

    with open(temp_path, "wb") as f:

        content = await audio.read()

        f.write(content)

    print("Audio saved")

    # speech-to-text
    text = stt.transcribe(temp_path)

    print(f"Transcribed: {text}")

    # llm response
    ai_response = llm.get_response(text)

    print(f"AI: {ai_response}")

    # text-to-speech
    audio_path = "../audio/response.mp3"

    await tts.speak(ai_response, audio_path)

    return JSONResponse({
        "status": "success",
        "transcription": text,
        "response": ai_response,
        "audio_url": "/audio/response.mp3"
    })


# serve audio files
app.mount("/audio", StaticFiles(directory="../audio"), name="audio")

# serve frontend LAST
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")