import os
import asyncio
from anthropic import AsyncAnthropic

# Async version of the simple wrapper, using Anthropic
async def call_llm(prompt):
    """Async wrapper for Anthropic API call."""
    client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key"))
    response = await client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=20000,
        thinking={
            "type": "enabled",
            "budget_tokens": 16000
        },
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.content[1].text

if __name__ == "__main__":
    async def run_test():
        print("## Testing async call_llm with Anthropic")
        prompt = "In a few words, what is the meaning of life?"
        print(f"## Prompt: {prompt}")
        response = await call_llm(prompt)
        print(f"## Response: {response}")

    asyncio.run(run_test()) 