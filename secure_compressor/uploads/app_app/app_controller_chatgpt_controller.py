# chatgpt_controller.py
from flask import Blueprint,jsonify, request,render_template,session
from models import User
from services.conversation_service import get_or_create_conversation, save_user_message, save_assistant_message, retrieve_user_ongoing_history_and_pair,get_conversation_status,allow_next_phase,get_phase_permissions
from services.chatgpt_service import get_chatgpt_response,generate_initial_message
from utils import login_required 
import requests

chatgpt_bp = Blueprint('chatgpt_bp', __name__)

@chatgpt_bp.route('/history', methods=['POST'])
@login_required
def user_chat_history():
    data = request.json
    conversation_type = data.get('conversation_type')
    user_id = session.get('user_id')
    
    # Check if user exists
    if not user_id:
        return jsonify({'error': 'User not found'}), 404

    # Retrieve or create a conversation
    conversation = get_or_create_conversation(user_id, conversation_type)

    # Retrieve chat history
    messages = []
    if conversation:
        messages = retrieve_user_ongoing_history_and_pair(user_id, conversation.conversation_id)
    
    pairs = []
    current_prompt = None

    # Build chat history pairs
    for message in messages:
        if message.role == "user":
            current_prompt = message.content
        elif message.role == "assistant":
            pairs.append({
                "prompt": current_prompt,
                "reply": message.content
            })
            current_prompt = None


    if not messages:
        first_message = generate_initial_message(conversation_type, conversation.conversation_id, user_id)
        pairs.append({
            "prompt": "",  # No user input for the first message
            "reply": first_message
        })

    return jsonify({
        'reply': pairs,
        'allow_reflection_phase': allow_next_phase('reflecting'),
        'allow_monitoring_phase': allow_next_phase('monitoring'),
        'allow_planning_phase': allow_next_phase('planning')
    })


@chatgpt_bp.route('/chat', methods=['POST'])
@login_required
def chat_with_gpt():
    try:
        """Process the chat with ChatGPT."""
        data = request.json
        user_id = session.get('user_id')
        conversation_type = data.get('conversation_type')
        user_message = data.get('message')

        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Retrieve or create a new conversation
        conversation = get_or_create_conversation(user_id, conversation_type)

        # Save user's message in the database
        save_user_message(conversation.conversation_id, user_id, user_message)

        # Get response from ChatGPT
        try:
            assistant_reply = get_chatgpt_response(user_message, conversation_type, conversation.conversation_id, user_id)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        # Save assistant's reply
        save_assistant_message(conversation.conversation_id, user_id, assistant_reply)
        allow_planning_phase, allow_monitoring_phase, allow_reflection_phase = get_phase_permissions(user_message, conversation_type)


        # Return the assistant's reply and phase permissions
        return jsonify({
            'reply': assistant_reply,
            'allow_reflection_phase': allow_reflection_phase,
            'allow_monitoring_phase': allow_monitoring_phase,
            'allow_planning_phase' : allow_planning_phase
        })
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with chat api {str(e)}")

@chatgpt_bp.route("/chatscreen")
@login_required
def chatscreen():
    return render_template("main.html")

@chatgpt_bp.route("/tips")
@login_required
def tipsscreen():
    return render_template("tips.html")

@chatgpt_bp.route("/help")
@login_required
def helpscreen():
    return render_template("help.html")

@chatgpt_bp.route("/welcome")
@login_required
def welcomescreen():
    return render_template("welcome.html")

@chatgpt_bp.route("/allow-next-phase", methods=['POST'])
@login_required
def check_next_phase_status():
    data = request.json
    conversation_type = data.get('conversation_type')
    user_message = ""

    allow_planning_phase, allow_monitoring_phase, allow_reflection_phase = get_phase_permissions(
        user_message, conversation_type
    )

    if conversation_type == 'tips':
        if allow_planning_phase and   and allow_reflection_phase:
            allow_planning_phase = True
            allow_monitoring_phase = False
            allow_reflection_phase = False

    return jsonify({
        'allow_reflection_phase': allow_reflection_phase,
        'allow_monitoring_phase': allow_monitoring_phase,
        'allow_planning_phase': allow_planning_phase
    })



    