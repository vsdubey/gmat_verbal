import requests
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variable for the API key
groq_client2 = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_groq_result(messages, model="llama3-70b-8192", temperature=0.3, is_json_response=False, groq_fallback=False):
    client_to_use = groq_client2
    res = client_to_use.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        response_format={"type": "json_object" if is_json_response else "text"},
    )
    res_content = res.choices[0].message.content or ""
    print(res_content)
    return res_content


def generate_question(difficulty, question_type):
    prompt = f"Generate a GMAT verbal {question_type} question with {difficulty} difficulty. Include the question and the correct answer."


    try:
        messages_post_filter = [{"role": "system", "content": prompt}]
        generated_text = get_groq_result(messages_post_filter)
        
        # Parse the generated text to extract question and answer
        # generated_text = result['choices'][0]['text'].strip()
        question, answer = generated_text.split('Answer:', 1)
        
        return {
            'question': question.strip(),
            'answer': answer.strip()
        }
    except requests.RequestException as e:
        print(f"Error generating question: {e}")
        return None
