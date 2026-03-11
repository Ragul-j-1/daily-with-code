import sqlite3
import os
import glob
from mcp.server.fastmcp import FastMCP

# Setup logging to a file since stdout is used for MCP
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.log")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(str(msg) + "\n")

# Use a global FastMCP instance
mcp = FastMCP('generic_database_server')

# Directory containing the databases, passed via environment variable
DB_DIRECTORY = os.environ.get("DB_DIRECTORY", ".")

def get_db_path(db_name: str) -> str:
    """Safely construct the path to a database within the DB_DIRECTORY."""
    # Prevent path traversal
    if ".." in db_name or db_name.startswith("/") or db_name.startswith("\\"):
        raise ValueError("Invalid database name")
    return os.path.join(DB_DIRECTORY, db_name)

@mcp.tool()
def list_databases() -> list:
    """List all SQLite databases (.db or .sqlite files) in the configured directory."""
    log(f"Tool called: list_databases in {DB_DIRECTORY}")
    try:
        db_files = glob.glob(os.path.join(DB_DIRECTORY, "*.db")) + glob.glob(os.path.join(DB_DIRECTORY, "*.sqlite"))
        return [os.path.basename(f) for f in db_files]
    except Exception as e:
        log(f"Error in list_databases: {e}")
        return [{"error": str(e)}]

@mcp.tool()
def list_tables(database_name: str) -> list:
    """List all tables available in the specified database along with their column names."""
    log(f"Tool called: list_tables for {database_name}")
    try:
        db_path = get_db_path(database_name)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        tables = [row[0] for row in cur.fetchall()]

        result = []
        for table in tables:
            cur.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cur.fetchall()]
            result.append({"table": table, "columns": columns})

        conn.close()
        log(f"Result for {database_name}: {result}")
        return result
    except Exception as e:
        log(f"Error in list_tables for {database_name}: {e}")
        return [{"error": str(e)}]

@mcp.tool()
def run_sql(database_name: str, query: str):
    """Execute a DQL (SELECT) query on the specified database."""
    log(f"Tool called: run_sql on {database_name} with query: {query}")
    try:
        # Security: only allow SELECT
        if not query.strip().upper().startswith("SELECT"):
            return "Error: Only SELECT queries are allowed."
            
        db_path = get_db_path(database_name)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        log(f"Result count: {len(result)}")
        return result
    except Exception as e:
        log(f"Error in run_sql on {database_name}: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    log(f"Server starting via mcp.run() with DB_DIRECTORY={DB_DIRECTORY}")
    mcp.run()
