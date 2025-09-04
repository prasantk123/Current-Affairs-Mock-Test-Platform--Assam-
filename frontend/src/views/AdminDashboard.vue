<template>
  <div class="container">
    <div class="card">
      <h1 style="text-align: center; color: #333; margin-bottom: 30px;">⚙️ Admin Dashboard</h1>
      
      <div class="alert" :class="aiAvailable ? 'alert-success' : 'alert-warning'">
        <strong>🤖 AI Status:</strong> {{ aiAvailable ? '✓ Available - You can upload PDFs for automatic question generation' : '⚠️ Not Available - Use JSON upload for manual questions' }}
      </div>
    </div>
    
    <!-- PDF Upload Section (AI) -->
    <div class="card" v-if="aiAvailable">
      <h2 style="color: #667eea; margin-bottom: 20px;">📄 Upload PDF & Generate Test (AI)</h2>
      <form @submit.prevent="uploadPDF">
        <div class="form-group">
          <input v-model="testTitle" class="form-control" placeholder="Test Title" required />
        </div>
        <div class="form-group">
          <input v-model="duration" type="number" class="form-control" placeholder="Duration (minutes)" required />
        </div>
        <div class="form-group">
          <input type="file" class="form-control" @change="selectFile" accept=".pdf" required />
        </div>
        <button type="submit" class="btn" :disabled="uploading" style="width: 100%;">
          {{ uploading ? '🔄 Processing...' : '🚀 Upload & Generate' }}
        </button>
      </form>
    </div>
    
    <!-- JSON Upload Section -->
    <div class="card">
      <h2 style="color: #667eea; margin-bottom: 20px;">📁 Upload Questions JSON (Manual)</h2>
      <form @submit.prevent="uploadJSON">
        <div class="form-group">
          <input v-model="jsonTestTitle" class="form-control" placeholder="Test Title" required />
        </div>
        <div class="form-group">
          <input v-model="jsonDuration" type="number" class="form-control" placeholder="Duration (minutes)" required />
        </div>
        <div class="form-group">
          <input type="file" class="form-control" @change="selectJSONFile" accept=".json" required />
        </div>
        <button type="submit" class="btn" :disabled="uploadingJSON" style="width: 100%;">
          {{ uploadingJSON ? '🔄 Processing...' : '📤 Upload JSON' }}
        </button>
      </form>
      
      <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
        <h4 style="color: #333; margin-bottom: 16px;">📝 JSON Format Example:</h4>
        <pre style="background: #2d3748; color: #e2e8f0; padding: 16px; border-radius: 6px; overflow-x: auto; font-size: 12px;">{{ jsonExample }}</pre>
        <p style="margin-top: 12px; color: #666; font-size: 14px;">
          💾 Use the <code>sample_questions.json</code> file in the project root as a template.
        </p>
      </div>
    </div>
    
    <!-- Existing Tests Section -->
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2 style="color: #667eea; margin: 0;">📈 Existing Tests</h2>
        <router-link to="/manage" class="btn" style="text-decoration: none;">
          📋 Manage Tests
        </router-link>
      </div>
      
      <div v-if="tests.length === 0" class="alert alert-warning">
        📄 No tests created yet. Upload a JSON file to create your first test.
      </div>
      <div v-else class="analysis-grid">
        <div v-for="test in tests" :key="test.id" class="stat-card">
          <h3 style="color: #333; margin-bottom: 12px;">{{ test.title }}</h3>
          <div class="stat-number" style="font-size: 24px;">{{ test.question_count }}</div>
          <p style="margin: 8px 0;">Questions</p>
          <p style="color: #666; font-size: 14px;">
            ⏱️ {{ test.duration }} minutes<br>
            📅 {{ new Date(test.created_at).toLocaleDateString() }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from '../config.js'

export default {
  data() {
    return {
      testTitle: '',
      duration: 60,
      selectedFile: null,
      uploading: false,
      jsonTestTitle: '',
      jsonDuration: 60,
      selectedJSONFile: null,
      uploadingJSON: false,
      aiAvailable: false,
      tests: [],
      jsonExample: `[
  {
    "question": "What is the capital of India?",
    "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"],
    "correct_answers": [1],
    "explanation": "Delhi is the capital of India.",
    "type": "MCQ"
  }
]`
    }
  },
  async mounted() {
    await this.checkAIStatus()
    await this.loadTests()
  },
  methods: {
    async checkAIStatus() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/admin/ai-status`)
        this.aiAvailable = response.data.ai_available
      } catch (error) {
        this.aiAvailable = false
      }
    },
    selectFile(event) {
      this.selectedFile = event.target.files[0]
    },
    selectJSONFile(event) {
      this.selectedJSONFile = event.target.files[0]
    },
    async uploadPDF() {
      if (!this.selectedFile) {
        alert('Please select a PDF file')
        return
      }
      
      if (!this.selectedFile.name.toLowerCase().endsWith('.pdf')) {
        alert('Please select a PDF file')
        return
      }
      
      this.uploading = true
      const formData = new FormData()
      formData.append('file', this.selectedFile)
      formData.append('title', this.testTitle)
      formData.append('duration', this.duration)
      
      try {
        const response = await axios.post(`${API_BASE_URL}/api/admin/upload-pdf`, formData)
        alert(`Success! ${response.data.message}`)
        this.testTitle = ''
        this.duration = 60
        this.selectedFile = null
        await this.loadTests()
      } catch (error) {
        alert('Error: ' + (error.response?.data?.error || 'Upload failed'))
      } finally {
        this.uploading = false
      }
    },
    async uploadJSON() {
      if (!this.selectedJSONFile) return
      
      this.uploadingJSON = true
      const formData = new FormData()
      formData.append('file', this.selectedJSONFile)
      formData.append('title', this.jsonTestTitle)
      formData.append('duration', this.jsonDuration)
      
      try {
        await axios.post(`${API_BASE_URL}/api/admin/upload-json`, formData)
        alert('Test created successfully from JSON!')
        this.jsonTestTitle = ''
        this.jsonDuration = 60
        this.selectedJSONFile = null
        await this.loadTests()
      } catch (error) {
        alert('Error creating test: ' + error.response?.data?.error)
      } finally {
        this.uploadingJSON = false
      }
    },
    async loadTests() {
      const response = await axios.get(`${API_BASE_URL}/api/admin/tests`)
      this.tests = response.data
    }
  }
}
</script>

<style scoped>
code {
  background: #f1f3f4;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}
</style>