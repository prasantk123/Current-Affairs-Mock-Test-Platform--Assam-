from flask import Blueprint, request, jsonify
from app.models.models import db, Test, Question, Option
from app.utils.pdf_processor import extract_text_from_pdf, generate_questions_with_ai, is_ai_available, validate_questions_json
import os
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/ai-status', methods=['GET'])
def ai_status():
    api_key = os.getenv('GEMINI_API_KEY')
    return jsonify({
        'ai_available': is_ai_available(),
        'has_api_key': bool(api_key and api_key.strip()),
        'api_key_preview': api_key[:10] + '...' if api_key else None
    })

@admin_bp.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'}), 400
    
    test_title = request.form.get('title', 'Untitled Test')
    duration = int(request.form.get('duration', 60))
    
    pdf_path = f"temp_{file.filename}"
    file.save(pdf_path)
    
    try:
        text = extract_text_from_pdf(pdf_path)
        
        if len(text.strip()) < 50:
            return jsonify({'error': 'PDF contains insufficient text for question generation'}), 400
        
        if is_ai_available():
            questions_data = generate_questions_with_ai(text)
            if not questions_data:
                return jsonify({'error': 'AI failed to generate questions from this PDF'}), 400
        else:
            return jsonify({'error': 'AI not available. Please upload questions JSON manually.'}), 400
        
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
        
        return jsonify({
            'message': f'Test "{test_title}" created successfully with {len(questions_data)} questions',
            'test_id': test.id
        })
    
    except Exception as e:
        db.session.rollback()
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

@admin_bp.route('/upload-json', methods=['POST'])
def upload_json():
    if 'file' not in request.files:
        return jsonify({'error': 'No JSON file uploaded'}), 400
    
    file = request.files['file']
    test_title = request.form.get('title', 'Untitled Test')
    duration = int(request.form.get('duration', 60))
    
    try:
        questions_data = json.load(file)
        
        # Validate JSON structure
        is_valid, message = validate_questions_json(questions_data)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Create test and questions
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
        
        return jsonify({'message': 'Test created successfully from JSON', 'test_id': test.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/tests', methods=['GET'])
def get_tests():
    tests = Test.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'duration': t.duration,
        'question_count': len(t.questions),
        'created_at': t.created_at.isoformat()
    } for t in tests])

@admin_bp.route('/tests/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    return jsonify({'message': 'Test deleted successfully'})

@admin_bp.route('/tests/<int:test_id>/questions', methods=['GET'])
def get_test_questions(test_id):
    test = Test.query.get_or_404(test_id)
    questions = []
    for q in test.questions:
        options = [{'id': opt.id, 'text': opt.option_text, 'is_correct': opt.is_correct} for opt in q.options]
        questions.append({
            'id': q.id,
            'question_text': q.question_text,
            'question_type': q.question_type,
            'explanation': q.explanation,
            'options': options
        })
    return jsonify({'test': {'id': test.id, 'title': test.title}, 'questions': questions})

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted successfully'})

@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.json
    
    question.question_text = data['question_text']
    question.question_type = data['question_type']
    question.explanation = data.get('explanation', '')
    
    # Delete existing options
    for option in question.options:
        db.session.delete(option)
    
    # Add new options
    for opt_data in data['options']:
        option = Option(
            question_id=question.id,
            option_text=opt_data['text'],
            is_correct=opt_data['is_correct']
        )
        db.session.add(option)
    
    db.session.commit()
    return jsonify({'message': 'Question updated successfully'})

@admin_bp.route('/questions', methods=['POST'])
def create_question():
    data = request.json
    question = Question(
        test_id=data['test_id'],
        question_text=data['question_text'],
        question_type=data['question_type'],
        explanation=data.get('explanation', '')
    )
    db.session.add(question)
    db.session.flush()
    
    for opt_data in data['options']:
        option = Option(
            question_id=question.id,
            option_text=opt_data['text'],
            is_correct=opt_data['is_correct']
        )
        db.session.add(option)
    
    db.session.commit()
    return jsonify({'message': 'Question created', 'question_id': question.id})