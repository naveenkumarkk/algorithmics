import requests
import os
from services.conversation_service import update_conversation_status,save_assistant_message
url = os.getenv('ENDPOINT_URL','https://tu-openai-api-management.azure-api.net/nail-projects/openai/deployments/gpt-4o-nail/chat/completions')
querystring = {"api-version": os.getenv('CHAT_GPT_API_VERSION','2024-08-01-preview')}


def get_chatgpt_response(user_message, conversation_type, conversation_id, user_id):
    """
    Generates a response from ChatGPT and provides an initial starter message if no user input.
    """
    try:
        # Detect if conversation just started (no user message)
        if not user_message or user_message.strip() == "":
            return generate_initial_message(conversation_type,conversation_id,user_id)
            
        # Detect if the user mentions finishing a phase
        if any(keyword in user_message.lower() for keyword in ["finished", "completed", "done"]):
            update_conversation_status(conversation_id, 'completed')
            if conversation_type == "planning":
                return (
                    "Great job on completing your planning phase! Now, let's move on to the monitoring phase. "
                    "Good luck, and keep up the great work!"
                )
            elif conversation_type == "monitoring":
                return (
                    "Well done on completing your monitoring phase! Let's move on to the reflecting phase. "
                    "\nThe reflecting phase helps you analyze your actions and outcomes, ensuring continuous improvement. Keep it up!"
                )
            elif conversation_type == "reflecting":
                return (
                    "Fantastic! You've completed the reflecting phase and learned from your experiences. "
                    "Now, it's time to apply these insights to your next plan. Start the planning phase again, "
                    "and let the AI tutor guide you in setting even better goals and strategies for success!"
                )

        # Dynamically adjust the system content based on the conversation type
        system_content = {
            "planning": (
                "You are an AI tutor designed to help students create and manage their study plans based on Self-Regulated Learning (SRL). "
                "Encourage students to create their own plans by setting goals, deadlines, and priorities. "
                "Ask questions like: 'What is your task?', 'How complicated do you think it will be?', or 'What resources do you need?'. "
                "Avoid giving solutions; instead, provide reflective prompts to guide their planning process."
            ),
            "reflecting": (
                "You are an AI tutor guiding students through self-reflection to improve their performance. "
                "Ask questions that analyze the connection between actions (causes) and outcomes (effects), such as: "
                "'Why do you think this approach worked?' or 'What could you have done differently?'. "
                "Help students learn from their experiences and improve future outcomes."
            ),
            "monitoring": (
                "You are an AI tutor helping students monitor their progress and stay motivated. "
                "Ask questions like: 'On which task are you currently working?' or 'How is your progress compared to your plan?'. "
                "Encourage students to assess if they are staying on track with their goals and timelines. "
                "If they are falling behind, suggest tips for minimizing distractions or rescheduling tasks."
            ),
        }.get(conversation_type, "You are an AI tutor designed to help students with their study goals.")

        # Prepare the payload for the OpenAI API
        payload = {
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 1000,
            "temperature": 0.3,
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Insomnia/2023.5.6",
            "api-key": os.getenv('CHAT_GPT_API_KEY'),
        }

        # Make the POST request to ChatGPT API
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        response.raise_for_status()

        # Extract the assistant's reply
        assistant_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        return assistant_reply

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with OpenAI API: {str(e)}")


def generate_initial_message(conversation_type, conversation_id, user_id):
    """
    Generates the first introductory message based on the conversation type.
    """
    if conversation_type == "planning":
        initial_message = (
            "Welcome to the planning phase! Let's get started. "
            "What task do you want to plan for? Try breaking it into smaller steps, setting priorities, and deadlines. "
            "How can I assist you in creating your study plan?"
        )
    elif conversation_type == "monitoring":
        initial_message = (
            "Welcome to the monitoring phase! I'm here to help you track your progress. "
            "On which task are you currently working? How is your progress compared to your plan?"
        )
    elif conversation_type == "reflecting":
        initial_message = (
            "Welcome to the reflecting phase! Let's analyze what worked and what didn't. "
            "What task did you recently complete? Why do you think it was successful, or what could have been improved?"
        )
    else:
        initial_message = ("Welcome! I'm your AI tutor here to assist with your study goals. How can I help you get started?")

    save_assistant_message(conversation_id, user_id, initial_message)

    return initial_message