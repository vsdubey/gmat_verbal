import io
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_questions_from_pdf(file_path):
    questions = []
    logger.info(f"Processing PDF file: {file_path}")

    try:
        output_string = io.StringIO()
        with open(file_path, 'rb') as file:
            extract_text_to_fp(file, output_string, laparams=LAParams(), output_type='text', codec='utf-8')
        
        text = output_string.getvalue()

        logger.info(f"Extracted {len(text)} characters from the PDF")
        logger.info(f"First 1000 characters of extracted text: {text[:1000]}")

        # More lenient regex pattern
        pattern = r"(?:Q(?:uestion)?\s*\d+[:.]?\s*)(.*?)(?:A(?:nswer)?[:.]?\s*)(.*?)(?=Q(?:uestion)?\s*\d+[:.]?|$)"
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        logger.info(f"Found {len(matches)} potential question-answer pairs")

        for i, match in enumerate(matches, 1):
            question = match[0].strip()
            answer = match[1].strip()
            
            logger.info(f"Processing pair {i}:")
            logger.info(f"Question: {question[:100]}...")
            logger.info(f"Answer: {answer[:100]}...")

            # Basic validation to ensure we have both question and answer
            if question and answer:
                questions.append({
                    'question': question,
                    'answer': answer,
                    'difficulty': 'Medium'  # Default difficulty
                })
                logger.info(f"Added question-answer pair {i}")
            else:
                logger.warning(f"Skipped invalid question-answer pair {i}")

        logger.info(f"Successfully extracted {len(questions)} valid questions")

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")

    return questions
