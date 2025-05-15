from anthropic import Anthropic
import os

def call_llm(prompt):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key"))
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=20000,
        thinking={
            "type": "enabled",
            "budget_tokens": 16000
        },
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[1].text

if __name__ == "__main__":
    print("## Testing call_llm")
    prompt = "In a few words, what is the meaning of life?"
    print(f"## Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"## Response: {response}")