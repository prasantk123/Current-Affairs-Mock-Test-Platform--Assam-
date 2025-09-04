# Current Affairs Mock Test Platform

## Setup

### Backend
```bash
pip install -r requirements.txt
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment
Create `.env` file:
```env
GEMINI_API_KEY=your_api_key
DATABASE_URL=sqlite:///current_affairs.db
SECRET_KEY=your-secret-key
```

## Features

- AI-powered PDF to question generation
- Manual JSON question upload
- Admin dashboard with full CRUD
- Test taking interface
- Performance analytics

## Usage

1. **Admin**: `/admin` - Upload PDFs/JSON, manage tests
2. **Manager**: `/manage` - Edit questions, delete tests
3. **Tests**: `/` - Take tests, view results

## Deployment

**Render:**
- Build: `pip install -r requirements.txt`
- Start: `gunicorn run:app`
- Add environment variables

**Netlify/Vercel:**
- Build: `cd frontend && npm run build`
- Deploy: `frontend/dist` folder