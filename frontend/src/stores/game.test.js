import { afterEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useGameStore } from './game'
import { clearPacksCache, localEngine } from '@/services/localEngine'

describe('game store API failures', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
    localEngine.reset()
    clearPacksCache()
  })

  it('ignores an early timeout response without changing the game state', async () => {
    setActivePinia(createPinia())
    const game = useGameStore()
    game.matchId = 'a'.repeat(32)
    game.lives = [3, 3]
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      headers: new Headers({ 'content-type': 'application/json' }),
      json: async () => ({ detail: { code: 'too_early', message: 'Too early' } })
    }))

    await expect(game.handleTimeout()).resolves.toBe(false)
    expect(game.lives).toEqual([3, 3])
    expect(game.errorMessage).toBe('')
  })

  it('shows a useful validation error from a rejected move', async () => {
    setActivePinia(createPinia())
    const game = useGameStore()
    game.matchId = 'b'.repeat(32)
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      headers: new Headers({ 'content-type': 'application/json' }),
      json: async () => ({ detail: { code: 'unknown_word', message: 'Mot inconnu' } })
    }))

    await expect(game.playMove('nope')).resolves.toBe(false)
    expect(game.errorMessage).toBe('Mot inconnu')
  })

  it('falls back to local client engine when backend is unavailable (404/network error)', async () => {
    setActivePinia(createPinia())
    const game = useGameStore()

    // Mock pack data with fully connected 1-letter ladder connections
    const mockPack = {
      lang: 'fr',
      version: '1.0.0',
      graph: {
        bain: ['pain', 'main', 'gain', 'nain'],
        pain: ['bain', 'main', 'gain', 'nain'],
        main: ['bain', 'pain', 'gain', 'nain'],
        gain: ['bain', 'pain', 'main', 'nain'],
        nain: ['bain', 'pain', 'main', 'gain']
      },
      levels: {
        basic: ['bain', 'pain', 'main', 'gain', 'nain']
      }
    }

    vi.stubGlobal('fetch', vi.fn().mockImplementation((url) => {
      if (String(url).includes('/matches')) {
        return Promise.resolve({
          ok: false,
          status: 404,
          headers: new Headers({ 'content-type': 'text/plain' }),
          text: async () => 'Not Found'
        })
      }
      if (String(url).includes('/packs/fr.json')) {
        return Promise.resolve({
          ok: true,
          status: 200,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => mockPack
        })
      }
      return Promise.resolve({
        ok: false,
        status: 404,
        headers: new Headers({ 'content-type': 'text/plain' }),
        text: async () => 'Not Found'
      })
    }))

    const match = await game.createMatch('fr', 'basic', 'duo')
    expect(game.isLocal).toBe(true)
    expect(match.word_length).toBe(4)
    expect(game.currentWord).toBeDefined()
    expect(game.lives).toEqual([3, 3])

    // Try a valid move directly from current word's legal neighbors
    const current = game.currentWord
    const validMoves = mockPack.graph[current] || []
    const nextMove = validMoves[0]
    const success = await game.playMove(nextMove)
    expect(success).toBe(true)
    expect(game.currentWord).toBe(nextMove)

    // Try an invalid move (wrong length or unknown)
    const fail = await game.playMove('inconnu')
    expect(fail).toBe(false)
    expect(game.errorMessage).toBeTruthy()
  })
})
