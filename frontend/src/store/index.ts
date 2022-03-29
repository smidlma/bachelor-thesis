import { getCurrentInstance } from 'vue'
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
    },
    // Connection closed
    SOCKET_ONCLOSE(state, event) {
      state.socket.isConnected = false

      state.socket.heartBeatTimer = 0
      console.log('The line is disconnected: ' + new Date())
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
      return -1
    },
  },
})
