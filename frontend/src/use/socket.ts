import { ComponentInternalInstance, getCurrentInstance } from 'vue'

export default function () {
  const { proxy } = getCurrentInstance() as ComponentInternalInstance

  const send = () => {}
  return {
    proxy,
  }
}
