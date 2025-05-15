from flow import create_voice_chat_flow

def main():
    """Runs the PocketFlow Voice Chat application."""
    print("Starting PocketFlow Voice Chat...")
    print("Speak your query after 'Listening for your query...' appears.")
    print("The conversation will continue until an error occurs or the loop is intentionally stopped.")
    print("To attempt to stop, you might need to cause an error (e.g., silence during capture if not handled by VAD to end gracefully) or modify shared[\"continue_conversation\"] if a mechanism is added.")

    shared = {
        "user_audio_data": None,
        "user_audio_sample_rate": None,
        "chat_history": [],
        "continue_conversation": True # Flag to control the main conversation loop
    }

    # Create the flow
    voice_chat_flow = create_voice_chat_flow()

    # Run the flow
    # The flow will loop based on the "next_turn" action from TextToSpeechNode
    # and the continue_conversation flag checked within nodes or if an error action is returned.
    voice_chat_flow.run(shared)

if __name__ == "__main__":
    main() 
