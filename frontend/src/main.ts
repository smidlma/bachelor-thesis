import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueNativeSock from 'vue-native-websocket-vue3'

// General Font
import 'vfonts/Lato.css'
// Monospace Font
import 'vfonts/FiraCode.css'
import { HOST, PORT } from './config'

const app = createApp(App)
app.use(router)
app.use(store)
app.use(VueNativeSock, `ws://${HOST}:${PORT}/ws`, {
  store: store,
  format: 'json',
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 3000,
})

app.mount('#app')
