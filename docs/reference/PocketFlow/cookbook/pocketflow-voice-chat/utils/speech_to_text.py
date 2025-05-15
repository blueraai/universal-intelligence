import os
from openai import OpenAI
import io

def speech_to_text_api(audio_data: bytes, sample_rate: int):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # The API expects a file-like object. We can use io.BytesIO for in-memory bytes.
    # We also need to give it a name, as if it were a file upload.
    audio_file = io.BytesIO(audio_data)
    audio_file.name = "audio.wav"  # Corrected to WAV format

    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=audio_file
        # language="en" # Optional: specify language ISO-639-1 code
        # prompt="PocketFlow, LLM" # Optional: provide a prompt to guide the model
    )
    return transcript.text

if __name__ == "__main__":
    print("Testing Speech-to-Text API...")
    # The OpenAI client will raise an error if API key is not found or invalid.
    # No explicit check here to keep it minimal.
    test_audio_path = "tts_output.mp3"
    if os.path.exists(test_audio_path):
        print(f"Found {test_audio_path}, using it for STT test.")
        with open(test_audio_path, "rb") as f:
            audio_bytes_for_stt = f.read()
        
        # Sample rate for tts_output.mp3 from our TTS script is 24000
        # but Whisper should ideally infer or handle common formats well.
        stt_sample_rate = 24000 

        transcribed_text = speech_to_text_api(audio_bytes_for_stt, stt_sample_rate)

        if transcribed_text:
            print(f"Transcribed text: {transcribed_text}")
        else:
            print("Failed to transcribe audio (API returned empty data).")
    else:
        print(f"Test audio file '{test_audio_path}' not found.")
        print("Please run the text_to_speech.py test first to generate it, or place your own audio file")
        print(" (e.g., named 'test_audio.mp3') in the same directory as this script and modify the path.")
        print("Make sure it's a common audio format like MP3, WAV, M4A etc.") 