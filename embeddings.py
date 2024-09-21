import openai
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_embedding(text):
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return None

def generate_question_embedding(question):
    return generate_embedding(question['question'])

def generate_answer_embedding(question):
    return generate_embedding(question['answer'])
