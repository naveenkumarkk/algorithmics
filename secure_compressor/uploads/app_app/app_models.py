from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(240), nullable=False)  # Maps to "given_name"
    last_name = db.Column(db.String(240), nullable=False)   # Maps to "family_name"
    email = db.Column(db.String(120), unique=True, nullable=False)  # Maps to "email"
    google_id = db.Column(db.String(255), unique=True, nullable=True)  # Maps to "id" from Google info
    profile_picture = db.Column(db.String(255), nullable=True)  # Maps to "picture"
    verified_email = db.Column(db.Boolean, nullable=True)  # Maps to "verified_email"
    sex = db.Column(db.Enum('male', 'female', 'not-preferred', name='sex'), default='not-preferred')
    nationality = db.Column(db.String(120), nullable=True)
    occupation = db.Column(db.String(120), nullable=True)
    organisation = db.Column(db.String(120), nullable=True)
    google_token = db.Column(db.Text, nullable=True)  # Google OAuth token
    microsoft_token = db.Column(db.Text, nullable=True)  # Microsoft OAuth token
    last_login = db.Column(db.DateTime, nullable=True)  # For tracking user's last login
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # User creation timestamp

    # Relationship: One user can have many conversations
    conversations = db.relationship('Conversation', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'


# Conversation model to track conversation sessions
class Conversation(db.Model):
    __tablename__ = 'conversations'
    conversation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('ongoing', 'completed', 'paused', name='conversation_status'), default='ongoing')
    conversation_type = db.Column(db.Enum('planning','monitoring','reflecting',name='conversation_type'),nullable = False)
    # Relationship: One conversation can have many messages
    messages = db.relationship('Message', backref='conversation', lazy=True)

    def __repr__(self):
        return f'<Conversation {self.conversation_id} for user {self.user_id}>'


# Message model to store each interaction in the conversation
class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.conversation_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    role = db.Column(db.Enum('user', 'assistant', name='message_role'), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.message_id} in conversation {self.conversation_id}>'

