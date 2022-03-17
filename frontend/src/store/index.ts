import { createStore } from 'vuex'
// import main from "../main";

export default createStore({
  state: {
    socket: {
      // Connection Status
      isConnected: false,
      // Message content
      message: '',
      // Reconnect error
      reconnectError: false,
      // Heartbeat message sending time
      heartBeatInterval: 50000,
      // Heartbeat timer
      heartBeatTimer: 0,
    },
    pipeline: null,
  },
  mutations: {
    // Connection open
    SOCKET_ONOPEN(state, event) {
      // main.config.globalProperties.$socket = event.currentTarget;
      state.socket.isConnected = true
      console.log('Connection open')
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
      state.pipeline = message.data
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
    currentPipeline(state) {
      return state.pipeline
    },
    runningPipelines(state) {
      return -1
    },
  },
})
