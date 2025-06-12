from chatgpt import ChatGPT
def main():
    chatGPT = ChatGPT()
    chatGPT.append_assistant_message("Hi there")
    chatGPT.append_user_message("Hi")
    print(chatGPT.generate_text_response())

if __name__ == "__main__":
    main()