<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'
import { useAuthStore } from '@/stores/auth'
import OnboardingHero from '@/components/OnboardingHero.vue'
import StepMode from '@/components/StepMode.vue'
import StepLang from '@/components/StepLang.vue'
import StepLevel from '@/components/StepLevel.vue'

const router = useRouter()
const game = useGameStore()
const auth = useAuthStore()

// Wizard state: 0 = Hero Poster, 1 = Mode, 2 = Lang, 3 = Level
const currentStep = ref(0)

const selectedMode = ref('solo')
const selectedLang = ref(auth.preferredLang || 'fr')
const selectedLevel = ref(auth.preferredLevel || 'basic')

function handleHeroStart() {
  currentStep.value = 1
}

function handleNextFromMode() {
  currentStep.value = 2
}

function handleBackFromMode() {
  currentStep.value = 0
}

function handleNextFromLang() {
  currentStep.value = 3
}

function handleBackFromLang() {
  currentStep.value = 1
}

function handleBackFromLevel() {
  currentStep.value = 2
}

async function handleLaunchGame() {
  auth.setPreferences(selectedLang.value, selectedLevel.value)
  try {
    await game.createMatch(selectedLang.value, selectedLevel.value, selectedMode.value)
    router.push('/game')
  } catch (err) {
    console.error('Launch failed:', err)
  }
}
</script>

<template>
  <div class="wizard-container container">
    <!-- Milestone Progress Bar for steps 1, 2, 3 -->
    <nav v-if="currentStep > 0" class="progress-milestone-wrap animate-pop" aria-label="Étapes de préparation">
      <div class="milestones-bar">
        <button
          type="button"
          class="milestone-item"
          :class="{ active: currentStep >= 1, current: currentStep === 1 }"
          :aria-current="currentStep === 1 ? 'step' : undefined"
          aria-label="Étape 1 sur 3 : Mode"
          @click="currentStep = 1"
        >
          <span class="milestone-dot">
            <span v-if="currentStep > 1">✓</span>
            <span v-else>1</span>
          </span>
          <span class="milestone-label">Mode</span>
        </button>

        <div class="milestone-connector" :class="{ filled: currentStep >= 2 }"></div>

        <button
          type="button"
          class="milestone-item"
          :class="{ active: currentStep >= 2, current: currentStep === 2 }"
          :aria-current="currentStep === 2 ? 'step' : undefined"
          aria-label="Étape 2 sur 3 : Langue"
          @click="currentStep = 2"
        >
          <span class="milestone-dot">
            <span v-if="currentStep > 2">✓</span>
            <span v-else>2</span>
          </span>
          <span class="milestone-label">Langue</span>
        </button>

        <div class="milestone-connector" :class="{ filled: currentStep >= 3 }"></div>

        <button
          type="button"
          class="milestone-item"
          :class="{ active: currentStep >= 3, current: currentStep === 3 }"
          :aria-current="currentStep === 3 ? 'step' : undefined"
          aria-label="Étape 3 sur 3 : Défi"
          @click="currentStep = 3"
        >
          <span class="milestone-dot">
            <span>3</span>
          </span>
          <span class="milestone-label">Défi</span>
        </button>
      </div>
    </nav>

    <!-- Step Views -->
    <transition name="fade-slide" mode="out-in">
      <div :key="currentStep" class="step-view-wrapper">
        <!-- Step 0: Hero Poster -->
        <OnboardingHero
          v-if="currentStep === 0"
          @start="handleHeroStart"
        />

        <!-- Step 1: Game Mode -->
        <StepMode
          v-else-if="currentStep === 1"
          v-model="selectedMode"
          @next="handleNextFromMode"
          @back="handleBackFromMode"
        />

        <!-- Step 2: Language -->
        <StepLang
          v-else-if="currentStep === 2"
          v-model="selectedLang"
          @next="handleNextFromLang"
          @back="handleBackFromLang"
        />

        <!-- Step 3: Level & Launch -->
        <StepLevel
          v-else-if="currentStep === 3"
          v-model="selectedLevel"
          :loading="game.loading"
          @submit="handleLaunchGame"
          @back="handleBackFromLevel"
        />
      </div>
    </transition>

    <!-- Global error banner -->
    <div v-if="game.errorMessage" class="error-banner animate-shake" role="alert">
      ⚠️ {{ game.errorMessage }}
    </div>
  </div>
</template>

<style scoped>
.wizard-container {
  width: 100%;
  min-height: 90vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1.5rem 1rem;
}

.progress-milestone-wrap {
  width: 100%;
  max-width: 480px;
  margin-bottom: 2rem;
}

.milestones-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.milestone-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  border: 0;
  background: transparent;
  font: inherit;
  padding: 0.25rem;
}

.milestone-dot {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid var(--border-color);
  color: var(--text-muted);
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  transition: var(--motion-interactive);
}

.milestone-item.active .milestone-dot {
  background: var(--accent-primary);
  border-color: var(--accent-primary);
  color: #fff;
  box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
}

.milestone-item.current .milestone-dot {
  transform: scale(1.15);
  box-shadow: 0 0 18px var(--accent-primary);
}

.milestone-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  transition: color 0.2s ease;
}

.milestone-item.active .milestone-label {
  color: var(--text-main);
}

.milestone-connector {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0 0.5rem -1rem 0.5rem;
  border-radius: var(--radius-full);
  transition: background 0.3s ease;
}

.milestone-connector.filled {
  background: var(--accent-primary);
}

.step-view-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.error-banner {
  margin-top: 1.5rem;
  padding: 0.85rem 1.5rem;
  background: rgba(244, 63, 94, 0.15);
  border: 1px solid var(--accent-danger);
  border-radius: var(--radius-md);
  color: #fecdd3;
  font-weight: 600;
  text-align: center;
  max-width: 500px;
}

.milestone-item:focus-visible {
  border-radius: var(--radius-md);
}

/* Transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition:
    opacity var(--motion-standard) var(--motion-ease),
    transform var(--motion-standard) var(--motion-ease);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.98);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(0.98);
}

@media (max-width: 600px) {
  .wizard-container {
    min-height: 90svh;
    padding: 1rem 0.75rem;
  }

  .progress-milestone-wrap {
    margin-bottom: 1.25rem;
  }

  .milestone-item {
    min-height: 48px;
  }
}
</style>
