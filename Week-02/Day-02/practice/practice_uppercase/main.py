
import gradio as gr


def uppercase(text):
    print(f"[main.py][uppercase] => (text): '{text}'")
    return text.upper()
    
def main():
    gr.Interface(fn=uppercase, inputs="textbox", outputs="textbox").launch(share=True)
    
if __name__ == "__main__":
    main()