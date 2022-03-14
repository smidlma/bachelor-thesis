import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueNativeSock from "vue-native-websocket-vue3";

// General Font
import "vfonts/Lato.css";
// Monospace Font
import "vfonts/FiraCode.css";

const app = createApp(App);
app.use(router);
app.use(store);
app.use(VueNativeSock, "ws://localhost:8000/ws", {
  store: store,
  format: "json",
});
app.mount("#app");
