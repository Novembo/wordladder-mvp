import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SetupWizardView from '../views/SetupWizardView.vue'
import GameView from '../views/GameView.vue'
import ResultView from '../views/ResultView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/setup',
      name: 'setup',
      component: SetupWizardView
    },
    {
      path: '/game',
      name: 'game',
      component: GameView
    },
    {
      path: '/result',
      name: 'result',
      component: ResultView
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: LeaderboardView
    }
  ]
})

export default router

