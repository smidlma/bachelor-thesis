import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// General Font
import 'vfonts/Lato.css';
// Monospace Font
import 'vfonts/FiraCode.css';

createApp(App).use(store).use(router).mount('#app');
