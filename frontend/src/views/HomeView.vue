<script setup>
import SetupWizardView from './SetupWizardView.vue'
</script>

<template>
  <div class="home-layout">
    <SetupWizardView />

    <footer class="home-bottom-nav">
      <router-link to="/leaderboard" class="btn btn-secondary btn-sm">
        🏆 Panthéon des Champions
      </router-link>
    </footer>
  </div>
</template>

<style scoped>
.home-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.home-bottom-nav {
  padding: 1rem 0 2rem;
  display: flex;
  justify-content: center;
}

.btn-sm {
  font-size: 0.95rem;
  padding: 0.55rem 1.4rem;
}
</style>
