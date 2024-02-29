from util import pretty_print_conversation
from api import chat_completion_request, execute_function_call


def main():
    # Initialize a list to store the entire conversation history
    conversation_history = []

    # Initial system message
    conversation_history.append(
        {
            "role": "system",
            "content": "Answer user questions by generating SQL queries against the Chinook Music Database.",
        }
    )
    print(
        "system: Hi, Welcome to the Chinook Music Database! "
        "Type 'exit' to end the conversation. "
        "Type 'print history' to see the conversation history."
    )

    while True:
        # Prompt for user input
        user_input = input("user: ")

        # Check if the user wants to exit or print the conversation history
        if user_input.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break
        elif user_input.lower() == "print history":
            pretty_print_conversation(conversation_history)
            continue

        # Add user question to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Initialize messages list with the latest user message for processing
        messages = [{"role": "user", "content": user_input}]

        # Process the user question
        chat_response = chat_completion_request(messages)
        assistant_message = chat_response.choices[0].message

        if not assistant_message.tool_calls:
            response = "Sorry, I cannot understand your question. Please be more specific or try a different question."
            print(f"assistant: {response}")
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})
        else:
            assistant_message.content = str(assistant_message.tool_calls[0].function)
            # Append assistant's response to conversation history
            conversation_history.append(
                {"role": "assistant", "content": assistant_message.content}
            )

            # Execute any function calls and append the results
            if assistant_message.tool_calls:
                results = execute_function_call(assistant_message)
                conversation_history.append(
                    {
                        "role": "function",
                        "tool_call_id": assistant_message.tool_calls[0].id,
                        "name": assistant_message.tool_calls[0].function.name,
                        "content": results,
                    }
                )

            # Display only the latest exchange instead of the entire conversation history
            pretty_print_conversation(
                conversation_history[-2:]
            )  # Pass only the last two messages (assistant and function results)


if __name__ == "__main__":
    main()
