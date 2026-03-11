import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import os

def _server_params(db_directory: str = "."):
    # Use absolute path for server.py to avoid any ambiguity
    server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mcp", "server.py"))
    
    # Merge environment variables to include the database directory
    env = os.environ.copy()
    env["DB_DIRECTORY"] = os.path.abspath(db_directory)
    
    return StdioServerParameters(
        command="python",
        args=[server_path],
        env=env
    )

async def _call_mcp_tool(tool_name, arguments, db_directory: str = "."):
    """Generic helper to call MCP tools with a timeout to prevent hangs."""
    try:
        async with stdio_client(_server_params(db_directory)) as (read, write):
            async with ClientSession(read, write) as session:
                # Use a timeout for initialization
                await asyncio.wait_for(session.initialize(), timeout=10.0)
                
                # Use a timeout for the tool call
                result = await asyncio.wait_for(
                    session.call_tool(tool_name, arguments), 
                    timeout=15.0
                )
                return result.content
    except asyncio.TimeoutError:
        return f"Error: MCP session timed out while calling {tool_name}"
    except Exception as e:
        return f"Error: {str(e)}"

async def run_query(database_name, query, db_directory):
    return await _call_mcp_tool("run_sql", {"database_name": database_name, "query": query}, db_directory)

async def run_list_tables(database_name, db_directory):
    return await _call_mcp_tool("list_tables", {"database_name": database_name}, db_directory)

async def run_list_databases(db_directory):
    return await _call_mcp_tool("list_databases", {}, db_directory)

def run_query_sync(database_name, query, db_directory):
    try:
        return asyncio.run(run_query(database_name, query, db_directory))
    except Exception as e:
        return f"Sync Error: {str(e)}"

def run_list_tables_sync(database_name, db_directory):
    try:
        return asyncio.run(run_list_tables(database_name, db_directory))
    except Exception as e:
        return f"Sync Error: {str(e)}"

def run_list_databases_sync(db_directory):
    try:
        return asyncio.run(run_list_databases(db_directory))
    except Exception as e:
        return f"Sync Error: {str(e)}"