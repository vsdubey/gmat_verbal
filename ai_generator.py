import requests
from config import GROQ_API_KEY, GROQ_API_URL

def generate_question(difficulty, question_type):
    prompt = f"Generate a GMAT verbal {question_type} question with {difficulty} difficulty. Include the question and the correct answer."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Parse the generated text to extract question and answer
        generated_text = result['choices'][0]['text'].strip()
        question, answer = generated_text.split('Answer:', 1)
        
        return {
            'question': question.strip(),
            'answer': answer.strip()
        }
    except requests.RequestException as e:
        print(f"Error generating question: {e}")
        return None
