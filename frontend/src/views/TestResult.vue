<template>
  <div class="container" v-if="result">
    <!-- Score Summary -->
    <div class="score-card">
      <h2>🏆 {{ result.test_title }}</h2>
      <div class="score-number">{{ result.percentage }}%</div>
      <p style="font-size: 18px;">{{ result.score }} out of {{ result.total }} questions correct</p>
      <div class="progress-bar" style="margin: 20px auto; max-width: 300px;">
        <div class="progress-fill" :style="{width: result.percentage + '%'}"></div>
      </div>
    </div>

    <!-- Performance Analysis -->
    <div class="card">
      <h3 style="text-align: center; margin-bottom: 30px;">📈 Performance Analysis</h3>
      <div class="analysis-grid">
        <div class="stat-card">
          <div class="stat-number">{{ result.score }}</div>
          <p>Correct Answers</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ result.total - result.score }}</div>
          <p>Incorrect Answers</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ getGrade() }}</div>
          <p>Grade</p>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ getTimePerQuestion() }}s</div>
          <p>Avg. Time/Question</p>
        </div>
      </div>
    </div>

    <!-- Detailed Question Analysis -->
    <div class="card">
      <h3 style="margin-bottom: 30px;">🔍 Detailed Question Analysis</h3>
      <div v-for="(item, index) in result.results" :key="index" class="question-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <h4 style="color: #333;">Q{{ index + 1 }}. {{ item.question }}</h4>
          <span :class="item.is_correct ? 'btn btn-success' : 'btn btn-danger'" style="padding: 4px 12px; font-size: 12px;">
            {{ item.is_correct ? '✓ Correct' : '✗ Incorrect' }}
          </span>
        </div>
        
        <div class="options" style="margin: 16px 0;">
          <div v-for="option in item.options" :key="option.id" 
               :class="getOptionClass(option, item)" class="option">
            <span v-if="option.is_correct">✓</span>
            <span v-else-if="item.user_answer.includes(option.id)">✗</span>
            <span v-else>○</span>
            {{ option.text }}
          </div>
        </div>
        
        <div class="explanation" v-if="item.explanation">
          <strong>💡 Explanation:</strong> {{ item.explanation }}
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div style="text-align: center; margin: 30px 0;">
      <button class="btn" @click="$router.push('/')" style="margin-right: 16px;">
        🏠 Back to Tests
      </button>
      <button class="btn btn-secondary" @click="retakeTest()">
        🔄 Retake Test
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return { 
      result: null,
      testDuration: 0
    }
  },
  async mounted() {
    const response = await axios.get(`http://localhost:5000/api/test/result/${this.$route.params.id}`)
    this.result = response.data
    // Get test duration for time calculation
    const testResponse = await axios.get(`http://localhost:5000/api/admin/tests`)
    const test = testResponse.data.find(t => t.id === this.result.test_id)
    this.testDuration = test ? test.duration : 30
  },
  methods: {
    getOptionClass(option, item) {
      if (option.is_correct) return 'correct'
      if (item.user_answer.includes(option.id)) return 'incorrect'
      return ''
    },
    getGrade() {
      const percentage = this.result.percentage
      if (percentage >= 90) return 'A+'
      if (percentage >= 80) return 'A'
      if (percentage >= 70) return 'B+'
      if (percentage >= 60) return 'B'
      if (percentage >= 50) return 'C'
      return 'F'
    },
    getTimePerQuestion() {
      return Math.round((this.testDuration * 60) / this.result.total)
    },
    retakeTest() {
      // Navigate back to test list or specific test
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
/* Additional specific styles for test results */
</style>