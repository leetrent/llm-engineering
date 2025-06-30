import os
from dotenv import load_dotenv
from openai import OpenAI
from airline_tools import AirlineTools

class ChatGPT:
    def __init__(self, sys_msg, msg_hist, curr_msg):
        self.model = "gpt-4o-mini"
        self.system_message = sys_msg
        self.message_history = msg_hist
        self.current_message = curr_msg
        self.all_messages = self._prepare_all_messages()
        
        # print("\nChatGPT (system_message)")
        # print(self.system_message)
        # print("\nChatGPT (message_history)")
        # print(self.message_history)
        # print("\nChatGPT (current_message)")
        # print(self.current_message)  
        # print("\nChatGPT (all_messages)")
        # print(self.all_messages)  

    def _get_api_key(self):
        load_dotenv(override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ No API key found in .env for ChatGPT.")
        return api_key
    
    def stream_response(self):
        try:
            openai_client = OpenAI(api_key=self._get_api_key())
            stream = openai_client.chat.completions.create(
                model=self.model,
                messages=self.all_messages,
                stream=True
            )
            result = ""
            for chunk in stream:
                result += chunk.choices[0].delta.content or ""
                yield result
        except Exception as e:
            raise RuntimeError(f"API call to ChatGPT failed: {e}")
        
    def generate_text_response(self):
        airline_tools = AirlineTools()
        openai_client = OpenAI(api_key=self._get_api_key())
        response = openai_client.chat.completions.create(model=self.model, messages=self.all_messages, tools=airline_tools.price_function_tool)
        
        if response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            response, city = airline_tools.handle_price_function_tool_call(message)
            self.all_messages.append(message)
            self.all_messages.append(response)
            response = openai_client.chat.completions.create(model=self.model, messages=self.all_messages)
    
        return response.choices[0].message.content
        
    def _prepare_all_messages(self):
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in [{"role": "system", "content": self.system_message}] + self.message_history + [{"role": "user", "content": self.current_message}]
        ]