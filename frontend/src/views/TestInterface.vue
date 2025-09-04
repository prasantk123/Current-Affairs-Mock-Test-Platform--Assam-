<template>
  <div class="container" v-if="test">
    <!-- Header with Timer -->
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
          <h2 style="color: #333; margin: 0;">📝 {{ test.title }}</h2>
          <p style="color: #666; margin: 8px 0 0 0;">Question {{ currentQuestionIndex + 1 }} of {{ test.questions.length }}</p>
        </div>
        <div class="timer">{{ formatTime(timeLeft) }}</div>
      </div>
      
      <!-- Progress Bar -->
      <div class="progress-bar">
        <div class="progress-fill" :style="{width: ((currentQuestionIndex + 1) / test.questions.length) * 100 + '%'}"></div>
      </div>
    </div>
    
    <!-- Question Card -->
    <div class="card" v-if="currentQuestion">
      <div class="question-card">
        <h3 style="color: #333; margin-bottom: 24px; line-height: 1.6;">
          Q{{ currentQuestionIndex + 1 }}. {{ currentQuestion.question }}
        </h3>
        
        <div class="alert alert-info" v-if="currentQuestion.type === 'MSQ'" style="margin-bottom: 20px;">
          📝 <strong>Note:</strong> This is a multiple select question. You can choose more than one answer.
        </div>
        
        <div class="options">
          <div v-for="option in currentQuestion.options" :key="option.id" 
               class="option" 
               :class="{selected: isSelected(option.id)}"
               @click="selectOption(option.id)">
            <input 
              :type="currentQuestion.type === 'MCQ' ? 'radio' : 'checkbox'"
              :name="'q' + currentQuestion.id"
              :value="option.id"
              :checked="isSelected(option.id)"
              style="margin-right: 12px;"
            />
            {{ option.text }}
          </div>
        </div>
      </div>
      
      <!-- Navigation -->
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 30px;">
        <button class="btn btn-secondary" @click="previousQuestion" :disabled="currentQuestionIndex === 0">
          ← Previous
        </button>
        
        <div style="display: flex; gap: 12px;">
          <span v-for="(q, index) in test.questions" :key="index" 
                :class="getQuestionStatus(index)"
                @click="goToQuestion(index)"
                style="width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-weight: bold;">
            {{ index + 1 }}
          </span>
        </div>
        
        <button class="btn" @click="nextQuestion" v-if="currentQuestionIndex < test.questions.length - 1">
          Next →
        </button>
        <button class="btn btn-success" @click="confirmSubmit" v-else>
          📤 Submit Test
        </button>
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
      test: null,
      currentQuestionIndex: 0,
      answers: {},
      timeLeft: 0,
      timer: null,
      userName: ''
    }
  },
  computed: {
    currentQuestion() {
      return this.test?.questions[this.currentQuestionIndex]
    }
  },
  async mounted() {
    this.userName = this.$route.query.name
    const response = await axios.get(`http://localhost:5000/api/test/${this.$route.params.id}/start`)
    this.test = response.data
    this.timeLeft = this.test.duration * 60
    this.startTimer()
  },
  methods: {
    startTimer() {
      this.timer = setInterval(() => {
        this.timeLeft--
        if (this.timeLeft <= 0) {
          this.submitTest()
        }
      }, 1000)
    },
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins}:${secs.toString().padStart(2, '0')}`
    },
    selectOption(optionId) {
      const questionId = this.currentQuestion.id
      if (this.currentQuestion.type === 'MCQ') {
        this.answers[questionId] = [optionId]
      } else {
        if (!this.answers[questionId]) this.answers[questionId] = []
        const index = this.answers[questionId].indexOf(optionId)
        if (index > -1) {
          this.answers[questionId].splice(index, 1)
        } else {
          this.answers[questionId].push(optionId)
        }
      }
    },
    isSelected(optionId) {
      const questionId = this.currentQuestion.id
      return this.answers[questionId] && this.answers[questionId].includes(optionId)
    },
    getQuestionStatus(index) {
      const questionId = this.test.questions[index].id
      const isAnswered = this.answers[questionId] && this.answers[questionId].length > 0
      const isCurrent = index === this.currentQuestionIndex
      
      if (isCurrent) return 'btn btn-primary'
      if (isAnswered) return 'btn btn-success'
      return 'btn btn-secondary'
    },
    goToQuestion(index) {
      this.currentQuestionIndex = index
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.test.questions.length - 1) {
        this.currentQuestionIndex++
      }
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },
    confirmSubmit() {
      const unanswered = this.test.questions.filter((q, index) => {
        return !this.answers[q.id] || this.answers[q.id].length === 0
      }).length
      
      let message = `Are you sure you want to submit the test?`
      if (unanswered > 0) {
        message += `\n\n⚠️ You have ${unanswered} unanswered questions.`
      }
      
      if (confirm(message)) {
        this.submitTest()
      }
    },
    async submitTest() {
      clearInterval(this.timer)
      try {
        const response = await axios.post(`${API_BASE_URL}/api/test/submit`, {
          test_id: this.test.test_id,
          user_name: this.userName,
          answers: this.answers
        })
        this.$router.push(`/result/${response.data.attempt_id}`)
      } catch (error) {
        alert('Error submitting test. Please try again.')
        console.error(error)
      }
    }
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer)
  }
}
</script>

<style scoped>
.alert-info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}
</style>