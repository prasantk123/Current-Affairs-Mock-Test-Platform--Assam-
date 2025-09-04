# Current Affairs Mock Test Platform

## 🌐 Live Demo
- **Frontend**: [Deploy on Netlify/Vercel]
- **Backend**: [Deploy on Render]
- **Admin Panel**: `/admin`
- **Test Manager**: `/manage`

## 🚀 Quick Start

### Backend
```bash
# For development (Windows/Mac/Linux)
pip install -r requirements-dev.txt
# For production (Linux only)
pip install -r requirements.txt
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Setup
Update `.env`:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=sqlite:///current_affairs.db
SECRET_KEY=your-secret-key-here
```

## 📋 Features

### 🤖 AI-Powered Question Generation
- Upload PDF files
- Automatic text extraction
- AI generates MCQ/MSQ questions
- Includes explanations

### 📝 Manual Question Management
- Upload JSON question files
- Edit questions inline
- Delete/modify tests
- Full CRUD operations

### 📊 Test Analytics
- Detailed performance analysis
- Grade calculation
- Time tracking
- Question-wise breakdown

## 🎛️ Admin Controls

**Main Admin Panel:** `http://localhost:3000/admin`
- Upload PDFs or JSON files
- View AI status
- Create new tests

**Test Manager:** `http://localhost:3000/manage`
- View all tests and questions
- Edit questions inline
- Delete tests/questions
- Manage test content

## 🤖 AI Customization

**See `AI_CUSTOMIZATION.md` for:**
- Custom AI prompts
- Question difficulty levels
- Subject-specific generation
- Quality control parameters
- Multi-language support

## 📁 File Structure

```
current affairs/
├── app/
│   ├── models/models.py      # Database models
│   ├── routes/admin.py       # Admin API routes
│   ├── routes/test.py        # Test API routes
│   └── utils/pdf_processor.py # AI & PDF processing
├── frontend/
│   ├── src/
│   │   ├── views/            # Vue components
│   │   ├── style.css        # Global styles
│   │   └── main.js          # Vue app setup
│   └── package.json
├── .env                      # Environment variables
├── run.py                    # Application entry point
├── sample_questions.json     # Example question format
└── requirements.txt          # Python dependencies
```

## 🔧 API Endpoints

### Admin Routes
```
GET    /api/admin/ai-status           # Check AI availability
GET    /api/admin/tests               # Get all tests
POST   /api/admin/upload-pdf          # Upload PDF for AI generation
POST   /api/admin/upload-json         # Upload JSON questions
DELETE /api/admin/tests/{id}          # Delete test
GET    /api/admin/tests/{id}/questions # Get test questions
PUT    /api/admin/questions/{id}      # Update question
DELETE /api/admin/questions/{id}      # Delete question
```

### Test Routes
```
GET    /api/test/available            # Get available tests
GET    /api/test/{id}/start           # Start test
POST   /api/test/submit               # Submit answers
GET    /api/test/result/{id}          # Get results
```

## 📝 JSON Question Format

```json
[
  {
    "question": "What is the capital of India?",
    "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"],
    "correct_answers": [1],
    "explanation": "Delhi is the capital of India.",
    "type": "MCQ"
  }
]
```

## 🎯 Usage Examples

### Upload PDF Test
1. Go to `http://localhost:3000/admin`
2. Enter test title and duration
3. Select PDF file
4. Click "Upload & Generate"
5. AI creates questions automatically

### Manual Question Upload
1. Create JSON file with questions
2. Go to admin panel
3. Use "Upload Questions JSON" section
4. Select your JSON file

### Take a Test
1. Go to `http://localhost:3000`
2. Click "Start Test" on any available test
3. Enter your name
4. Answer questions
5. View detailed results

## 🔒 Security Notes

- Keep your Gemini API key secure
- Use strong SECRET_KEY in production
- Consider rate limiting for API endpoints
- Validate all file uploads

## 🚀 Production Deployment

1. Update environment variables
2. Use PostgreSQL instead of SQLite
3. Set up proper web server (nginx + gunicorn)
4. Enable HTTPS
5. Configure proper CORS settings

---

**Ready to create professional mock tests with AI-powered question generation!**

## Features

### Admin Features
- Upload PDF files for automatic question generation
- Manual question creation via CRUD interface
- View all created tests and statistics

### User Features
- Browse available tests
- Take timed mock tests with MCQ/MSQ questions
- View detailed results with explanations
- Track performance and scores

## API Endpoints

### Admin Routes (`/api/admin/`)
- `POST /upload-pdf` - Upload PDF and generate questions
- `GET /tests` - Get all tests
- `POST /questions` - Create manual questions

### Test Routes (`/api/test/`)
- `GET /available` - Get available tests
- `GET /<id>/start` - Start a test
- `POST /submit` - Submit test answers
- `GET /result/<id>` - Get test results

## Database Schema
- **Test**: id, title, duration, created_at
- **Question**: id, test_id, question_text, question_type, explanation
- **Option**: id, question_id, option_text, is_correct
- **TestAttempt**: id, test_id, user_name, score, total_questions, attempted_at
- **UserAnswer**: id, attempt_id, question_id, selected_options