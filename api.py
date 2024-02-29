from openai import OpenAI

client = OpenAI()
from util import conn, database_schema_string
import json

tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_database",
            "description": "Use this function to answer user questions about music. Input should be a fully formed SQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                                SQL query extracting info to answer the user's question.
                                SQL should be written using this database schema:
                                {database_schema_string}
                                The query should be returned in plain text, not in JSON.
                                """,
                    }
                },
                "required": ["query"],
            },
        },
    }
]


def chat_completion_request(messages):
    """Function to send a chat completion request to the OpenAI API."""
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
    )
    return completion


def ask_database(conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(conn.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error: {e}"
    return results


def execute_function_call(message):
    """提取query并调用ask_database函数执行查询，返回查询结果。"""
    if message.tool_calls[0].function.name == "ask_database":
        query = json.loads(message.tool_calls[0].function.arguments)["query"]
        results = ask_database(conn, query)
    else:
        results = (
            f"Error: function {message.tool_calls[0].function.name} does not exist"
        )
    return results
