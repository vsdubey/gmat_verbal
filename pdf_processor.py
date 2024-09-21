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
