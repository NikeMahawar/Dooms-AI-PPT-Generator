import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Set your Gemini API key
genai_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=genai_api_key)

class GeminiPro:
    def __init__(self):
        self.model_name = "models/gemini-1.5-flash"

    def chat_development(self, user_message):
        conversation = self.build_conversation(user_message)
        try:
            response = self.generate_assistant_message(conversation)
        except Exception as err:
            response = f"An error occurred: {str(err)}"
        return response

    def build_conversation(self, user_message):
        return [
        {"role": "system",
         "content": ("You are tasked with creating detailed PowerPoint slides based on the user's input. "
                     "Ensure the 'Content' section for each slide contains approximately 100–120 words. "
                     "Each slide should be written as if you are presenting to an audience of medical students, professionals, or researchers. "
                     "Follow this format strictly: "
                     "Slide X: Title: {Title} Content: /n {Detailed content with approximately 100–120 words}. "
                     "Keywords: {keyword1, keyword2, ...}. "
                     "Provide concise, accurate, and relevant information for each slide.")},
        {"role": "user", "content": user_message}
    ]

    def generate_assistant_message(self, conversation):
        chat = genai.GenerativeModel(self.model_name).start_chat(history=[])
        response = chat.send_message(conversation[-1]['content'])  # Assuming a simple conversation structure
        return response.text

# Example usage
def chat_development(user_message):
    gemini_bot = GeminiPro()
    return gemini_bot.chat_development(user_message)
