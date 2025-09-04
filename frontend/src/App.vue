<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-links">
        <router-link to="/">📚 Tests</router-link>
        <router-link to="/admin">⚙️ Admin</router-link>
        <router-link to="/manage">📋 Manage</router-link>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
import './style.css'
export default {
  name: 'App'
}
</script>