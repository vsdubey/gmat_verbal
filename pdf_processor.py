import PyPDF2
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_questions_from_pdf(file_path):
    questions = []
    logger.info(f"Processing PDF file: {file_path}")

    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        logger.info(f"Extracted {len(text)} characters from the PDF")

        # Updated pattern to match various question formats
        pattern = r"(Q\d+:|Question \d+:)\s*(.*?)\s*(A:|Answer:)\s*(.*?)(?=Q\d+:|Question \d+:|$)"
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        logger.info(f"Found {len(matches)} potential question-answer pairs")

        for match in matches:
            question = match[1].strip()
            answer = match[3].strip()
            
            # Basic validation to ensure we have both question and answer
            if question and answer:
                questions.append({
                    'question': question,
                    'answer': answer,
                    'difficulty': 'Medium'  # Default difficulty
                })
            else:
                logger.warning(f"Skipped invalid question-answer pair: Q: {question}, A: {answer}")

        logger.info(f"Successfully extracted {len(questions)} valid questions")

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")

    return questions
