import asyncio
from universal_intelligence.community.tools.mcp_client.tool import UniversalTool

async def test_time_server():
    # Configure the MCP client to connect to our time server
    mcp_client = UniversalTool({
        "server_command": "python",
        "server_args": ["time_server.py"]
    })

    try:
        # List available tools
        tools, status = await mcp_client.list_tools()
        print("Available tools:", tools)
        
        # Get the current time
        print("\nCalling get_current_time...")
        time_result, time_status = await mcp_client.call_tool("get_current_time")
        print(f"Current time: {time_result}")
        
        # Get the current date
        print("\nCalling get_current_date...")
        date_result, date_status = await mcp_client.call_tool("get_current_date")
        print(f"Current date: {date_result}")
        
        # Get the timestamp
        print("\nCalling get_timestamp...")
        timestamp_result, timestamp_status = await mcp_client.call_tool("get_timestamp")
        print(f"Current timestamp: {timestamp_result}")
        
    finally:
        # Clean up
        if mcp_client._session:
            await mcp_client._session.close()

if __name__ == "__main__":
    asyncio.run(test_time_server())