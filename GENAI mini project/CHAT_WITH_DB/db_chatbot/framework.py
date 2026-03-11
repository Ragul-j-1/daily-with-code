from langchain_ollama import ChatOllama
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
import os

from client import run_query_sync, run_list_tables_sync, run_list_databases_sync

class DatabaseChatbot:
    def __init__(self, db_directory: str, model_name: str = "gpt-oss:120b-cloud"):
        self.db_directory = os.path.abspath(db_directory)
        self.history_db = f"sqlite:///{os.path.join(self.db_directory, 'chat_history.db')}"
        
        # LLM setup
        self.llm = ChatOllama(
            model=model_name,
            base_url="http://localhost:11434"
        )
        
        # Discover databases and tables to build a dynamic prompt
        raw_databases = run_list_databases_sync(self.db_directory)
        
        # Correctly extract strings from MCP content objects
        self.databases = []
        if isinstance(raw_databases, list):
            for content in raw_databases:
                if hasattr(content, 'text'):
                    self.databases.append(content.text)
                else:
                    self.databases.append(str(content))

        self.schema_info = {}
        
        for db in self.databases:
            tables = run_list_tables_sync(db, self.db_directory)
            # Ensure tables is a list of dicts by extracting from MCP content if needed
            processed_tables = []
            if isinstance(tables, list):
                for t in tables:
                    if hasattr(t, 'text'):
                        import json
                        try:
                            processed_tables.append(json.loads(t.text))
                        except:
                            processed_tables.append(t.text)
                    else:
                        processed_tables.append(t)
            self.schema_info[db] = processed_tables
        
        self.system_prompt = self._build_system_prompt()
        self.agent = create_react_agent(self.llm, self._get_tools(), prompt=self.system_prompt)

    def _build_system_prompt(self) -> str:
        prompt = (
            "You are a helpful database assistant. You have access to a directory of SQLite databases. "
            "Use the tools provided to query the databases and answer user questions accurately. "
            "Always use ListTablesTool if you are unsure about the structure of a database.\n\n"
            f"Available Databases in this folder: {', '.join(self.databases) if isinstance(self.databases, list) else 'No databases found'}\n"
        )
        
        if self.schema_info:
            prompt += "\nImmediate Schema Knowledge:\n"
            for db, tables in self.schema_info.items():
                prompt += f"- Database: {db}\n"
                if isinstance(tables, list):
                    for table_info in tables:
                        if isinstance(table_info, dict):
                            prompt += f"  * Table: {table_info.get('table')} (Columns: {', '.join(table_info.get('columns', []))})\n"
        
        prompt += "\nInstructions:\n1. Use DatabaseTool to run SQL SELECT queries. You MUST specify the database_name and the query.\n"
        prompt += "2. Only run SELECT queries. Do not attempt to modify the data.\n"
        return prompt

    def _get_tools(self):
        def sql_tool(database_name: str, query: str) -> str:
            """Execute a SQL SELECT query on a specific database.
            Args:
                database_name: The name of the .db file (e.g., 'my_data.db').
                query: The SQL SELECT query to run.
            """
            result = run_query_sync(database_name, query, self.db_directory)
            return str(result)

        def list_tables_tool(database_name: str) -> str:
            """List all tables and their columns in a specific database.
            Args:
                database_name: The name of the .db file.
            """
            result = run_list_tables_sync(database_name, self.db_directory)
            return str(result)

        return [
            Tool(name="ListTablesTool", func=list_tables_tool, description=list_tables_tool.__doc__),
            Tool(name="DatabaseTool", func=sql_tool, description=sql_tool.__doc__)
        ]

    def get_history(self, session_id: str):
        return SQLChatMessageHistory(
            session_id=session_id,
            connection=self.history_db
        )

    def chat(self, user_query: str, session_id: str) -> str:
        history = self.get_history(session_id)

        # Build message list from history + new question
        messages = []
        for msg in history.messages:
            messages.append(msg)
        messages.append(HumanMessage(content=user_query))

        result = self.agent.invoke({"messages": messages})

        # Get the last AI message as the response
        ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
        response = ai_messages[-1].content if ai_messages else "Sorry, I could not process that."

        # Save to history
        history.add_user_message(user_query)
        history.add_ai_message(response)

        return response
