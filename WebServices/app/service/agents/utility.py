class Function:
    def __init__(self, arguments, name):
        self.arguments = arguments
        self.name = name

class ChatCompletionsMessageToolCall:
    def __init__(self, id, function, type):
        self.id = id
        self.function = function
        self.type = type

class ChatCompletionMessage:
    def __init__(self, content, role, function_call, tool_calls):
        self.content = content
        self.role = role
        self.function_call = function_call
        self.tool_calls = tool_calls

def chat_completion_message_to_dict(chat_completion_message):
    return {
        "content": chat_completion_message.content,
        "role": chat_completion_message.role,
        "function_call": chat_completion_message.function_call,
        "tool_calls": [
            {
                "id": tc.id,
                "function": {
                    "arguments": tc.function.arguments,
                    "name": tc.function.name
                },
                "type": tc.type
            } for tc in chat_completion_message.tool_calls
        ]
    }