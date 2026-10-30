<script setup>
import { ref, onMounted } from 'vue'

const activeLang = ref('all')
const entries = ref([])
const loading = ref(false)
const error = ref(null)

const filters = [
  { code: 'all', label: 'Toutes les langues', flag: '🌍' },
  { code: 'fr', label: 'Français', flag: '🇫🇷' },
  { code: 'en', label: 'English', flag: '🇬🇧' },
  { code: 'es', label: 'Español', flag: '🇪🇸' }
]

async function fetchLeaderboard(lang = 'all') {
  activeLang.value = lang
  loading.value = true
  error.value = null

  try {
    const url = lang === 'all' ? '/v1/leaderboard' : `/v1/leaderboard?lang=${lang}`
    const res = await fetch(url)
    if (!res.ok) throw new Error('Impossible de charger le classement')
    entries.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function formatDate(isoStr) {
  if (!isoStr) return '-'
  const d = new Date(isoStr)
  return d.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchLeaderboard('all')
})
</script>

<template>
  <div class="leaderboard-view container">
    <header class="view-header">
      <router-link to="/" class="btn btn-secondary btn-back">
        ← Retour
      </router-link>
      <div class="header-titles">
        <h1 class="view-title">🏆 Tableau d'Honneur</h1>
        <p class="view-sub">Les meilleures séries et parties terminées de Word Ladder</p>
      </div>
    </header>

    <!-- Filters Bar -->
    <div class="filters-bar">
      <button
        v-for="f in filters"
        :key="f.code"
        type="button"
        class="filter-pill"
        :class="{ active: activeLang === f.code }"
        @click="fetchLeaderboard(f.code)"
      >
        <span>{{ f.flag }}</span>
        <span>{{ f.label }}</span>
      </button>
    </div>

    <!-- Table Card -->
    <div class="leaderboard-card glass-panel">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <span>Chargement des records...</span>
      </div>

      <div v-else-if="error" class="error-state">
        {{ error }}
      </div>

      <div v-else-if="entries.length === 0" class="empty-state">
        <span class="empty-icon">🪜</span>
        <p>Aucun match terminé enregistré pour le moment.</p>
        <router-link to="/" class="btn btn-primary btn-sm">
          Sois le premier à jouer !
        </router-link>
      </div>

      <div v-else class="table-responsive">
        <table class="leaderboard-table">
          <thead>
            <tr>
              <th class="th-rank">Rang</th>
              <th>Langue</th>
              <th>Difficulté</th>
              <th>Mode</th>
              <th class="th-center">Mots joués</th>
              <th class="th-center">Score</th>
              <th class="th-right">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in entries" :key="item.match_id" class="table-row">
              <td class="td-rank">
                <span v-if="item.rank === 1" class="rank-badge rank-1">🥇 1</span>
                <span v-else-if="item.rank === 2" class="rank-badge rank-2">🥈 2</span>
                <span v-else-if="item.rank === 3" class="rank-badge rank-3">🥉 3</span>
                <span v-else class="rank-badge rank-other">#{{ item.rank }}</span>
              </td>
              <td>
                <span class="lang-tag">{{ item.lang.toUpperCase() }}</span>
              </td>
              <td class="capitalize">{{ item.level }}</td>
              <td>
                <span class="mode-pill">{{ item.mode }}</span>
              </td>
              <td class="td-center font-mono font-bold">{{ item.total_moves }}</td>
              <td class="td-center font-mono font-bold">
                {{ item.scores ? item.scores.join(' - ') : '-' }}
              </td>
              <td class="td-right text-dim">{{ formatDate(item.finished_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.leaderboard-view {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-top: 2rem;
}

.view-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.btn-back {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.view-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.view-sub {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.filters-bar {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-pill {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  font-family: var(--font-main);
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.5rem 0.9rem;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-pill:hover {
  background: rgba(51, 65, 85, 0.8);
  color: var(--text-main);
}

.filter-pill.active {
  background: rgba(99, 102, 241, 0.2);
  border-color: var(--accent-primary);
  color: #fff;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}

.leaderboard-card {
  padding: 1.5rem;
  min-height: 300px;
}

.loading-state, .empty-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  min-height: 250px;
  color: var(--text-muted);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 2.5rem;
}

.table-responsive {
  overflow-x: auto;
}

.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.leaderboard-table th {
  padding: 0.75rem 1rem;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-dim);
  border-bottom: 1px solid var(--border-color);
}

.leaderboard-table td {
  padding: 0.9rem 1rem;
  font-size: 0.9rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.table-row:hover {
  background: rgba(255, 255, 255, 0.02);
}

.th-center, .td-center {
  text-align: center;
}

.th-right, .td-right {
  text-align: right;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-weight: 700;
  font-size: 0.9rem;
}

.rank-1 { color: #fbbf24; }
.rank-2 { color: #cbd5e1; }
.rank-3 { color: #f97316; }
.rank-other { color: var(--text-dim); font-size: 0.85rem; }

.lang-tag {
  background: rgba(99, 102, 241, 0.15);
  color: var(--accent-primary);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 0.75rem;
}

.mode-pill {
  text-transform: capitalize;
  color: var(--text-muted);
}

.font-mono {
  font-family: var(--font-mono);
}

.font-bold {
  font-weight: 700;
}

.text-dim {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.capitalize {
  text-transform: capitalize;
}
</style>

