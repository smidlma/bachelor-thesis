<script setup lang="ts">
import {
  darkTheme,
  NConfigProvider,
  GlobalTheme,
  NMessageProvider,
  NLoadingBarProvider,
  NNotificationProvider,
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
      <NNotificationProvider>
        <NMessageProvider>
          <Layout :theme="theme" @change-theme="changeTheme" />
        </NMessageProvider>
      </NNotificationProvider>
    </NLoadingBarProvider>
  </NConfigProvider>
</template>

<style lang="sass" src="./App.sass" scoped />
