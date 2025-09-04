from flask import Blueprint, request, jsonify
from app.models.models import db, Test, Question, Option, TestAttempt, UserAnswer

test_bp = Blueprint('test', __name__)

@test_bp.route('/available', methods=['GET'])
def get_available_tests():
    tests = Test.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'duration': t.duration,
        'question_count': len(t.questions)
    } for t in tests])

@test_bp.route('/<int:test_id>/start', methods=['GET'])
def start_test(test_id):
    test = Test.query.get_or_404(test_id)
    questions = []
    
    for q in test.questions:
        options = [{'id': opt.id, 'text': opt.option_text} for opt in q.options]
        questions.append({
            'id': q.id,
            'question': q.question_text,
            'type': q.question_type,
            'options': options
        })
    
    return jsonify({
        'test_id': test.id,
        'title': test.title,
        'duration': test.duration,
        'questions': questions
    })

@test_bp.route('/submit', methods=['POST'])
def submit_test():
    data = request.json
    test_id = data['test_id']
    user_name = data['user_name']
    answers = data['answers']  # {question_id: [selected_option_ids]}
    
    test = Test.query.get_or_404(test_id)
    
    # Calculate score
    score = 0
    total_questions = len(test.questions)
    
    attempt = TestAttempt(
        test_id=test_id,
        user_name=user_name,
        total_questions=total_questions
    )
    db.session.add(attempt)
    db.session.flush()
    
    for question in test.questions:
        correct_options = {opt.id for opt in question.options if opt.is_correct}
        user_selected = set(answers.get(str(question.id), []))
        
        # Store user answer
        user_answer = UserAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_options=list(user_selected)
        )
        db.session.add(user_answer)
        
        # Check if answer is correct
        if user_selected == correct_options:
            score += 1
    
    attempt.score = score
    db.session.commit()
    
    return jsonify({
        'attempt_id': attempt.id,
        'score': score,
        'total': total_questions,
        'percentage': round((score/total_questions)*100, 2)
    })

@test_bp.route('/result/<int:attempt_id>', methods=['GET'])
def get_result(attempt_id):
    attempt = TestAttempt.query.get_or_404(attempt_id)
    test = Test.query.get(attempt.test_id)
    
    results = []
    for answer in attempt.answers:
        question = Question.query.get(answer.question_id)
        correct_options = [opt.id for opt in question.options if opt.is_correct]
        
        results.append({
            'question': question.question_text,
            'user_answer': answer.selected_options,
            'correct_answer': correct_options,
            'is_correct': set(answer.selected_options) == set(correct_options),
            'explanation': question.explanation,
            'options': [{'id': opt.id, 'text': opt.option_text, 'is_correct': opt.is_correct} 
                       for opt in question.options]
        })
    
    return jsonify({
        'test_title': test.title,
        'score': attempt.score,
        'total': attempt.total_questions,
        'percentage': round((attempt.score/attempt.total_questions)*100, 2),
        'results': results
    })