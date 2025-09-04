from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Models
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, default=60)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', backref='test', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(10), default='MCQ')
    explanation = db.Column(db.Text)
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_text = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

class TestAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, default=0)
    total_questions = db.Column(db.Integer, default=0)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.relationship('UserAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('test_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_options = db.Column(db.Text)

# AI Functions
def is_ai_available():
    api_key = os.getenv('GEMINI_API_KEY')
    return bool(api_key and api_key.strip())

def extract_text_from_pdf(pdf_path):
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def generate_questions_with_ai(text, num_questions=10):
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return []
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        
        prompt = f"""Generate {num_questions} multiple choice questions from this text.
Return ONLY a valid JSON array with this exact format:
[{{"question": "Question text?", "options": ["Option A", "Option B", "Option C", "Option D"], "correct_answers": [0], "explanation": "Brief explanation", "type": "MCQ"}}]

Text: {text[:2000]}"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            
            # Clean response
            text_response = text_response.strip()
            if text_response.startswith('```json'):
                text_response = text_response[7:]
            if text_response.endswith('```'):
                text_response = text_response[:-3]
            
            return json.loads(text_response.strip())
        return []
    except Exception as e:
        print(f"AI Error: {e}")
        return []

# Routes
@app.route('/api/admin/ai-status')
def ai_status():
    return jsonify({'ai_available': is_ai_available()})

@app.route('/api/admin/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'}), 400
    
    test_title = request.form.get('title', 'Test')
    duration = int(request.form.get('duration', 60))
    
    pdf_path = f"temp_{file.filename}"
    file.save(pdf_path)
    
    try:
        text = extract_text_from_pdf(pdf_path)
        if len(text.strip()) < 50:
            return jsonify({'error': 'PDF contains insufficient text'}), 400
        
        questions_data = generate_questions_with_ai(text)
        if not questions_data:
            return jsonify({'error': 'Failed to generate questions from PDF'}), 400
        
        test = Test(title=test_title, duration=duration)
        db.session.add(test)
        db.session.flush()
        
        for q_data in questions_data:
            question = Question(
                test_id=test.id,
                question_text=q_data['question'],
                question_type=q_data['type'],
                explanation=q_data['explanation']
            )
            db.session.add(question)
            db.session.flush()
            
            for j, option_text in enumerate(q_data['options']):
                option = Option(
                    question_id=question.id,
                    option_text=option_text,
                    is_correct=j in q_data['correct_answers']
                )
                db.session.add(option)
        
        db.session.commit()
        os.remove(pdf_path)
        
        return jsonify({'message': f'Test created with {len(questions_data)} questions'})
    except Exception as e:
        db.session.rollback()
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/upload-json', methods=['POST'])
def upload_json():
    file = request.files['file']
    test_title = request.form.get('title', 'Test')
    duration = int(request.form.get('duration', 60))
    
    try:
        questions_data = json.load(file)
        
        test = Test(title=test_title, duration=duration)
        db.session.add(test)
        db.session.flush()
        
        for q_data in questions_data:
            question = Question(
                test_id=test.id,
                question_text=q_data['question'],
                question_type=q_data['type'],
                explanation=q_data['explanation']
            )
            db.session.add(question)
            db.session.flush()
            
            for i, option_text in enumerate(q_data['options']):
                option = Option(
                    question_id=question.id,
                    option_text=option_text,
                    is_correct=i in q_data['correct_answers']
                )
                db.session.add(option)
        
        db.session.commit()
        return jsonify({'message': 'Test created successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/tests')
def get_tests():
    tests = Test.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'duration': t.duration,
        'question_count': len(t.questions),
        'created_at': t.created_at.isoformat()
    } for t in tests])

@app.route('/api/admin/tests/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    return jsonify({'message': 'Test deleted'})

@app.route('/api/test/available')
def available_tests():
    tests = Test.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'duration': t.duration,
        'question_count': len(t.questions)
    } for t in tests])

@app.route('/api/test/<int:test_id>/start')
def start_test(test_id):
    test = Test.query.get_or_404(test_id)
    questions = []
    for q in test.questions:
        options = [{'id': opt.id, 'text': opt.option_text} for opt in q.options]
        questions.append({
            'id': q.id,
            'question_text': q.question_text,
            'question_type': q.question_type,
            'options': options
        })
    return jsonify({
        'test': {'id': test.id, 'title': test.title, 'duration': test.duration},
        'questions': questions
    })

@app.route('/api/test/submit', methods=['POST'])
def submit_test():
    data = request.json
    
    attempt = TestAttempt(
        test_id=data['test_id'],
        user_name=data['user_name'],
        total_questions=len(data['answers'])
    )
    db.session.add(attempt)
    db.session.flush()
    
    correct_count = 0
    for answer in data['answers']:
        user_answer = UserAnswer(
            attempt_id=attempt.id,
            question_id=answer['question_id'],
            selected_options=json.dumps(answer['selected_options'])
        )
        db.session.add(user_answer)
        
        question = Question.query.get(answer['question_id'])
        correct_options = [opt.id for opt in question.options if opt.is_correct]
        if set(answer['selected_options']) == set(correct_options):
            correct_count += 1
    
    attempt.score = (correct_count / len(data['answers'])) * 100
    db.session.commit()
    
    return jsonify({'attempt_id': attempt.id, 'score': attempt.score})

@app.route('/api/test/result/<int:attempt_id>')
def get_result(attempt_id):
    attempt = TestAttempt.query.get_or_404(attempt_id)
    test = Test.query.get(attempt.test_id)
    
    results = []
    for answer in attempt.answers:
        question = Question.query.get(answer.question_id)
        selected = json.loads(answer.selected_options)
        correct_options = [opt.id for opt in question.options if opt.is_correct]
        
        options_data = []
        for opt in question.options:
            options_data.append({
                'text': opt.option_text,
                'is_correct': opt.is_correct,
                'was_selected': opt.id in selected
            })
        
        results.append({
            'question': question.question_text,
            'options': options_data,
            'explanation': question.explanation,
            'is_correct': set(selected) == set(correct_options)
        })
    
    return jsonify({
        'test_title': test.title,
        'user_name': attempt.user_name,
        'score': attempt.score,
        'total_questions': attempt.total_questions,
        'results': results
    })

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)