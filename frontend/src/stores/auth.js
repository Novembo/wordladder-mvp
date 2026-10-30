import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const username = ref(localStorage.getItem('wl_username') || 'Joueur')
  const preferredLang = ref(localStorage.getItem('wl_lang') || 'fr')
  const preferredLevel = ref(localStorage.getItem('wl_level') || 'basic')

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
    preferredLang,
    preferredLevel,
    setUsername,
    setPreferences,
  }
})

