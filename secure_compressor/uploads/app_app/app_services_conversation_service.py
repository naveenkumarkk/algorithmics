from models import db, User, Conversation, Message
from datetime import datetime
from flask import session
import requests

def get_or_create_conversation(user_id,conversation_type):
    """Retrieve an ongoing conversation or create a new one."""
    conversation = Conversation.query.filter_by(user_id=user_id, status='ongoing',conversation_type = conversation_type).first()
    if not conversation:
        conversation = Conversation(user_id=user_id,conversation_type = conversation_type)
        db.session.add(conversation)
        db.session.commit()
    return conversation

def get_conversation_status(user_id,conversation_type):
    return Conversation.query.filter_by(user_id=user_id, status='ongoing',conversation_type = conversation_type).first()

def retrieve_user_ongoing_history_and_pair(user_id, conversation_id):
    return (
        Message.query.filter_by(user_id=user_id, conversation_id=conversation_id,)
        .order_by(Message.created_at)
        .all()
    )

def save_user_message(conversation_id, user_id, user_message):
    """Save a user's message in the database."""
    user_msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role='user',
        content=user_message,
        created_at=datetime.utcnow()
    )
    db.session.add(user_msg)
    db.session.commit()

def save_assistant_message(conversation_id, user_id, assistant_reply):
    """Save the assistant's reply in the database."""
    assistant_msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role='assistant',
        content=assistant_reply,
        created_at=datetime.utcnow()
    )
    db.session.add(assistant_msg)
    db.session.commit()

def update_conversation_status(conversation_id,status):
     conversation = Conversation.query.filter_by(conversation_id = conversation_id).first()
     if conversation:
        conversation.status = status
        db.session.commit()
    
def allow_next_phase(conversation_type):
    """
    Determines whether the next phase is allowed based on conversation status.
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return False

        dependencies = {
            'monitoring': ['planning', 'reflecting'],
            'reflecting': ['monitoring', 'planning'],
            'planning': ['reflecting', 'monitoring']
        }

        if conversation_type not in dependencies:
            return True 

        for dependent_phase in dependencies[conversation_type]:
            if get_conversation_status(user_id, dependent_phase):
                return False

        return True  # Allow if no dependencies are active

    except Exception as e:
        raise Exception(f"Error in allow_next_phase: {str(e)}")


def get_phase_permissions(user_message, conversation_type):
    message_lower = user_message.lower()

    allow_planning_phase = allow_next_phase('planning')
    allow_monitoring_phase = allow_next_phase('monitoring')
    allow_reflection_phase = allow_next_phase('reflecting')

    if any(keyword in message_lower for keyword in ["finished", "completed", "done"]):
        phase_map = {
            'planning': {'allow_planning_phase': False, 'allow_monitoring_phase': True, 'allow_reflection_phase': False},
            'monitoring': {'allow_planning_phase': False, 'allow_monitoring_phase': False, 'allow_reflection_phase': True},
            'reflecting': {'allow_planning_phase': True, 'allow_monitoring_phase': False, 'allow_reflection_phase': False}
        }

        current_phase = phase_map.get(conversation_type, {})
        allow_planning_phase = current_phase.get('allow_planning_phase', allow_planning_phase)
        allow_monitoring_phase = current_phase.get('allow_monitoring_phase', allow_monitoring_phase)
        allow_reflection_phase = current_phase.get('allow_reflection_phase', allow_reflection_phase)

    return allow_planning_phase, allow_monitoring_phase, allow_reflection_phase

