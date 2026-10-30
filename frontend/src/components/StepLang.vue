<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: 'fr'
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

const languages = [
  {
    code: 'fr',
    label: 'Français',
    flag: '🇫🇷',
    motto: 'Mots & trésors de la langue française',
    sample: 'CHAT ➔ CHAR ➔ CHER'
  },
  {
    code: 'en',
    label: 'English',
    flag: '🇬🇧',
    motto: 'Learn and climb the English word ladder',
    sample: 'COLD ➔ CORD ➔ CARD'
  },
  {
    code: 'es',
    label: 'Español',
    flag: '🇪🇸',
    motto: '¡Descubre y juega en español!',
    sample: 'CASA ➔ CAMA ➔ CARA'
  }
]
</script>

<template>
  <div class="step-card glass-panel animate-pop">
    <div class="step-header">
      <span class="step-badge">Étape 2 sur 3</span>
      <h2 class="step-title">Dans quelle langue jouer ?</h2>
      <p class="step-sub">Choisis la langue de ton dictionnaire pour cette partie.</p>
    </div>

    <div class="langs-list">
      <div
        v-for="l in languages"
        :key="l.code"
        class="lang-choice-card"
        :class="{ active: modelValue === l.code }"
        @click="emit('update:modelValue', l.code)"
      >
        <div class="lang-flag">{{ l.flag }}</div>
        <div class="lang-body">
          <div class="lang-title-row">
            <h3 class="lang-name">{{ l.label }}</h3>
            <span class="sample-pill font-mono">{{ l.sample }}</span>
          </div>
          <p class="lang-motto">{{ l.motto }}</p>
        </div>
        <div class="choice-radio" :class="{ checked: modelValue === l.code }">
          ✓
        </div>
      </div>
    </div>

    <div class="step-actions">
      <button type="button" class="btn btn-secondary" @click="emit('back')">
        ← Retour au mode
      </button>
      <button type="button" class="btn btn-primary" @click="emit('next')">
        Continuer vers le défi →
      </button>
    </div>
  </div>
</template>

<style scoped>
.step-card {
  max-width: 600px;
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
  color: var(--accent-secondary);
  background: rgba(6, 182, 212, 0.15);
  border: 1px solid rgba(6, 182, 212, 0.3);
  padding: 0.25rem 0.85rem;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.step-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.step-sub {
  color: var(--text-muted);
  font-size: 1rem;
}

.langs-list {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.lang-choice-card {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  padding: 1.15rem;
  background: rgba(30, 41, 59, 0.6);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 0 rgba(0, 0, 0, 0.25);
}

.lang-choice-card:hover {
  background: rgba(51, 65, 85, 0.85);
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.lang-choice-card.active {
  background: rgba(6, 182, 212, 0.15);
  border-color: var(--accent-secondary);
  box-shadow: 0 5px 0 var(--accent-secondary-shadow);
  transform: translateY(-3px);
}

.lang-flag {
  font-size: 2.4rem;
  line-height: 1;
}

.lang-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.lang-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.lang-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
}

.sample-pill {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.08);
  color: #a5f3fc;
}

.lang-motto {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.choice-radio {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  border: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.9rem;
  color: transparent;
  transition: all 0.2s ease;
}

.choice-radio.checked {
  background: var(--accent-success);
  border-color: var(--accent-success);
  color: #fff;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

.step-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 0.5rem;
}

@media (max-width: 600px) {
  .step-actions {
    flex-direction: column-reverse;
  }
}
</style>

