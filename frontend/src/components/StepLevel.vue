<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: 'basic'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'back'])

const levels = [
  {
    id: 'basic',
    name: 'Apprenti',
    badge: 'Niveau Débutant',
    icon: '🟢',
    letters: '3 à 4 lettres',
    time: '80 secondes',
    desc: 'Idéal pour s’entraîner et découvrir le jeu en douceur avec un chrono détendu !',
    colorClass: 'level-green'
  },
  {
    id: 'intermediate',
    name: 'Aventurier',
    badge: 'Niveau Équilibré',
    icon: '🟡',
    letters: '5 lettres',
    time: '60 secondes',
    desc: 'Pour les explorateurs des mots qui aiment un peu de défi et de vivacité.',
    colorClass: 'level-yellow'
  },
  {
    id: 'advanced',
    name: 'Champion',
    badge: 'Grand Défi',
    icon: '🔴',
    letters: '6+ lettres',
    time: '40 secondes',
    desc: 'Pour les as du dictionnaire : mots plus longs et chrono rapide !',
    colorClass: 'level-red'
  }
]
</script>

<template>
  <div class="step-card glass-panel animate-pop">
    <div class="step-header">
      <span class="step-badge">Étape 3 sur 3</span>
      <h2 class="step-title">Choisis ton défi</h2>
      <p class="step-sub">Sélectionne la difficulté et le temps accordé à chaque tour.</p>
    </div>

    <div class="levels-list" role="group" aria-label="Niveau de difficulté">
      <button
        v-for="lvl in levels"
        :key="lvl.id"
        type="button"
        class="level-card"
        :class="[lvl.colorClass, { active: modelValue === lvl.id }]"
        :aria-pressed="modelValue === lvl.id"
        @click="emit('update:modelValue', lvl.id)"
      >
        <span class="level-icon-wrap">
          <span class="level-emoji">{{ lvl.icon }}</span>
        </span>

        <span class="level-body">
          <span class="level-top-row">
            <span class="level-name" role="heading" aria-level="3">{{ lvl.name }}</span>
            <span class="level-time-pill">⏱️ {{ lvl.time }}</span>
          </span>
          <span class="level-meta">
            <span class="level-letters-tag">📏 {{ lvl.letters }}</span>
            <span class="level-desc">{{ lvl.desc }}</span>
          </span>
        </span>

        <span class="choice-radio" :class="{ checked: modelValue === lvl.id }" aria-hidden="true">
          ✓
        </span>
      </button>
    </div>

    <div class="step-actions">
      <button type="button" class="btn btn-secondary" :disabled="loading" @click="emit('back')">
        ← Retour à la langue
      </button>
      <button
        type="button"
        class="btn btn-success btn-launch"
        :disabled="loading"
        @click="emit('submit')"
      >
        <span v-if="loading">Préparation du jeu...</span>
        <span v-else>C'est parti ! 🎮</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.step-card {
  max-width: 620px;
  width: 100%;
  margin: 0 auto;
  padding: 2.25rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.step-header {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-badge {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--accent-gold);
  background: rgba(251, 191, 36, 0.15);
  border: 1px solid rgba(251, 191, 36, 0.3);
  padding: 0.25rem 0.85rem;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.step-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-main);
}

.step-sub {
  font-size: 0.95rem;
  color: var(--text-muted);
}

.levels-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.level-card {
  display: flex;
  align-items: center;
  gap: 1.1rem;
  padding: 1.15rem 1.25rem;
  background: rgba(255, 255, 255, 0.03);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  color: inherit;
  font: inherit;
  text-align: left;
  width: 100%;
  transition: var(--motion-interactive);
  position: relative;
  user-select: none;
}

.level-card:hover {
  background: rgba(255, 255, 255, 0.06);
  transform: translateY(-2px);
}

.level-card.active {
  border-color: var(--accent-success);
  background: rgba(16, 185, 129, 0.1);
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
}

.level-card:focus-visible {
  outline-offset: 4px;
}

.level-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.level-body {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.level-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.level-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-main);
}

.level-time-pill {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.08);
  color: var(--accent-secondary);
}

.level-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.level-letters-tag {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--accent-gold);
}

.level-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.choice-radio {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  border: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: transparent;
  font-size: 0.9rem;
  font-weight: 800;
  flex-shrink: 0;
  transition: var(--motion-interactive);
}

.choice-radio.checked {
  background: var(--accent-success);
  border-color: var(--accent-success);
  color: #fff;
}

.step-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.btn-launch {
  flex: 1;
}

@media (max-width: 520px) {
  .step-card {
    padding: 1.5rem 1rem;
    gap: 1.25rem;
  }

  .step-actions {
    flex-direction: column-reverse;
  }
  .btn {
    width: 100%;
  }
}

@media (max-width: 380px) {
  .level-card {
    display: grid;
    grid-template-columns: 2.5rem minmax(0, 1fr) 1.75rem;
    gap: 0.5rem;
    padding: 0.75rem;
    align-items: start;
  }

  .level-icon-wrap {
    width: 2.5rem;
    height: 2.5rem;
  }

  .level-body {
    display: contents;
  }

  .level-top-row {
    grid-column: 2;
    grid-row: 1;
    align-content: center;
  }

  .level-meta {
    grid-column: 1 / -1;
    grid-row: 2;
  }

  .choice-radio {
    grid-column: 3;
    grid-row: 1;
    align-self: center;
  }
}
</style>
