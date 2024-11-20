from flask import Flask, jsonify, request
import speech_recognition as sr
from main import speech_to_text

# Create a Blueprint for speech-to-text functionality
speech_to_text_bp = Blueprint('speech_to_text', __name__)

@speech_to_text_bp.route('/speech-to-text', methods=['GET'])
def handle_speech_to_text():
    """
    Handle speech-to-text by listening to the microphone and processing the audio.
    Returns the transcribed text.
    """
    query = speech_to_text()  # Call the function from main.py
    return jsonify({'text': query})  # Return the transcribed text as a JSON response