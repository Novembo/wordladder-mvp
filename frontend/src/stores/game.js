import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

const API_BASE = '/v1'

export const useGameStore = defineStore('game', () => {
  const matchId = ref(null)
  const lang = ref('fr')
  const level = ref('basic')
  const mode = ref('solo')
  const part = ref(1)
  const scores = ref([0, 0])
  const lives = ref([3, 3])
  const wordLength = ref(4)
  const currentWord = ref('')
  const wordHistory = ref([])
  const toMove = ref(0)
  const timeLimit = ref(80)
  const usedCount = ref(0)
  const finished = ref(false)
  const winner = ref(null)
  const lastEvent = ref('')

  const currentHint = ref(null)
  const loading = ref(false)
  const errorMessage = ref('')
  const shakeInput = ref(false)

  const isMyTurn = computed(() => {
    if (finished.value) return false
    if (mode.value === 'solo') {
      return toMove.value === 0
    }
    return true
  })

  const currentPlayerLabel = computed(() => {
    if (mode.value === 'solo') {
      return toMove.value === 0 ? 'À toi de jouer !' : 'Robot Antigravity réfléchit...'
    }
    return toMove.value === 0 ? 'Tour de Joueur 1' : 'Tour de Joueur 2'
  })

  function triggerError(msg) {
    errorMessage.value = msg
    shakeInput.value = true
    setTimeout(() => {
      shakeInput.value = false
    }, 600)
  }

  function clearError() {
    errorMessage.value = ''
  }

  function clearHint() {
    currentHint.value = null
  }

  async function createMatch(selectedLang, selectedLevel, selectedMode) {
    loading.value = true
    clearError()
    clearHint()
    wordHistory.value = []

    try {
      const auth = useAuthStore()
      await auth.initialize()
      lang.value = selectedLang
      level.value = selectedLevel
      mode.value = selectedMode

      const res = await fetch(`${API_BASE}/matches`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(auth.csrfToken ? { 'X-CSRF-Token': auth.csrfToken } : {}),
        },
        body: JSON.stringify({
          lang: selectedLang,
          level: selectedLevel,
          mode: selectedMode,
          play_all_parts: false
        })
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail?.message || 'Erreur lors de la création du match')
      }

      const data = await res.json()
      applyState(data)
      if (data.current_word) {
        wordHistory.value.push({ word: data.current_word, player: -1 })
      }
      return data
    } catch (e) {
      triggerError(e.message)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function playMove(word) {
    if (!matchId.value || finished.value) return false
    loading.value = true
    clearError()
    clearHint()

    const activePlayer = toMove.value
    const cleaned = word.trim().toLowerCase()

    try {
      const res = await fetch(`${API_BASE}/matches/${matchId.value}/moves`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(useAuthStore().csrfToken ? { 'X-CSRF-Token': useAuthStore().csrfToken } : {}),
        },
        body: JSON.stringify({
          player: activePlayer,
          word: cleaned
        })
      })

      const data = await res.json()

      if (!res.ok) {
        const msg = data.detail?.message || 'Coup invalide'
        triggerError(msg)
        return false
      }

      wordHistory.value.push({ word: cleaned, player: activePlayer })
      applyState(data)

      if (mode.value === 'solo' && data.current_word && data.current_word !== cleaned) {
        wordHistory.value.push({ word: data.current_word, player: 1 })
      }

      return true
    } catch (e) {
      triggerError(e.message)
      return false
    } finally {
      loading.value = false
    }
  }

  async function handleTimeout() {
    if (!matchId.value || finished.value) return
    clearError()

    try {
      const res = await fetch(`${API_BASE}/matches/${matchId.value}/timeout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(useAuthStore().csrfToken ? { 'X-CSRF-Token': useAuthStore().csrfToken } : {}),
        },
        body: JSON.stringify({ player: toMove.value })
      })

      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail?.message || 'Impossible de déclarer la fin du temps')
      }

      applyState(data)
      if (data.current_word && !data.finished && data.event.includes('part_')) {
        wordHistory.value.push({ word: data.current_word, player: -1 })
      }
    } catch (e) {
      triggerError(e instanceof Error ? e.message : 'Impossible de déclarer la fin du temps')
    }
  }

  async function requestHint() {
    if (!matchId.value || finished.value) return null
    try {
      const res = await fetch(`${API_BASE}/matches/${matchId.value}/hint`, {
        method: 'POST'
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail?.message || 'Impossible de récupérer un indice')
      }

      currentHint.value = data
      return data
    } catch (e) {
      triggerError(e instanceof Error ? e.message : 'Impossible de récupérer un indice')
      return null
    }
  }

  function applyState(data) {
    matchId.value = data.match_id
    part.value = data.part
    scores.value = [...data.scores]
    lives.value = data.lives ? [...data.lives] : [3, 3]
    wordLength.value = data.word_length || (data.current_word ? data.current_word.length : 4)
    currentWord.value = data.current_word
    toMove.value = data.to_move
    timeLimit.value = data.time_limit
    usedCount.value = data.used_count
    finished.value = data.finished
    winner.value = data.winner
    lastEvent.value = data.event
  }

  function reset() {
    matchId.value = null
    wordHistory.value = []
    finished.value = false
    winner.value = null
    errorMessage.value = ''
    currentHint.value = null
    scores.value = [0, 0]
    lives.value = [3, 3]
  }

  return {
    matchId,
    lang,
    level,
    mode,
    part,
    scores,
    lives,
    wordLength,
    currentWord,
    wordHistory,
    toMove,
    timeLimit,
    usedCount,
    finished,
    winner,
    lastEvent,
    currentHint,
    loading,
    errorMessage,
    shakeInput,
    isMyTurn,
    currentPlayerLabel,
    createMatch,
    playMove,
    handleTimeout,
    requestHint,
    clearHint,
    clearError,
    triggerError,
    reset,
  }
})
