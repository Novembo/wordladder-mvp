import { afterEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { useGameStore } from '@/stores/game'
import Timer from './Timer.vue'

describe('Timer', () => {
  let wrapper

  afterEach(() => {
    wrapper?.unmount()
    vi.useRealTimers()
  })

  it('renders the remaining time from the server deadline', async () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-11-17T12:00:00.000Z'))
    setActivePinia(createPinia())
    const game = useGameStore()
    game.timeLimit = 80
    game.deadlineAt = new Date(Date.now() + 2500).toISOString()
    game.finished = false
    game.handleTimeout = vi.fn().mockResolvedValue(true)
    expect(Date.parse(game.deadlineAt)).not.toBeNaN()
    console.log('timer fixture', game.deadlineAt, Date.now(), Date.parse(game.deadlineAt))

    wrapper = mount(Timer)
    expect(wrapper.find('.timer-number').text()).toBe('3')

    await vi.advanceTimersByTimeAsync(1200)
    expect(wrapper.find('.timer-number').text()).toBe('2')
    expect(game.handleTimeout).not.toHaveBeenCalled()
  })

  it('reports expiration once when the deadline is reached', async () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-11-17T12:00:00.000Z'))
    setActivePinia(createPinia())
    const game = useGameStore()
    game.timeLimit = 80
    game.deadlineAt = new Date(Date.now() + 100).toISOString()
    game.finished = false
    game.handleTimeout = vi.fn().mockResolvedValue(true)

    wrapper = mount(Timer)
    await vi.advanceTimersByTimeAsync(500)

    expect(game.handleTimeout).toHaveBeenCalledTimes(1)
    expect(wrapper.attributes('role')).toBe('timer')
  })
})
