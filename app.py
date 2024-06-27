from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pyttsx3
import logging

# Set up logging for comtypes to suppress debug messages
logging.getLogger('comtypes').setLevel(logging.WARNING)

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text')
    app.logger.debug(f'Received text: {text}')  # Debugging: Log the received text

    if text:
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()  # Ensure the engine is properly stopped
            return jsonify({'status': 'success', 'message': 'Text spoken'})
        except Exception as e:
            app.logger.error(f'Error: {e}')
            return jsonify({'status': 'error', 'message': 'Failed to speak text'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
