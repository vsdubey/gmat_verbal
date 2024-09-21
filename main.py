from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from database import init_db, add_question, get_random_question, save_generated_question
from pdf_processor import extract_questions_from_pdf
from ai_generator import generate_question
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        questions = extract_questions_from_pdf(filepath)
        for question in questions:
            add_question(question['question'], question['answer'], 'PDF', question.get('difficulty', 'Medium'))
        os.remove(filepath)
        return jsonify({'message': f'Processed {len(questions)} questions from {filename}'}), 200
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/get_question', methods=['GET'])
def get_question():
    question = get_random_question()
    if question:
        return jsonify({
            'id': question[0],
            'question': question[1],
            'answer': question[2],
            'source': question[3],
            'difficulty': question[4]
        }), 200
    return jsonify({'error': 'No questions available'}), 404

@app.route('/generate_question', methods=['POST'])
def generate_new_question():
    difficulty = request.json.get('difficulty', 'Medium')
    question_type = request.json.get('type', 'Critical Reasoning')
    generated = generate_question(difficulty, question_type)
    if generated:
        question_id = save_generated_question(generated['question'], generated['answer'], difficulty)
        return jsonify({
            'id': question_id,
            'question': generated['question'],
            'answer': generated['answer'],
            'source': 'AI',
            'difficulty': difficulty
        }), 201
    return jsonify({'error': 'Failed to generate question'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
