import sounddevice as sd
import numpy as np

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 1
DEFAULT_CHUNK_SIZE_MS = 50  # Process audio in 50ms chunks for VAD
DEFAULT_SILENCE_THRESHOLD_RMS = 0.01 # RMS value, needs tuning
DEFAULT_MIN_SILENCE_DURATION_MS = 1000 # 1 second of silence to stop
DEFAULT_MAX_RECORDING_DURATION_S = 15 # Safety cap for recording
DEFAULT_PRE_ROLL_CHUNKS = 3 # Number of chunks to keep before speech starts

def record_audio(sample_rate = DEFAULT_SAMPLE_RATE,
                 channels = DEFAULT_CHANNELS,
                 chunk_size_ms = DEFAULT_CHUNK_SIZE_MS,
                 silence_threshold_rms = DEFAULT_SILENCE_THRESHOLD_RMS,
                 min_silence_duration_ms = DEFAULT_MIN_SILENCE_DURATION_MS,
                 max_recording_duration_s = DEFAULT_MAX_RECORDING_DURATION_S,
                 pre_roll_chunks_count = DEFAULT_PRE_ROLL_CHUNKS):
    """
    Records audio from the microphone with silence-based VAD.
    Returns in-memory audio data (NumPy array of float32) and sample rate.
    Returns (None, sample_rate) if recording fails or max duration is met without speech.
    """
    chunk_size_frames = int(sample_rate * chunk_size_ms / 1000)
    min_silence_chunks = int(min_silence_duration_ms / chunk_size_ms)
    max_chunks = int(max_recording_duration_s * 1000 / chunk_size_ms)

    print(f"Listening... (max {max_recording_duration_s}s). Speak when ready.")
    print(f"(Silence threshold RMS: {silence_threshold_rms}, Min silence duration: {min_silence_duration_ms}ms)")

    recorded_frames = []
    pre_roll_frames = []
    is_recording = False
    silence_counter = 0
    chunks_recorded = 0

    with sd.InputStream(samplerate=sample_rate, channels=channels, dtype='float32') as stream:

        for i in range(max_chunks):
            audio_chunk, overflowed = stream.read(chunk_size_frames)
            if overflowed:
                print("Warning: Audio buffer overflowed!")
            
            rms = np.sqrt(np.mean(audio_chunk**2))

            if is_recording:
                recorded_frames.append(audio_chunk)
                chunks_recorded += 1
                if rms < silence_threshold_rms:
                    silence_counter += 1
                    if silence_counter >= min_silence_chunks:
                        print("Silence detected, stopping recording.")
                        break
                else:
                    silence_counter = 0 # Reset silence counter on sound
            else:
                pre_roll_frames.append(audio_chunk)
                if len(pre_roll_frames) > pre_roll_chunks_count:
                    pre_roll_frames.pop(0)
                
                if rms > silence_threshold_rms:
                    print("Speech detected, starting recording.")
                    is_recording = True
                    for frame_to_add in pre_roll_frames:
                        recorded_frames.append(frame_to_add)
                    chunks_recorded = len(recorded_frames)
                    pre_roll_frames.clear()
            
            if i == max_chunks - 1 and not is_recording:
                print("No speech detected within the maximum recording duration.")
                return None, sample_rate

        if not recorded_frames and is_recording:
            print("Recording started but captured no frames before stopping. This might be due to immediate silence.")

    if not recorded_frames:
        print("No audio was recorded.")
        return None, sample_rate

    audio_data = np.concatenate(recorded_frames)
    print(f"Recording finished. Total duration: {len(audio_data)/sample_rate:.2f}s")
    return audio_data, sample_rate

def play_audio_data(audio_data, sample_rate):
    """Plays in-memory audio data (NumPy array)."""
    try:
        print(f"Playing in-memory audio data (Sample rate: {sample_rate} Hz, Duration: {len(audio_data)/sample_rate:.2f}s)")
        sd.play(audio_data, sample_rate)
        sd.wait()
        print("Playback from memory finished.")
    except Exception as e:
        print(f"Error playing in-memory audio: {e}")


if __name__ == "__main__":
    print("--- Testing audio_utils.py ---")

    # Test 1: record_audio() and play_audio_data() (in-memory)
    print("\n--- Test: Record and Play In-Memory Audio ---")
    print("Please speak into the microphone. Recording will start on sound and stop on silence.")
    recorded_audio, rec_sr = record_audio(
        sample_rate=DEFAULT_SAMPLE_RATE,
        silence_threshold_rms=0.02, 
        min_silence_duration_ms=1500,
        max_recording_duration_s=10
    )

    if recorded_audio is not None and rec_sr is not None:
        print(f"Recorded audio data shape: {recorded_audio.shape}, Sample rate: {rec_sr} Hz")
        play_audio_data(recorded_audio, rec_sr)
    else:
        print("No audio recorded or recording failed.")

    print("\n--- audio_utils.py tests finished. ---") 