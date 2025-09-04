// API Configuration
export const API_BASE_URL = import.meta.env.PROD 
  ? 'https://your-backend-url.onrender.com'  // Replace with your actual Render backend URL
  : 'http://localhost:5000'

export const config = {
  apiUrl: API_BASE_URL,
  maxFileSize: 16 * 1024 * 1024, // 16MB
  supportedFormats: ['.pdf', '.json'],
  defaultTestDuration: 60
}