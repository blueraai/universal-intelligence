
# Sample agent implementation for the webui
from universal_intelligence import Agent, Tool, Model

# Create a model with default configuration
model = Model()

# Create custom tool classes
class SearchTool(Tool):
    def __init__(self, configuration=None):
        super().__init__(configuration)
    
    def search(self, query: str) -> tuple[str, dict]:
        """Search for information on the web.
        
        Args:
            query: The search query
            
        Returns:
            Search results as text
        """
        # This is a mock implementation
        result = f"Search results for: {query}"
        return result, {"status": "success"}


class SimplePrinter(Tool):
    def __init__(self, configuration=None):
        super().__init__(configuration)
    
    def print_text(self, text: str) -> tuple[str, dict]:
        """Prints a given text to the console.
        
        Args:
            text: Text to be printed
            
        Returns:
            The printed text and operation status
        """
        # Print to console
        print("\n\n")
        print(text)
        print("\n\n")
        return text, {"status": "success"}


class PythonCodeHelper(Tool):
    def __init__(self, configuration=None):
        super().__init__(configuration)
    
    def generate_python_code(self, task_description: str) -> tuple[str, dict]:
        """Generates Python code based on a task description.
        
        Args:
            task_description: Description of what the code should do
            
        Returns:
            Generated Python code and metadata
        """
        # This would typically call a specialized model or service
        # For demo purposes, we'll return some example code based on the task
        
        if "hello" in task_description.lower():
            code = """def greet(name):\n    return f\"Hello, {name}!\"\n\nif __name__ == \"__main__\":\n    name = input(\"Enter your name: \")\n    print(greet(name))"""
        elif "file" in task_description.lower():
            code = """def write_to_file(filename, content):\n    with open(filename, 'w') as f:\n        f.write(content)\n    print(f\"Content written to {filename}\")\n\nif __name__ == \"__main__\":\n    filename = input(\"Enter filename: \")\n    content = input(\"Enter content: \")\n    write_to_file(filename, content)"""
        elif "web" in task_description.lower() or "http" in task_description.lower():
            code = """import requests\n\ndef fetch_url(url):\n    response = requests.get(url)\n    return response.text\n\nif __name__ == \"__main__\":\n    url = input(\"Enter URL: \")\n    content = fetch_url(url)\n    print(f\"Content length: {len(content)} characters\")\n    print(content[:500] + \"...\" if len(content) > 500 else content)"""
        else:
            code = """def main():\n    print(\"This is a sample Python program\")\n    print(\"You can customize this based on your needs\")\n    data = [1, 2, 3, 4, 5]\n    print(f\"Sum of data: {sum(data)}\")\n    print(f\"Average of data: {sum(data)/len(data)}\")\n\nif __name__ == \"__main__\":\n    main()"""
        
        return code, {"language": "python", "status": "success"}

# Create the tools
search_tool = SearchTool()
printer_tool = SimplePrinter()
python_tool = PythonCodeHelper()

# Create the agent with all tools
agent = Agent(
    universal_model=model,
    expand_tools=[search_tool, printer_tool, python_tool],
)

# Export the agent for discovery
root_agent = agent
