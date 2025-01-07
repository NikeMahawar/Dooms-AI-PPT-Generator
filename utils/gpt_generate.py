import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GPT-key")

def chat_development(user_message):
    conversation = build_conversation(user_message)
    try:
        assistant_message = generate_assistant_message(conversation)
    except openai.error.RateLimitError:
        assistant_message = "Rate limit exceeded. Please try again later."

    return assistant_message

def build_conversation(user_message):
    return [
        {"role": "system",
         "content": ("You are an expert in medical science with deep knowledge across various disciplines including clinical practice, research, and medical education. "
                    "You are tasked with creating detailed, content-rich PowerPoint slides on the requested topic. Each slide should be written as if you are presenting to an audience of medical students, professionals, or researchers. "
                    "Provide comprehensive information with full explanations, relevant examples, and up-to-date research where applicable. "
                    "Ensure the content is accurate, in-depth, and suitable for educational purposes. "
                    "Structure each slide with a title, detailed content, and relevant keywords to capture the essence of the slide. "
                    "The format of the response should be: Slide X: {Title} Content: /n {Detailed content with multiple paragraphs, subheadings if needed, and full sentences}. "
                    )},
        {"role": "user", "content": user_message}
    ]

def generate_assistant_message(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        max_tokens=5500,  # Increased token limit for more detailed content (adjust as needed)
        temperature=0.7  # Adjust temperature for balanced output
    )
    return response['choices'][0]['message']['content']
