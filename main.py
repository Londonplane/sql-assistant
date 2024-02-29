from util import (
    get_table_names,
    get_column_names,
    get_database_info,
    pretty_print_conversation,
)
from api import chat_completion_request, execute_function_call

messages = []
messages.append(
    {
        "role": "system",
        "content": "Answer user questions by generating SQL queries against the Chinook Music Database.",
    }
)
messages.append(
    {"role": "user", "content": "Hi, who are the top 5 artists by number of tracks?"}
)

chat_response = chat_completion_request(messages)
assistant_message = chat_response.choices[0].message
assistant_message.content = str(assistant_message.tool_calls[0].function) # sql-assistant returns a query string
messages.append({"role": assistant_message.role, "content": assistant_message.content}) # query string is added to messages
if assistant_message.tool_calls:
    results = execute_function_call(assistant_message)
    messages.append( # 结果格式化后添加到messages
        {
            "role": "function",
            "tool_call_id": assistant_message.tool_calls[0].id,
            "name": assistant_message.tool_calls[0].function.name, # 返回被调用的函数名
            "content": results,
        }
    )
pretty_print_conversation(messages)


messages.append({"role": "user", "content": "What is the name of the album with the most tracks?"})
chat_response = chat_completion_request(messages)
print(chat_response)
assistant_message = chat_response.choices[0].message
assistant_message.content = str(assistant_message.tool_calls[0].function)
messages.append({"role": assistant_message.role, "content": assistant_message.content})
if assistant_message.tool_calls:
    results = execute_function_call(assistant_message)
    messages.append({"role": "function", "tool_call_id": assistant_message.tool_calls[0].id, "name": assistant_message.tool_calls[0].function.name, "content": results})
pretty_print_conversation(messages)

