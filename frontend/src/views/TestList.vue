<template>
  <div class="container">
    <div class="card">
      <h1 style="text-align: center; color: #333; margin-bottom: 30px;">🏆 Current Affairs Mock Tests</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="tests.length === 0" class="alert alert-warning">
        ⚠️ No tests available. Please contact admin to add tests.
      </div>
      
      <div v-else class="analysis-grid">
        <div v-for="test in tests" :key="test.id" class="card">
          <h3 style="color: #667eea; margin-bottom: 16px;">📝 {{ test.title }}</h3>
          <div style="margin-bottom: 20px;">
            <p><strong>⏱️ Duration:</strong> {{ test.duration }} minutes</p>
            <p><strong>❓ Questions:</strong> {{ test.question_count }}</p>
            <p><strong>🎯 Difficulty:</strong> <span class="badge">{{ getDifficulty(test.question_count) }}</span></p>
          </div>
          <button class="btn" @click="startTest(test.id)" style="width: 100%;">
            🚀 Start Test
          </button>
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
      tests: [],
      loading: true
    }
  },
  async mounted() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/test/available`)
      this.tests = response.data
    } catch (error) {
      console.error('Error loading tests:', error)
    } finally {
      this.loading = false
    }
  },
  methods: {
    startTest(testId) {
      const userName = prompt('👤 Enter your name to start the test:')
      if (userName && userName.trim()) {
        this.$router.push(`/test/${testId}?name=${encodeURIComponent(userName.trim())}`)
      }
    },
    getDifficulty(questionCount) {
      if (questionCount <= 5) return 'Easy'
      if (questionCount <= 10) return 'Medium'
      return 'Hard'
    }
  }
}
</script>

<style scoped>
.badge {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}
</style>