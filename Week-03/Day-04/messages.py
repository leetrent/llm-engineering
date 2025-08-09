messages = [
    {"role": "system", "content": "You are a helpful assistant"}
  ]

def append_user_message(user_message):
    messages.append({"role": "user", "content": user_message})
         
def get_messages():
  return messages