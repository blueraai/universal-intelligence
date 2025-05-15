from fastmcp import FastMCP
import datetime

# Create a named server
mcp = FastMCP("Time Server")

# Define time-related tools
@mcp.tool()
def get_current_time() -> str:
    """Get the current time in ISO format"""
    return datetime.datetime.now().isoformat()

@mcp.tool()
def get_current_date() -> str:
    """Get the current date in YYYY-MM-DD format"""
    return datetime.date.today().isoformat()

@mcp.tool()
def get_timestamp() -> int:
    """Get the current timestamp as seconds since epoch"""
    return int(datetime.datetime.now().timestamp())

# Start the server
if __name__ == "__main__":
    mcp.run()