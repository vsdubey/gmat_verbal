import PyPDF2
import re

def extract_questions_from_pdf(file_path):
    questions = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Simple pattern matching for questions and answers
    # This is a basic implementation and may need to be adjusted based on the actual PDF structure
    pattern = r"Q(\d+):\s*(.*?)\s*A:\s*(.*?)(?=Q\d+:|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        questions.append({
            'question': match[1].strip(),
            'answer': match[2].strip(),
            'difficulty': 'Medium'  # Default difficulty, can be improved with more sophisticated analysis
        })

    return questions
