from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import logging
from database import init_db, add_question, get_random_question, save_generated_question, get_similar_questions
from pdf_processor import extract_questions_from_pdf
from ai_generator import generate_question
from embeddings import generate_embedding
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        logger.warning("No file part in the request")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        logger.warning("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        logger.info(f"File saved: {filepath}, Size: {file_size} bytes")
        questions = extract_questions_from_pdf(filepath)
        for question in questions:
            add_question(question['question'], question['answer'], 'PDF', question.get('difficulty', 'Medium'))
        os.remove(filepath)
        logger.info(f"Processed {len(questions)} questions from {filename}")
        return jsonify({'message': f'Processed {len(questions)} questions from {filename}'}), 200
    logger.warning(f"Invalid file type: {file.filename}")
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/get_question', methods=['GET'])
def get_question():
    question = get_random_question()
    if question:
        logger.info(f"Retrieved question: ID {question[0]}")
        return jsonify({
            'id': question[0],
            'question': question[1],
            'answer': question[2],
            'source': question[3],
            'difficulty': question[4]
        }), 200
    logger.error("No questions available in the database")
    return jsonify({'error': 'No questions available'}), 404

@app.route('/generate_question', methods=['POST'])
def generate_new_question():
    difficulty = request.json.get('difficulty', 'Medium')
    question_type = request.json.get('type', 'Critical Reasoning')
    generated = generate_question(difficulty, question_type)
    if generated:
        question_id = save_generated_question(generated['question'], generated['answer'], difficulty)
        if question_id:
            return jsonify({
                'id': question_id,
                'question': generated['question'],
                'answer': generated['answer'],
                'source': 'AI',
                'difficulty': difficulty
            }), 201
    logger.error("Failed to generate or save question")
    return jsonify({'error': 'Failed to generate question'}), 500

@app.route('/search', methods=['POST'])
def search_questions():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    query_embedding = generate_embedding(query)
    if not query_embedding:
        return jsonify({'error': 'Failed to generate embedding for search query'}), 500
    
    similar_questions = get_similar_questions(query_embedding)
    results = [
        {
            'id': q[0],
            'question': q[1],
            'answer': q[2],
            'source': q[3],
            'difficulty': q[4],
            'similarity': 1 - q[5]  # Convert distance to similarity
        }
        for q in similar_questions
    ]
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
