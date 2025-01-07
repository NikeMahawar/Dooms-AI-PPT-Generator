import os
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from dotenv import load_dotenv

load_dotenv()
jamba_api_key = os.getenv("JAMBA_KEY")

# Initialize the AI21 client
client = AI21Client(api_key=jamba_api_key)

def chat_development(user_message):
    conversation = build_conversation(user_message)
    try:
        assistant_message = generate_assistant_message(conversation)
    except Exception as e:
        assistant_message = f"An error occurred: {e}"

    return assistant_message

def build_conversation(user_message):
    # Build conversation structure for AI21 API
    return [
        UserMessage(content=(
            "You are an expert in medical science with deep knowledge across various disciplines including clinical practice, research, and medical education. "
            "You are tasked with creating detailed, content-rich PowerPoint slides on the requested topic. Each slide should include a title, content, and keywords for image searches. "
            "Please format your response as follows for each slide:\n"
            "Slide X:\n"
            "Title: {Slide Title}\n"
            "Content: {Detailed content with multiple paragraphs, subheadings if needed, and full sentences}\n"
            "Keywords: {Two-word keyword for image search}\n\n"
            "Separate each slide with a line containing only '---'. Ensure there are no additional characters like '**' or unnecessary labels."
        )),
        UserMessage(content=user_message)
    ]

def generate_assistant_message(conversation):
    # Create a response using the AI21 Jamba 1.5 API
    response = client.chat.completions.create(
        model="jamba-1.5-large",
        messages=conversation
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    user_message = input("Enter your message: ")
    response = chat_development(user_message)
    print("Assistant Response:", response)
