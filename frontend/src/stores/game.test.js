import { afterEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useGameStore } from './game'

describe('game store API failures', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('ignores an early timeout response without changing the game state', async () => {
    setActivePinia(createPinia())
    const game = useGameStore()
    game.matchId = 'a'.repeat(32)
    game.lives = [3, 3]
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
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
      json: async () => ({ detail: { code: 'unknown_word', message: 'Mot inconnu' } })
    }))

    await expect(game.playMove('nope')).resolves.toBe(false)
    expect(game.errorMessage).toBe('Mot inconnu')
  })
})
