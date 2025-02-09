# AI Personal Assistant

This project is an AI-powered personal assistant that can transcribe speech, generate responses using Gemini AI, and convert text to speech using ElevenLabs. It provides real-time interaction and can assist with various tasks.

## Features
- **Voice Input:** Records user speech and processes it.
- **Speech-to-Text:** Uses Whisper for transcription.
- **AI Response:** Utilizes Google Gemini for intelligent responses.
- **Text-to-Speech:** Converts AI responses to natural-sounding speech with ElevenLabs.
- **Async Processing:** Optimized for better response time using asynchronous tasks.

## Installation

### Prerequisites
Ensure you have Python 3.8+ installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-assistant.git
   cd ai-assistant
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your API keys:
   ```plaintext
   GEMINI_API_KEY=your_google_gemini_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```

## Usage
Run the assistant:
```bash
python ai_assistant.py
```
Press the **spacebar** to stop recording.

## Technologies Used
- [Whisper](https://github.com/openai/whisper) for speech-to-text
- [Google Gemini](https://ai.google.dev/) for AI-generated responses
- [ElevenLabs](https://elevenlabs.io/) for text-to-speech
- Python (asyncio, threading, pyaudio, dotenv)

## License
This project is licensed under the MIT License.



