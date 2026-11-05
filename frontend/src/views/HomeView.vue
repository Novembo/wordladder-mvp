<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import SetupWizardView from './SetupWizardView.vue'

const auth = useAuthStore()
const showAccountForm = ref(false)
const isRegistering = ref(true)
const username = ref('')
const password = ref('')
const formError = ref('')

async function submitAccountForm() {
  formError.value = ''
  const succeeded = isRegistering.value
    ? await auth.register({ username: username.value, password: password.value })
    : await auth.login({ username: username.value, password: password.value })
  if (succeeded) {
    password.value = ''
    showAccountForm.value = false
  } else {
    formError.value = auth.errorMessage
  }
}

async function logout() {
  await auth.logout()
}
</script>

<template>
  <div class="home-layout">
    <header class="account-bar">
      <div v-if="auth.authenticated" class="account-summary">
        <span>Connecté·e en tant que <strong>{{ auth.username }}</strong></span>
        <button class="btn btn-secondary btn-sm" type="button" :disabled="auth.loading" @click="logout">
          Se déconnecter
        </button>
      </div>
      <button
        v-else
        class="btn btn-secondary btn-sm"
        type="button"
        :aria-expanded="showAccountForm"
        @click="showAccountForm = !showAccountForm"
      >
        {{ showAccountForm ? 'Fermer' : 'Créer un compte / Se connecter' }}
      </button>
    </header>
    <p v-if="auth.errorMessage && !showAccountForm" class="account-error" role="status">
      {{ auth.errorMessage }}
    </p>

    <section v-if="showAccountForm && !auth.authenticated" class="account-panel glass-panel animate-pop" aria-labelledby="account-title">
      <h1 id="account-title">{{ isRegistering ? 'Créer un pseudo' : 'Ravi·e de te revoir !' }}</h1>
      <p class="account-intro">Le compte est facultatif : tu peux aussi jouer en invité.</p>
      <form class="account-form" @submit.prevent="submitAccountForm">
        <label for="account-username">Pseudo</label>
        <input
          id="account-username"
          v-model="username"
          autocomplete="username"
          minlength="3"
          maxlength="20"
          pattern="[A-Za-z0-9_]+"
          required
          aria-describedby="username-help"
        >
        <span id="username-help" class="account-help">3 à 20 caractères : lettres, chiffres et _</span>

        <label for="account-password">Mot de passe</label>
        <input
          id="account-password"
          v-model="password"
          type="password"
          :autocomplete="isRegistering ? 'new-password' : 'current-password'"
          minlength="8"
          maxlength="128"
          required
        >
        <span v-if="isRegistering" class="account-help">Au moins 8 caractères. Sans adresse e-mail, le mot de passe ne pourra pas être récupéré.</span>

        <p v-if="formError" class="account-error" role="alert">{{ formError }}</p>
        <button class="btn btn-primary" type="submit" :disabled="auth.loading">
          {{ auth.loading ? 'Patiente…' : (isRegistering ? 'Créer mon compte' : 'Se connecter') }}
        </button>
      </form>
      <button
        class="account-switch"
        type="button"
        @click="isRegistering = !isRegistering; formError = ''; auth.errorMessage = ''"
      >
        {{ isRegistering ? 'J’ai déjà un compte' : 'Créer un compte' }}
      </button>
    </section>

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
  padding:
    max(1rem, env(safe-area-inset-top))
    max(1rem, env(safe-area-inset-right))
    max(1rem, env(safe-area-inset-bottom))
    max(1rem, env(safe-area-inset-left));
}

.account-bar {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  min-height: 48px;
}

.account-summary {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  flex-wrap: wrap;
  color: var(--text-muted);
}

.account-summary strong {
  color: var(--text-main);
}

.account-panel {
  width: min(100%, 420px);
  padding: 1.5rem;
  margin: 0.5rem 0 1rem;
}

.account-panel h1 {
  font-size: 1.5rem;
}

.account-intro,
.account-help {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-top: 0.4rem;
}

.account-form {
  display: grid;
  gap: 0.55rem;
  margin-top: 1rem;
}

.account-form label {
  font-weight: 700;
  margin-top: 0.5rem;
}

.account-form input {
  width: 100%;
  min-height: 48px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 0.7rem 0.8rem;
  background: var(--bg-secondary);
  color: var(--text-main);
  font: inherit;
}

.account-help {
  margin-top: 0;
}

.account-error {
  color: #fecdd3;
  font-weight: 600;
}

.account-switch {
  display: block;
  border: 0;
  background: transparent;
  color: #a5b4fc;
  text-decoration: underline;
  font: inherit;
  cursor: pointer;
  padding: 0.75rem 0 0;
  min-height: 48px;
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

@media (max-width: 480px) {
  .account-summary {
    align-items: flex-end;
    flex-direction: column;
  }

  .account-panel {
    padding: 1.1rem;
  }
}
</style>
