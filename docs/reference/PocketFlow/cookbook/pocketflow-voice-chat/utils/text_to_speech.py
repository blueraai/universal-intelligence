import os
from openai import OpenAI

def text_to_speech_api(text_to_synthesize: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy", # Other voices: echo, fable, onyx, nova, shimmer
        input=text_to_synthesize,
        response_format="mp3" # Other formats: opus, aac, flac. MP3 is widely supported.
                              # OpenAI default sample rate for tts-1 is 24kHz.
    )
    # The response.content is already bytes (the audio data)
    # Alternatively, for streaming and saving to file: response.stream_to_file("output.mp3")
    audio_data_bytes = response.content
    sample_rate = 24000 # OpenAI TTS model tts-1 outputs 24kHz
    return audio_data_bytes, sample_rate

if __name__ == "__main__":
    print("Testing Text-to-Speech API...")
    # The OpenAI client will raise an error if API key is not found or invalid.
    # No explicit check here to keep it minimal.
    text = "Hello from PocketFlow! This is a test of the text-to-speech functionality."
    audio_bytes, rate = text_to_speech_api(text)
    if audio_bytes and rate:
        print(f"Successfully converted text to speech. Audio data length: {len(audio_bytes)} bytes, Sample rate: {rate} Hz.")
        with open('tts_output.mp3', 'wb') as f:
            f.write(audio_bytes)
        print("Saved TTS output to tts_output.mp3")
    else: 
        print("Failed to convert text to speech (API returned empty data).")