# 🤖 AI Customization Guide

## 📝 Customize AI Question Generation

### 1. **Modify AI Prompt**

Edit `backend/app/utils/pdf_processor.py` - Line 35:

```python
prompt = f"""
Generate {num_questions} multiple choice questions from the following current affairs text.

CUSTOM INSTRUCTIONS:
- Focus on factual information and dates
- Include difficulty levels: Easy, Medium, Hard
- Add current affairs context
- Ensure questions test comprehension, not memorization

For each question, provide:
1. Question text
2. 4 options (A, B, C, D)  
3. Correct answer(s)
4. Brief explanation
5. Question type (MCQ for single correct, MSQ for multiple correct)

FORMAT REQUIREMENTS:
- Use simple, clear language
- Avoid ambiguous questions
- Include specific dates and names
- Add explanatory context

Format as JSON array:
[{{
    "question": "Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answers": [0], // indices of correct options
    "explanation": "Explanation here",
    "type": "MCQ",
    "difficulty": "Medium"
}}]

Text: {text[:4000]}
"""
```

### 2. **Adjust Question Count**

Change default number in `backend/app/routes/admin.py` - Line 45:

```python
questions_data = generate_questions_with_ai(text, num_questions=15)  # Change from 10
```

### 3. **Modify AI Model**

Change model in `backend/app/utils/pdf_processor.py` - Line 33:

```python
model = genai.GenerativeModel('gemini-1.5-pro')  # More advanced model
# or
model = genai.GenerativeModel('gemini-1.5-flash')  # Faster model
```

### 4. **Add Question Difficulty Levels**

Update database model in `backend/app/models/models.py`:

```python
class Question(db.Model):
    # ... existing fields ...
    difficulty = db.Column(db.String(10), default='Medium')  # Add this line
```

### 5. **Custom Question Types**

Modify prompt to include:
- **True/False questions**
- **Fill in the blanks**
- **Match the following**
- **Assertion-Reason questions**

Example prompt addition:
```python
"question_types": ["MCQ", "MSQ", "TRUE_FALSE", "FILL_BLANK"]
```

### 6. **Subject-Specific Prompts**

Create specialized prompts for different subjects:

```python
def get_subject_prompt(subject, text, num_questions):
    prompts = {
        "current_affairs": "Focus on recent events, government policies, international relations...",
        "history": "Focus on dates, events, personalities, cause-effect relationships...",
        "geography": "Focus on locations, physical features, climate, demographics...",
        "science": "Focus on concepts, processes, discoveries, applications..."
    }
    
    base_prompt = prompts.get(subject, prompts["current_affairs"])
    return f"{base_prompt}\n\nText: {text}"
```

### 7. **Quality Control Parameters**

Add validation rules in `pdf_processor.py`:

```python
def validate_generated_questions(questions):
    valid_questions = []
    for q in questions:
        # Check question length
        if len(q['question']) < 20 or len(q['question']) > 200:
            continue
            
        # Check option variety
        if len(set(q['options'])) != len(q['options']):
            continue
            
        # Check explanation quality
        if len(q['explanation']) < 30:
            continue
            
        valid_questions.append(q)
    
    return valid_questions
```

### 8. **Advanced AI Configuration**

Add to `pdf_processor.py`:

```python
generation_config = {
    "temperature": 0.7,  # Creativity level (0-1)
    "top_p": 0.8,       # Nucleus sampling
    "top_k": 40,        # Top-k sampling
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
```

### 9. **Multi-Language Support**

Add language parameter:

```python
def generate_questions_with_ai(text, num_questions=10, language="English"):
    prompt = f"""
    Generate {num_questions} questions in {language} language...
    """
```

### 10. **Custom Question Templates**

Create question templates:

```python
QUESTION_TEMPLATES = {
    "factual": "What is the {concept} mentioned in the text?",
    "analytical": "Why did {event} occur according to the passage?",
    "comparative": "How does {item1} differ from {item2}?",
    "chronological": "When did {event} take place?"
}
```

## 🎯 Quick Customization Examples

### **For Competitive Exams:**
```python
prompt = f"""
Generate {num_questions} UPSC/SSC style questions focusing on:
- Current affairs from last 12 months
- Government schemes and policies  
- International relations
- Economic developments
- Awards and recognitions

Difficulty: 70% Medium, 30% Hard
"""
```

### **For Academic Tests:**
```python
prompt = f"""
Generate {num_questions} academic questions with:
- Clear learning objectives
- Progressive difficulty
- Conceptual understanding focus
- Real-world applications

Include bloom's taxonomy levels: Remember, Understand, Apply, Analyze
"""
```

### **For Quick Assessments:**
```python
prompt = f"""
Generate {num_questions} quick assessment questions:
- Short, direct questions
- Clear, unambiguous options
- Focus on key facts and figures
- Time-efficient for test-takers
"""
```

## 🔧 Implementation Steps

1. **Backup original files**
2. **Edit the prompt in `pdf_processor.py`**
3. **Test with sample PDF**
4. **Adjust based on results**
5. **Deploy changes**

## 📊 Monitoring AI Performance

Add logging to track:
- Question generation success rate
- Average processing time
- Question quality scores
- User feedback on generated questions

Your AI is now fully customizable for any specific requirements!