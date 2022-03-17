import { ComponentInternalInstance, getCurrentInstance } from 'vue'

export default function () {
  const { proxy } = getCurrentInstance() as ComponentInternalInstance

  const sendToServer = (cmd: string, data: Object) => {
    const msg = { from: 'FE', to: 'BE', cmd: cmd, data: data }
    console.log(msg)

    // @ts-ignore: Unreachable code error
    proxy.$socket.sendObj(msg)
  }
  return {
    sendToServer,
  }
}
