import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend', '.env'))

try:
    import google.generativeai as genai
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key and api_key.strip():
        genai.configure(api_key=api_key.strip())
        AI_AVAILABLE = True
    else:
        AI_AVAILABLE = False
except ImportError:
    AI_AVAILABLE = False
except Exception:
    AI_AVAILABLE = False

def extract_text_from_pdf(pdf_path):
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        return "PDF processing not available. Install PyMuPDF: pip install PyMuPDF"

def is_ai_available():
    return AI_AVAILABLE

def generate_questions_with_ai(text, num_questions=10):
    if not AI_AVAILABLE:
        return []
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Generate {num_questions} multiple choice questions from the following current affairs text.
    For each question, provide:
    1. Question text
    2. 4 options (A, B, C, D)
    3. Correct answer(s)
    4. Brief explanation
    5. Question type (MCQ for single correct, MSQ for multiple correct)
    
    Format as JSON array:
    [{{
        "question": "Question text here",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answers": [0], // indices of correct options
        "explanation": "Explanation here",
        "type": "MCQ"
    }}]
    
    Text: {text[:4000]}  # Limit text to avoid token limits
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Clean the response text
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        questions_data = json.loads(response_text.strip())
        return questions_data
    except Exception:
        return []

def validate_questions_json(data):
    """Validate JSON structure for manual upload"""
    required_fields = ['question', 'options', 'correct_answers', 'explanation', 'type']
    
    if not isinstance(data, list):
        return False, "Data must be an array of questions"
    
    for i, q in enumerate(data):
        for field in required_fields:
            if field not in q:
                return False, f"Question {i+1} missing field: {field}"
        
        if not isinstance(q['options'], list) or len(q['options']) < 2:
            return False, f"Question {i+1} must have at least 2 options"
        
        if not isinstance(q['correct_answers'], list) or not q['correct_answers']:
            return False, f"Question {i+1} must have at least one correct answer"
        
        if q['type'] not in ['MCQ', 'MSQ']:
            return False, f"Question {i+1} type must be MCQ or MSQ"
    
    return True, "Valid"