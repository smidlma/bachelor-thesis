<template>
  <n-config-provider :theme="darkTheme">
    <n-button type="primary">
      Primary
    </n-button>
    <n-button type="error">
      Error
    </n-button>
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view />
  </n-config-provider>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { NConfigProvider, darkTheme, NButton } from 'naive-ui';

export default defineComponent({
  components: {
    NConfigProvider, NButton,
  },
  setup() {
    return { darkTheme };
  },
});
</script>
