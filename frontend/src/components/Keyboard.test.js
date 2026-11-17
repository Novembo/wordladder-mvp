import { afterEach, describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import Keyboard from './Keyboard.vue'

describe('Keyboard', () => {
  let wrapper

  afterEach(() => wrapper?.unmount())

  it('accepts physical letters, backspace, and enter', async () => {
    wrapper = mount(Keyboard)
    document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'A', bubbles: true }))
    document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'Backspace', bubbles: true }))
    document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }))

    expect(wrapper.emitted('input-key')).toEqual([['a']])
    expect(wrapper.emitted('backspace')).toHaveLength(1)
    expect(wrapper.emitted('submit')).toHaveLength(1)
    expect(wrapper.attributes('aria-label')).toBe('Clavier de saisie')
  })

  it('does not capture keys while disabled or while a key button has focus', async () => {
    wrapper = mount(Keyboard, { props: { disabled: true } })
    document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'B', bubbles: true }))
    expect(wrapper.emitted('input-key')).toBeUndefined()

    await wrapper.setProps({ disabled: false })
    const button = wrapper.get('button').element
    button.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }))
    expect(wrapper.emitted('submit')).toBeUndefined()
  })
})
