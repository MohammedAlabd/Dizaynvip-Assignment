"""
Flask API server for the chatbot application.
"""

import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot import ChatbotManager
from topics import get_all_topics

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow requests from frontend
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
if allowed_origins != '*':
    allowed_origins = allowed_origins.split(',')

CORS(app, 
     resources={r"/api/*": {"origins": allowed_origins}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

# Store active chat sessions (in production, use Redis or similar)
chat_sessions = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get list of available topics."""
    topics = get_all_topics()
    return jsonify({"topics": topics})


@app.route('/api/conversation/start', methods=['POST'])
def start_conversation():
    """Start a new conversation with a random topic."""
    try:
        # Select random topic
        topics = get_all_topics()
        selected_topic = random.choice(topics)
        
        # Create new chatbot instance
        session_id = os.urandom(16).hex()
        chatbot = ChatbotManager()
        
        # Start conversation
        initial_message = chatbot.start_conversation(selected_topic)
        
        # Store session
        chat_sessions[session_id] = chatbot
        
        return jsonify({
            "session_id": session_id,
            "topic": selected_topic,
            "message": initial_message,
            "is_complete": False
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/message', methods=['POST'])
def send_message():
    """Send a message in an ongoing conversation."""
    try:
        data = request.json
        session_id = data.get('session_id')
        user_message = data.get('message')
        
        if not session_id or not user_message:
            return jsonify({"error": "Missing session_id or message"}), 400
        
        # Get chatbot session
        chatbot = chat_sessions.get(session_id)
        if not chatbot:
            return jsonify({"error": "Invalid session_id"}), 404
        
        # Get bot response
        bot_message, is_complete = chatbot.get_bot_response(user_message)
        
        response_data = {
            "message": bot_message,
            "is_complete": is_complete
        }
        
        # If conversation is complete, generate score
        if is_complete:
            evaluation = chatbot.evaluate_and_score()
            response_data["evaluation"] = evaluation
            # Clean up session
            del chat_sessions[session_id]
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/end', methods=['POST'])
def end_conversation():
    """Manually end a conversation and get evaluation."""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({"error": "Missing session_id"}), 400
        
        # Get chatbot session
        chatbot = chat_sessions.get(session_id)
        if not chatbot:
            return jsonify({"error": "Invalid session_id"}), 404
        
        # Generate evaluation
        evaluation = chatbot.evaluate_and_score()
        
        # Clean up session
        del chat_sessions[session_id]
        
        return jsonify({
            "evaluation": evaluation,
            "is_complete": True
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("WARNING: OPENAI_API_KEY not found in environment variables!")
        print("Please create a .env file with your OpenAI API key.")
    
    # Get port from environment variable (for deployment) or use 5001 for local dev
    port = int(os.getenv('PORT', 5001))
    # Use 0.0.0.0 for production deployment, 127.0.0.1 for local dev
    host = os.getenv('HOST', '127.0.0.1')
    debug = os.getenv('FLASK_ENV') != 'production'
    
    app.run(debug=debug, port=port, host=host)

