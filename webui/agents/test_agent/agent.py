
# Sample agent implementation for the webui
from universal_intelligence import Agent, Tool, Model

# Create a simple model with default configuration
model = Model()

# Create a custom tool class
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

# Create the search tool
search_tool = SearchTool()

# Create the agent with the search tool
agent = Agent(
    universal_model=model,
    expand_tools=[search_tool],
)

# Export the agent for discovery
root_agent = agent
