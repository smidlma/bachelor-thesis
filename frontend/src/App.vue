<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import {
  NLayout,
  NButton,
  NLayoutHeader,
  NLayoutFooter,
  NMenu,
  darkTheme,
  NConfigProvider,
  NLayoutSider,
  GlobalTheme,
  NLayoutContent,
  NPageHeader,
  NSpace,
  NAvatar,
  MenuOption,
} from 'naive-ui'
import { ref, h } from 'vue'
import { RouterLink } from 'vue-router'

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'Home',
          },
        },
        { default: () => 'Home' }
      ),
    key: 'home',
    // icon: renderIcon(HomeIcon)
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'Files',
          },
        },
        { default: () => 'Files' }
      ),
    key: 'files',
    // icon: renderIcon(WorkIcon),
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'Editor',
          },
        },
        { default: () => 'Editor' }
      ),
    key: 'editor',
    // icon: renderIcon(WorkIcon),
  },
]

const theme = ref<GlobalTheme | null>(darkTheme)
</script>

<template>
  <NConfigProvider :theme="theme">
    <NLayout position="absolute">
      <NLayoutHeader bordered class="s-nav-header">
        <NPageHeader>
          <template #title>ETL tool</template>
          <template #avatar>
            <NAvatar
              src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
            />
          </template>
          <template #extra>
            <NSpace>
              <NButton
                @click="
                  () => {
                    // @ts-ignore: Unreachable code error
                    $socket.sendObj({ cmd: 'INIT_STATE' })
                  }
                "
                >Create pipeline</NButton
              >
              <NButton v-if="theme" @click="theme = null">Light</NButton>
              <NButton v-else @click="theme = darkTheme">Dark</NButton>
            </NSpace>
          </template>
        </NPageHeader>
      </NLayoutHeader>
      <NLayout has-sider position="absolute" style="top: 64px; bottom: 64px">
        <NLayoutSider
          bordered
          show-trigger
          collapse-mode="width"
          :collapsed-width="64"
          :width="240"
          :native-scrollbar="false"
        >
          <NMenu
            :collapsed-width="64"
            :collapsed-icon-size="22"
            :options="menuOptions"
          />
        </NLayoutSider>
        <NLayout content-style="padding: 24px;">
          <NLayoutContent>
            <router-view />
          </NLayoutContent>
        </NLayout>
      </NLayout>
      <NLayoutFooter
        bordered
        position="absolute"
        style="height: 64px; padding: 24px"
      >
        @Martin Smidl
      </NLayoutFooter>
    </NLayout>
  </NConfigProvider>
</template>

<style lang="sass" src="./App.sass" scoped />
