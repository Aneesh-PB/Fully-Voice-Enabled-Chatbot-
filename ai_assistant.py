import os
import asyncio
import pyaudio
import keyboard
import numpy as np
import whisper
from google import genai
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

# Load Whisper model (small for speed, change to 'base' or 'medium' for better accuracy)
whisper_model = whisper.load_model("small")

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

full_transcript = [
    {
        "role": "system",
        "content": "You are an intelligent and helpful AI assistant. "
        "Your role is to provide clear, concise, and accurate responses to user inquiries. "
        "You should be professional, friendly, and adaptable to different situations. "
        "If a request is unclear, ask for clarification. "
        "If you don’t know something, respond honestly rather than making assumptions.",
    },
]


def record_audio():
    chunk = 1024
    sample_format = pyaudio.paInt16  # 16-bit PCM
    channels = 1
    fs = 16000  # 16kHz sample rate
    p = pyaudio.PyAudio()

    print("Recording... Press 'space' to stop.")
    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        input=True,
        frames_per_buffer=chunk,
    )

    frames = []

    while True:
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)
        if keyboard.is_pressed("space"):
            print("Stopping recording...")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert raw PCM data to a NumPy array for processing
    audio_data = (
        np.frombuffer(b"".join(frames), dtype=np.int16).astype(np.float32) / 32768.0
    )

    return audio_data


def transcribe_audio(audio_data):
    print("Transcribing...")
    result = whisper_model.transcribe(
        audio_data
    )  # We can also use AssumblyAI API here which supports Real-time transcription
    transcript = result["text"].strip()
    print(f"\nUser: {transcript}")
    return transcript


async def generate_ai_response(transcript):
    full_transcript.append({"role": "user", "content": transcript})

    response = await asyncio.to_thread(
        gemini_client.models.generate_content,
        model="gemini-1.5-flash",
        contents=transcript,
    )

    ai_response = response.text
    await generate_audio(ai_response)


async def generate_audio(text):
    full_transcript.append({"role": "assistant", "content": text})
    print(f"\nAI Assistant: {text}")

    audio_stream = await asyncio.to_thread(
        elevenlabs_client.text_to_speech.convert_as_stream,
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_flash_v2",
    )

    stream(audio_stream)


async def main():
    greeting = "Hello, my name is Jarvis. How may I assist you?"
    await generate_audio(greeting)

    while True:
        audio_data = record_audio()
        transcript = transcribe_audio(audio_data)
        await generate_ai_response(transcript)


if __name__ == "__main__":
    asyncio.run(main())
