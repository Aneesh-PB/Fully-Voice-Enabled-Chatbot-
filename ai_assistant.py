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


class AI_Assistant:
    def __init__(self):
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

        # Prompt
        self.full_transcript = [
            {
                "role": "system",
                "content": "You are an intelligent and helpful AI assistant. "
                "Your role is to provide clear, concise, and accurate responses to user inquiries. "
                "You should be professional, friendly, and adaptable to different situations. "
                "If a request is unclear, ask for clarification. "
                "If you don’t know something, respond honestly rather than making assumptions.",
            },
        ]

    def record_audio(self):
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

    def transcribe_audio(self, audio_data):
        print("Transcribing...")
        result = whisper_model.transcribe(audio_data)
        transcript = result["text"].strip()
        print(f"\nPatient: {transcript}", end="\r\n")
        return transcript

    async def generate_ai_response(self, transcript):
        self.full_transcript.append({"role": "user", "content": transcript})

        response = await asyncio.to_thread(
            self.gemini_client.models.generate_content,
            model="gemini-1.5-flash",
            contents=transcript,
        )

        ai_response = response.text
        await self.generate_audio(ai_response)

    async def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist: {text}")

        audio_stream = await asyncio.to_thread(
            self.elevenlabs_client.text_to_speech.convert_as_stream,
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_flash_v2",
        )

        stream(audio_stream)

    async def run(self):
        greeting = "Hello My name is Jarvis, how may I assist you?"
        await self.generate_audio(greeting)

        while True:
            audio_data = self.record_audio()  # Get raw audio instead of a file
            transcript = self.transcribe_audio(audio_data)
            await self.generate_ai_response(transcript)


if __name__ == "__main__":
    ai_assistant = AI_Assistant()
    asyncio.run(ai_assistant.run())
