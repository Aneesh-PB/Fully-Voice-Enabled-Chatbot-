# AI Assistant - Voice-Powered Receptionist

## Overview
This AI Assistant acts as a receptionist using voice input and AI-generated responses. It records audio, transcribes it using OpenAI Whisper, processes the text with Google Gemini, and generates speech responses using ElevenLabs.

## Features
- **Voice Recognition**: Uses OpenAI Whisper for transcription.
- **AI Response Generation**: Utilizes Google Gemini for intelligent responses.
- **Text-to-Speech**: Converts AI-generated text into speech with ElevenLabs.
- **Async Processing**: Uses `asyncio` to optimize performance.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/ai-assistant.git
cd ai-assistant
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add your API keys:
```
GEMINI_API_KEY=your_google_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Usage
Run the assistant with:
```bash
python ai_assistant.py
```
The assistant will start listening. Press the `space` key to stop recording.

## Dependencies
- `pyaudio` (for recording audio)
- `whisper` (for speech-to-text transcription)
- `google-generativeai` (for AI response generation)
- `elevenlabs` (for text-to-speech synthesis)
- `keyboard` (for stopping recording with a keypress)

## License
This project is open-source. Feel free to modify and enhance it!

