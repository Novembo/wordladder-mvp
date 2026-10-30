<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: 'solo'
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])
</script>

<template>
  <div class="step-card glass-panel animate-pop">
    <div class="step-header">
      <span class="step-badge">Étape 1 sur 3</span>
      <h2 class="step-title">Comment veux-tu jouer ?</h2>
      <p class="step-sub">Choisis ton aventure : seul contre l'ordinateur ou en duel d'amis !</p>
    </div>

    <div class="modes-grid">
      <!-- Solo Card -->
      <div
        class="choice-card"
        :class="{ active: modelValue === 'solo' }"
        @click="emit('update:modelValue', 'solo')"
      >
        <div class="choice-icon-wrap bot-gradient">
          <span class="choice-emoji">🤖</span>
        </div>
        <div class="choice-body">
          <h3 class="choice-title">Solo vs Robot</h3>
          <p class="choice-desc">Entraîne-toi tranquillement contre notre robot malicieux Antigravity.</p>
        </div>
        <div class="choice-radio" :class="{ checked: modelValue === 'solo' }">
          ✓
        </div>
      </div>

      <!-- Duo Card -->
      <div
        class="choice-card"
        :class="{ active: modelValue === 'duo' }"
        @click="emit('update:modelValue', 'duo')"
      >
        <div class="choice-icon-wrap friends-gradient">
          <span class="choice-emoji">👥</span>
        </div>
        <div class="choice-body">
          <h3 class="choice-title">Duel à Deux</h3>
          <p class="choice-desc">Défie un copain ou un parent sur le même écran !</p>
        </div>
        <div class="choice-radio" :class="{ checked: modelValue === 'duo' }">
          ✓
        </div>
      </div>
    </div>

    <div class="step-actions">
      <button type="button" class="btn btn-secondary" @click="emit('back')">
        ← Retour à l'affiche
      </button>
      <button type="button" class="btn btn-primary" @click="emit('next')">
        Continuer vers la langue →
      </button>
    </div>
  </div>
</template>

<style scoped>
.step-card {
  max-width: 580px;
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

.modes-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.choice-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  background: rgba(30, 41, 59, 0.6);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 0 rgba(0, 0, 0, 0.25);
}

.choice-card:hover {
  background: rgba(51, 65, 85, 0.85);
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.choice-card.active {
  background: rgba(99, 102, 241, 0.22);
  border-color: var(--accent-primary);
  box-shadow: 0 5px 0 var(--accent-primary-shadow);
  transform: translateY(-3px);
}

.choice-icon-wrap {
  width: 58px;
  height: 58px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.bot-gradient {
  background: linear-gradient(135deg, #ec4899, #f43f5e);
}

.friends-gradient {
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
}

.choice-emoji {
  font-size: 2rem;
}

.choice-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.choice-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-main);
}

.choice-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.4;
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

