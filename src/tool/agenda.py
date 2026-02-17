from langchain_mcp_adapters.tools import load_mcp_tools
import logging
import os
import dotenv


async def get_agenda_tools():
    """
    Fetch and return the tools from the Agenda MCP server.
    """
    dotenv.load_dotenv()
    connection = {
        "transport": "streamable_http",
        "url": os.getenv("MCP_URL_AGENDA"),
    }

    try:
        return await load_mcp_tools(None, connection=connection)
    except Exception as e:
        print(f"Error loading Agenda MCP tools: {e}")
        return []
