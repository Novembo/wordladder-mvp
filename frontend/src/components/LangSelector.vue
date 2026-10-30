<script setup>
const props = defineProps({
  modelLang: {
    type: String,
    default: 'fr'
  },
  modelLevel: {
    type: String,
    default: 'basic'
  }
})

const emit = defineEmits(['update:modelLang', 'update:modelLevel'])

const languages = [
  { code: 'fr', label: 'Français', flag: '🇫🇷' },
  { code: 'en', label: 'English', flag: '🇬🇧' },
  { code: 'es', label: 'Español', flag: '🇪🇸' }
]

const levels = [
  { code: 'basic', label: 'Débutant', time: '60s', desc: 'Mots simples (3-4 lettres)' },
  { code: 'intermediate', label: 'Intermédiaire', time: '40s', desc: 'Mots moyens (5 lettres)' },
  { code: 'advanced', label: 'Expert', time: '20s', desc: 'Mots riches (6+ lettres)' }
]
</script>

<template>
  <div class="selector-box">
    <!-- Language Selection -->
    <div class="section-group">
      <label class="group-label">Langue du vocabulaire</label>
      <div class="pills-grid">
        <button
          v-for="l in languages"
          :key="l.code"
          type="button"
          class="pill-btn"
          :class="{ selected: modelLang === l.code }"
          @click="emit('update:modelLang', l.code)"
        >
          <span class="flag-icon">{{ l.flag }}</span>
          <span class="pill-label">{{ l.label }}</span>
        </button>
      </div>
    </div>

    <!-- Difficulty Selection -->
    <div class="section-group">
      <label class="group-label">Niveau de difficulté</label>
      <div class="levels-grid">
        <button
          v-for="lvl in levels"
          :key="lvl.code"
          type="button"
          class="level-card"
          :class="{ selected: modelLevel === lvl.code }"
          @click="emit('update:modelLevel', lvl.code)"
        >
          <div class="level-top">
            <span class="level-name">{{ lvl.label }}</span>
            <span class="level-badge">{{ lvl.time }}</span>
          </div>
          <div class="level-desc">{{ lvl.desc }}</div>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.selector-box {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.section-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.group-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.pill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-main);
  font-family: var(--font-main);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pill-btn:hover {
  background: rgba(51, 65, 85, 0.8);
  border-color: rgba(255, 255, 255, 0.15);
}

.pill-btn.selected {
  background: rgba(99, 102, 241, 0.2);
  border-color: var(--accent-primary);
  color: #fff;
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
}

.flag-icon {
  font-size: 1.2rem;
}

.levels-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.level-card {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.85rem;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.level-card:hover {
  background: rgba(51, 65, 85, 0.8);
}

.level-card.selected {
  background: rgba(6, 182, 212, 0.12);
  border-color: var(--accent-secondary);
  box-shadow: 0 0 15px rgba(6, 182, 212, 0.25);
}

.level-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.level-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-main);
}

.level-badge {
  font-size: 0.75rem;
  font-family: var(--font-mono);
  font-weight: 600;
  background: rgba(255, 255, 255, 0.08);
  padding: 0.15rem 0.4rem;
  border-radius: var(--radius-sm);
  color: var(--accent-secondary);
}

.level-desc {
  font-size: 0.75rem;
  color: var(--text-dim);
}

@media (max-width: 640px) {
  .levels-grid {
    grid-template-columns: 1fr;
  }
}
</style>

