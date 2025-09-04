<template>
  <div class="container">
    <div class="card">
      <h2 style="color: #667eea; margin-bottom: 20px;">📝 Test Manager</h2>
      
      <div v-if="selectedTest">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h3>{{ selectedTest.title }} - Questions</h3>
          <button class="btn btn-secondary" @click="selectedTest = null">← Back to Tests</button>
        </div>
        
        <div v-for="(question, index) in questions" :key="question.id" class="card" style="margin: 16px 0;">
          <div style="display: flex; justify-content: between; align-items: start;">
            <div style="flex: 1;">
              <h4>Q{{ index + 1 }}. {{ question.question_text }}</h4>
              <p><strong>Type:</strong> {{ question.question_type }}</p>
              
              <div style="margin: 12px 0;">
                <div v-for="option in question.options" :key="option.id" 
                     :class="option.is_correct ? 'option correct' : 'option'">
                  {{ option.is_correct ? '✓' : '○' }} {{ option.text }}
                </div>
              </div>
              
              <div v-if="question.explanation" class="explanation">
                <strong>💡 Explanation:</strong> {{ question.explanation }}
              </div>
            </div>
            
            <div style="display: flex; gap: 8px;">
              <button class="btn btn-secondary" @click="editQuestion(question)" style="padding: 6px 12px; font-size: 12px;">
                ✏️ Edit
              </button>
              <button class="btn btn-danger" @click="deleteQuestion(question.id)" style="padding: 6px 12px; font-size: 12px;">
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else>
        <div class="analysis-grid">
          <div v-for="test in tests" :key="test.id" class="card">
            <h3 style="color: #333; margin-bottom: 12px;">{{ test.title }}</h3>
            <p>📝 {{ test.question_count }} questions</p>
            <p>⏱️ {{ test.duration }} minutes</p>
            <p style="font-size: 12px; color: #666;">📅 {{ new Date(test.created_at).toLocaleDateString() }}</p>
            
            <div style="display: flex; gap: 8px; margin-top: 16px;">
              <button class="btn" @click="viewQuestions(test)" style="flex: 1; font-size: 12px;">
                👁️ View Questions
              </button>
              <button class="btn btn-danger" @click="deleteTest(test.id)" style="padding: 8px; font-size: 12px;">
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Edit Question Modal -->
    <div v-if="editingQuestion" class="modal-overlay" @click="closeEdit">
      <div class="modal-content" @click.stop>
        <h3>Edit Question</h3>
        <form @submit.prevent="saveQuestion">
          <div class="form-group">
            <label>Question Text:</label>
            <textarea v-model="editingQuestion.question_text" class="form-control" rows="3" required></textarea>
          </div>
          
          <div class="form-group">
            <label>Type:</label>
            <select v-model="editingQuestion.question_type" class="form-control" required>
              <option value="MCQ">MCQ (Single Correct)</option>
              <option value="MSQ">MSQ (Multiple Correct)</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Options:</label>
            <div v-for="(option, index) in editingQuestion.options" :key="index" style="display: flex; gap: 8px; margin: 8px 0;">
              <input v-model="option.text" class="form-control" placeholder="Option text" required>
              <label style="display: flex; align-items: center; gap: 4px;">
                <input type="checkbox" v-model="option.is_correct">
                Correct
              </label>
              <button type="button" class="btn btn-danger" @click="removeOption(index)" style="padding: 4px 8px;">×</button>
            </div>
            <button type="button" class="btn btn-secondary" @click="addOption">+ Add Option</button>
          </div>
          
          <div class="form-group">
            <label>Explanation:</label>
            <textarea v-model="editingQuestion.explanation" class="form-control" rows="2"></textarea>
          </div>
          
          <div style="display: flex; gap: 12px; justify-content: end;">
            <button type="button" class="btn btn-secondary" @click="closeEdit">Cancel</button>
            <button type="submit" class="btn">Save Changes</button>
          </div>
        </form>
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
      tests: [],
      selectedTest: null,
      questions: [],
      editingQuestion: null
    }
  },
  async mounted() {
    await this.loadTests()
  },
  methods: {
    async loadTests() {
      const response = await axios.get(`${API_BASE_URL}/api/admin/tests`)
      this.tests = response.data
    },
    
    async viewQuestions(test) {
      this.selectedTest = test
      const response = await axios.get(`http://localhost:5000/api/admin/tests/${test.id}/questions`)
      this.questions = response.data.questions
    },
    
    async deleteTest(testId) {
      if (confirm('Are you sure you want to delete this test? This will delete all questions.')) {
        await axios.delete(`http://localhost:5000/api/admin/tests/${testId}`)
        await this.loadTests()
      }
    },
    
    async deleteQuestion(questionId) {
      if (confirm('Are you sure you want to delete this question?')) {
        await axios.delete(`http://localhost:5000/api/admin/questions/${questionId}`)
        await this.viewQuestions(this.selectedTest)
      }
    },
    
    editQuestion(question) {
      this.editingQuestion = JSON.parse(JSON.stringify(question))
    },
    
    closeEdit() {
      this.editingQuestion = null
    },
    
    addOption() {
      this.editingQuestion.options.push({ text: '', is_correct: false })
    },
    
    removeOption(index) {
      this.editingQuestion.options.splice(index, 1)
    },
    
    async saveQuestion() {
      try {
        await axios.put(`http://localhost:5000/api/admin/questions/${this.editingQuestion.id}`, this.editingQuestion)
        await this.viewQuestions(this.selectedTest)
        this.closeEdit()
        alert('Question updated successfully!')
      } catch (error) {
        alert('Error updating question: ' + error.response?.data?.error)
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

label {
  font-weight: 600;
  margin-bottom: 4px;
  display: block;
}
</style>