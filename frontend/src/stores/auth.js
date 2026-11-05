import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE = '/v1/auth'

export const useAuthStore = defineStore('auth', () => {
  const guestUsername = localStorage.getItem('wl_username') || 'Joueur'
  const username = ref(guestUsername)
  const userId = ref(null)
  const authenticated = ref(false)
  const csrfToken = ref('')
  const preferredLang = ref(localStorage.getItem('wl_lang') || 'fr')
  const preferredLevel = ref(localStorage.getItem('wl_level') || 'basic')
  const errorMessage = ref('')
  const loading = ref(false)
  const ready = ref(false)
  let initialization = null

  function applyUser(user) {
    username.value = user.username
    userId.value = user.id
    csrfToken.value = user.csrf_token
    authenticated.value = true
  }

  function clearUser() {
    username.value = guestUsername
    userId.value = null
    csrfToken.value = ''
    authenticated.value = false
  }

  function initialize() {
    if (initialization) return initialization
    initialization = (async () => {
      try {
        const response = await fetch(`${API_BASE}/me`, { credentials: 'same-origin' })
        if (response.status === 401) {
          clearUser()
          return
        }
        if (!response.ok) throw new Error('Impossible de vérifier la session')
        applyUser(await response.json())
      } catch (error) {
        errorMessage.value = error instanceof Error ? error.message : 'Erreur de connexion'
      } finally {
        ready.value = true
      }
    })()
    return initialization
  }

  async function submitCredentials(action, credentials) {
    await initialize()
    loading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/${action}`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'La demande a échoué')
      }
      applyUser(data)
      return true
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'Erreur de connexion'
      return false
    } finally {
      loading.value = false
    }
  }

  function register(credentials) {
    return submitCredentials('register', credentials)
  }

  function login(credentials) {
    return submitCredentials('login', credentials)
  }

  async function logout() {
    loading.value = true
    errorMessage.value = ''
    try {
      const response = await fetch(`${API_BASE}/logout`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'X-CSRF-Token': csrfToken.value },
      })
      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Impossible de fermer la session')
      }
      clearUser()
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'Erreur de connexion'
    } finally {
      loading.value = false
    }
  }

  function setUsername(name) {
    username.value = name || 'Joueur'
    localStorage.setItem('wl_username', username.value)
  }

  function setPreferences(lang, level) {
    preferredLang.value = lang
    preferredLevel.value = level
    localStorage.setItem('wl_lang', lang)
    localStorage.setItem('wl_level', level)
  }

  return {
    username,
    userId,
    authenticated,
    csrfToken,
    preferredLang,
    preferredLevel,
    errorMessage,
    loading,
    ready,
    initialize,
    register,
    login,
    logout,
    setUsername,
    setPreferences,
  }
})
