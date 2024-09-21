from flask import Flask, request, jsonify, render_template
import logging
import os
from ai_generator import generate_question

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_question', methods=['POST'])
def generate_new_question():
    difficulty = request.json.get('difficulty', 'Medium')
    question_type = request.json.get('type', 'Critical Reasoning')
    generated = generate_question(difficulty, question_type)
    if generated:
        return jsonify({
            'question': generated['question'],
            'answer': generated['answer'],
            'source': 'AI',
            'difficulty': difficulty
        }), 201
    logger.error("Failed to generate question")
    return jsonify({'error': 'Failed to generate question'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port)  # Bind to the port