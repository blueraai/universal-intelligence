# Structured Output Demo

A minimal demo application showing how to use PocketFlow to extract structured data from a resume using direct prompting and YAML formatting. Why YAML? Check out the [doc](https://the-pocket.github.io/PocketFlow/design_pattern/structure.html).

This implementation is based on: [Structured Output for Beginners: 3 Must-Know Prompting Tips](https://zacharyhuang.substack.com/p/structured-output-for-beginners-3).

## Features

- Extracts structured data using prompt engineering
- Validates output structure before processing

## Run It

1. Install the packages you need with this simple command:
    ```bash
    pip install -r requirements.txt
    ```

2. Make sure your OpenAI API key is set:
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```
    Alternatively, you can edit the [`utils.py`](./utils.py) file to include your API key directly.

    Let's do a quick check to make sure your API key is working properly:

    ```bash
    python utils.py
    ```

3. Edit [data.txt](./data.txt) with the resume you want to parse (a sample resume is already included)

4. Run the application:
    ```bash
    python main.py
    ```

## How It Works

```mermaid
flowchart LR
    parser[ResumeParserNode]
```

The Resume Parser application uses a single node that:
1. Takes resume text from the shared state (loaded from data.txt)
2. Sends the resume to an LLM with a prompt that requests YAML formatted output
3. Extracts and validates the structured YAML data
4. Outputs the structured result

## Files

- [`main.py`](./main.py): Implementation of the ResumeParserNode
- [`utils.py`](./utils.py): LLM utilities
- [`data.txt`](./data.txt): Sample resume text file
 
## Example Output

```
=== Resume Parser - Structured Output with Indexes & Comments ===


=== STRUCTURED RESUME DATA (Comments & Skill Index List) ===

name: JOHN SMTIH
email: johnsmtih1983@gnail.com
experience:
- {title: SALES MANAGER, company: ABC Corportaion}
- {title: ASST. MANAGER, company: XYZ Industries}
- {title: CUSTOMER SERVICE REPRESENTATIVE, company: Fast Solutions Inc}
skill_indexes: [0, 1, 2, 3, 4]


============================================================

✅ Extracted resume information.

--- Found Target Skills (from Indexes) ---
- Team leadership & management (Index: 0)
- CRM software (Index: 1)
- Project management (Index: 2)
- Public speaking (Index: 3)
- Microsoft Office (Index: 4)
----------------------------------------
```
