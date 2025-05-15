# Parallel Batch Translation Process

This project demonstrates using PocketFlow's async and parallel features (`AsyncFlow`, `AsyncParallelBatchNode`) to translate a document into multiple languages concurrently.

- Check out the [Substack Post Tutorial](https://pocketflow.substack.com/p/parallel-llm-calls-from-scratch-tutorial) for more!

## Goal

Translate `../../README.md` into multiple languages (Chinese, Spanish, etc.) in parallel, saving each to a file in the `translations/` directory. The main goal is to compare execution time against a sequential process.

## Getting Started

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Set API Key:
   Set the environment variable for your Anthropic API key.
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```
   *(Replace `"your-api-key-here"` with your actual key)*
   *(Alternatively, place `ANTHROPIC_API_KEY=your-api-key-here` in a `.env` file)*

3. Verify API Key (Optional):
   Run a quick check using the utility script.
   ```bash
   python utils.py
   ```
   *(Note: This requires a valid API key to be set.)*

4. Run the translation process:
   ```bash
   python main.py
   ```

## How It Works

The implementation uses an `AsyncParallelBatchNode` that processes translation requests concurrently. The `TranslateTextNodeParallel`:

1. Prepares batches, pairing the source text with each target language.

2. Executes translation calls to the LLM for all languages concurrently using `async` operations.

3. Saves the translated content to individual files (`translations/README_LANGUAGE.md`).

This approach leverages `asyncio` and parallel execution to speed up I/O-bound tasks like multiple API calls.

## Example Output & Comparison

Running this parallel version significantly reduces the total time compared to a sequential approach:

```
# --- Sequential Run Output (from pocketflow-batch) ---
Starting sequential translation into 8 languages...
Translated Chinese text
...
Translated Korean text
Saved translation to translations/README_CHINESE.md
...
Saved translation to translations/README_KOREAN.md

Total sequential translation time: ~1136 seconds

=== Translation Complete ===
Translations saved to: translations
============================


# --- Parallel Run Output (this example) ---
Starting parallel translation into 8 languages...
Translated French text
Translated Portuguese text
... # Messages may appear interleaved
Translated Spanish text
Saved translation to translations/README_CHINESE.md
...
Saved translation to translations/README_KOREAN.md

Total parallel translation time: ~209 seconds

=== Translation Complete ===
Translations saved to: translations
============================
```
*(Actual times will vary based on API response speed and system.)*

## Files

- [`main.py`](./main.py): Implements the parallel batch translation node and flow.
- [`utils.py`](./utils.py): Async wrapper for calling the Anthropic model.
- [`requirements.txt`](./requirements.txt): Project dependencies (includes `aiofiles`).
- [`translations/`](./translations/): Output directory (created automatically). 
