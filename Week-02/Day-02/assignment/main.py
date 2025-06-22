from website_details import WebsiteDetails
from brochure_creation_prompts import BrochureCreationPrompts
from chatgpt import ChatGPT
from claude import Claude
from gemini import Gemini
import gradio as gr

def stream_brochure(company_name, url, model):
    website = WebsiteDetails(url)
    website.fetch
    
    prompts = BrochureCreationPrompts(company_name, website.content)
    
    print("\nSYSTEM PROMPT:\n", prompts.system_prompt)
    print("\nUSER PROMPT:\n", prompts.user_prompt)
    print("")
    
    if model == "ChatGPT":
        result = ChatGPT(prompts.system_prompt, prompts.user_prompt).stream_response()
    elif model == "Claude":
        result = Claude(prompts.system_prompt, prompts.user_prompt).stream_response()
    elif model == "Gemini":
        result = Gemini(prompts.system_prompt, prompts.user_prompt).stream_response()
    else:
        raise ValueError(f"Unsupported model: {model}")
    
    yield from result
    #return result
    
def main():
    view = gr.Interface(
        fn=stream_brochure,
        inputs=[
            gr.Textbox(label="Company Name:"),
            gr.Textbox(label="URL:"),
            gr.Dropdown(["ChatGPT", "Claude", "Gemini"], label="Select Model:"),
        ],
        outputs=[gr.Markdown(label="Response:")],
        flagging_mode="never"
    )
    view.launch(share=True)
    
if __name__ == "__main__":
    main()