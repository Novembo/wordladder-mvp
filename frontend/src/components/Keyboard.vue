<script setup>
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['input-key', 'backspace', 'submit'])

const rows = [
  ['A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M'],
  ['ENTER', 'W', 'X', 'C', 'V', 'B', 'N', 'BACKSPACE']
]

function handleKeyClick(key) {
  if (props.disabled) return
  if (key === 'ENTER') {
    emit('submit')
  } else if (key === 'BACKSPACE') {
    emit('backspace')
  } else {
    emit('input-key', key.toLowerCase())
  }
}

function handlePhysicalKeyDown(e) {
  if (props.disabled) return
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return

  if (e.key === 'Enter') {
    if (e.target.closest('button')) return
    e.preventDefault()
    emit('submit')
  } else if (e.key === 'Backspace') {
    e.preventDefault()
    emit('backspace')
  } else if (/^[a-zA-Z]$/.test(e.key)) {
    e.preventDefault()
    emit('input-key', e.key.toLowerCase())
  }
}

onMounted(() => {
  window.addEventListener('keydown', handlePhysicalKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handlePhysicalKeyDown)
})
</script>

<template>
  <div class="virtual-keyboard" :class="{ 'is-disabled': disabled }" role="group" aria-label="Clavier de saisie">
    <div v-for="(row, rIdx) in rows" :key="rIdx" class="keyboard-row">
      <button
        v-for="k in row"
        :key="k"
        type="button"
        class="key-btn"
        :class="{
          'key-wide': k === 'ENTER' || k === 'BACKSPACE',
          'key-enter': k === 'ENTER',
          'key-backspace': k === 'BACKSPACE'
        }"
        :aria-label="k === 'ENTER' ? 'Valider le mot' : k === 'BACKSPACE' ? 'Effacer la dernière lettre' : k"
        :disabled="disabled"
        @click="handleKeyClick(k)"
      >
        <span v-if="k === 'BACKSPACE'">⌫</span>
        <span v-else-if="k === 'ENTER'">Valider</span>
        <span v-else>{{ k }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.virtual-keyboard {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-top: 1rem;
  touch-action: manipulation;
  user-select: none;
  max-width: 580px;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
}

.virtual-keyboard.is-disabled {
  opacity: 0.6;
  pointer-events: none;
}

.keyboard-row {
  display: flex;
  justify-content: center;
  gap: 0.35rem;
}

.key-btn {
  flex: 1;
  min-width: 0;
  min-height: 48px;
  height: 48px;
  background: rgba(30, 41, 59, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-sm);
  color: var(--text-main);
  font-family: var(--font-main);
  font-size: 1.05rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--motion-interactive);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.key-btn:hover:not(:disabled) {
  background: rgba(51, 65, 85, 0.95);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.key-btn:active:not(:disabled) {
  transform: translateY(1px);
  background: var(--accent-primary);
}

.key-wide {
  flex: 1.6;
  font-size: 0.85rem;
  letter-spacing: 0.02em;
}

.key-enter {
  background: linear-gradient(135deg, var(--accent-primary), #4f46e5);
  color: #fff;
  border-color: rgba(99, 102, 241, 0.4);
}

.key-enter:hover:not(:disabled) {
  background: linear-gradient(135deg, #4f46e5, #4338ca);
}

.key-backspace {
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
  border-color: rgba(239, 68, 68, 0.25);
  font-size: 1.2rem;
}

.key-backspace:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.25);
}

@media (max-width: 600px) {
  .virtual-keyboard {
    margin-top: 0.5rem;
  }

  .key-btn {
    height: 48px;
    font-size: 0.95rem;
  }
  .key-wide {
    font-size: 0.75rem;
  }
}
</style>
