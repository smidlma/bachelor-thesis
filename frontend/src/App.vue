<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import {
  darkTheme,
  NConfigProvider,
  GlobalTheme,
  NMessageProvider,
  NLoadingBarProvider,
} from 'naive-ui'
import { ref } from 'vue'
import Layout from './Layout.vue'

const theme = ref<GlobalTheme | null>(darkTheme)
const changeTheme = (type: string) => {
  theme.value = type === 'light' ? null : darkTheme
}
</script>

<template>
  <NConfigProvider :theme="theme">
    <NLoadingBarProvider :loading-bar-style="{ loading: 'height: 5px' }">
      <NMessageProvider>
        <Layout :theme="theme" @change-theme="changeTheme" />
      </NMessageProvider>
    </NLoadingBarProvider>
  </NConfigProvider>
</template>

<style lang="sass" src="./App.sass" scoped />
