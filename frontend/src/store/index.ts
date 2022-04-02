import { createStore } from 'vuex'
import { INIT_STATE } from '../utils/commands'

export default createStore({
  state: {
    socket: {
      // Connection Status
      isConnected: false,
      // Reconnect error
      reconnectError: false,
      // Heartbeat message sending time
      heartBeatInterval: 50000,
      // Heartbeat timer
      heartBeatTimer: 0,
    },
    pipeline: null,
    runningPipelines: [],
    issues: [],
  },
  mutations: {
    // Connection open
    SOCKET_ONOPEN(state, event) {
      state.socket.isConnected = true
      console.log('Connection open')
      const socket = event.currentTarget
      const msg = { from: 'FE', to: 'BE', cmd: INIT_STATE, data: null }
      console.log(msg)
      socket.sendObj(msg)

      //@ts-ignore
      window.$notification.success({
        content: 'Server connected',
        duration: 3000,
      })
    },
    // Connection closed
    SOCKET_ONCLOSE(state, event) {
      state.socket.isConnected = false

      state.socket.heartBeatTimer = 0
      console.log('The line is disconnected: ' + new Date())
      //@ts-ignore
      window.$notification.error({
        content: 'Server is not connected',
        duration: 5000,
      })
    }, // An error occurred
    SOCKET_ONERROR(state, event) {
      console.error(state, event)
    },
    // Receive the message sent by the server
    SOCKET_ONMESSAGE(state, message) {
      console.log(message)
      if (message.cmd === 'PIPELINE') {
        state.pipeline = message.data
      } else if (message.cmd === 'INIT') {
      } else if (message.cmd === 'RUNNING_PIPELINE') {
        state.runningPipelines = message.data
        if (message.data.length > 0) {
          //@ts-ignore
          window.$notification.info({
            content: `Pipeline is running`,
            duration: 5000,
          })
        }
      } else if (message.cmd === 'INFO') {
        if (message.data.success) {
          //@ts-ignore
          window.$notification.success({
            content: `${message.data.message}`,
            duration: 5000,
          })
        } else {
          //@ts-ignore
          window.$notification.error({
            content: `Error: ${message.data.error}`,
          })
        }
      }
    },
    // Auto reconnect
    SOCKET_RECONNECT(state, count) {
      console.info('reconecting...', count)
    },
    // Reconnect error
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true
    },
  },
  actions: {},
  modules: {},
  getters: {
    socketConnection(state) {
      return state.socket.isConnected
    },
    currentPipeline(state) {
      return state.pipeline
    },
    runningPipelines(state) {
      return state.runningPipelines
    },
  },
})
