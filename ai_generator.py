import requests
from groq import Groq

groq_client2 = Groq(api_key="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")

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

    # headers = {
    #     "Authorization": f"Bearer {GROQ_API_KEY}",
    #     "Content-Type": "application/json"
    # }

    # data = {
    #     "model": "mixtral-8x7b-32768",
    #     "prompt": prompt,
    #     "max_tokens": 500,
    #     "temperature": 0.7
    # }

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
