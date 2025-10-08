import io
import openai
from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

audio_buffers = {}

@socketio.on('connect', namespace='/ws/meeting-audio')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect', namespace='/ws/meeting-audio')
def handle_disconnect():
    sid = request.sid
    if sid in audio_buffers:
        del audio_buffers[sid]
    print("Client disconnected")

@socketio.on('message', namespace='/ws/meeting-audio')
def handle_audio_chunk(audio_chunk):
    sid = request.sid
    # Buffer the audio data
    if sid not in audio_buffers:
        audio_buffers[sid] = b''
    audio_buffers[sid] += audio_chunk

    # For demo: every ~5 seconds or if buffer > threshold, transcribe and analyze
    if len(audio_buffers[sid]) > 16000 * 2 * 5:  # 5 seconds of 16kHz 16-bit mono
        audio_data = audio_buffers[sid]
        audio_buffers[sid] = b''
        # Transcribe with OpenAI Whisper API
        transcription = transcribe_audio_openai(audio_data)
        emit('message', {'type': 'transcription', 'text': transcription})
        # Analyze with ChatGPT
        insight = analyze_with_gpt(transcription)
        emit('message', {'type': 'insight', 'insight': insight})

def transcribe_audio_openai(audio_bytes):
    # OpenAI Whisper API expects a file-like object
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    audio_file.seek(0)
    try:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcript
    except Exception as e:
        print(f"Whisper API error: {e}")
        return ""

def analyze_with_gpt(text):
    if not text.strip():
        return ""
    prompt = f"Analyze the following meeting transcript and provide a single actionable insight:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
