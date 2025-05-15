from pocketflow import Flow
from nodes import CaptureAudioNode, SpeechToTextNode, QueryLLMNode, TextToSpeechNode

def create_voice_chat_flow() -> Flow:
    """Creates and returns the voice chat flow."""
    # Create nodes
    capture_audio = CaptureAudioNode()
    speech_to_text = SpeechToTextNode()
    query_llm = QueryLLMNode()
    text_to_speech = TextToSpeechNode()

    # Define transitions
    capture_audio >> speech_to_text
    speech_to_text >> query_llm
    query_llm >> text_to_speech

    # Loop back for next turn or end
    text_to_speech - "next_turn" >> capture_audio
    # "end_conversation" action from any node will terminate the flow naturally
    # if no transition is defined for it from the current node.
    # Alternatively, one could explicitly transition to an EndNode if desired.

    # Create flow starting with the capture audio node
    voice_chat_flow = Flow(start=capture_audio)
    return voice_chat_flow 