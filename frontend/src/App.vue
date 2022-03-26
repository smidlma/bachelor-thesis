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
  NIcon,
  NMessageProvider,
  NLoadingBarProvider,
  useLoadingBar,
  useMessage,
} from 'naive-ui'
import { ref, h, Component } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Analytics, FileTray, Build } from '@vicons/ionicons5'

// const loadingBar = useLoadingBar()

const renderIcon = (icon: Component) => {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'Pipelines',
          },
        },
        { default: () => 'Pipelines' }
      ),
    key: 'pipelines',
    icon: renderIcon(Analytics),
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
    icon: renderIcon(FileTray),
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
    icon: renderIcon(Build),
  },
]

const theme = ref<GlobalTheme | null>(darkTheme)
const router = useRouter()
const menuRef = ref(null)
const routeItem = ref<string | undefined>('Pipelines')

router.beforeEach((to) => {
  console.log(to)
  routeItem.value = to.name?.toString().toLocaleLowerCase()
})
</script>

<template>
  <NConfigProvider :theme="theme">
    <NMessageProvider>
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
              ref="menuRef"
              :collapsed-width="64"
              :collapsed-icon-size="22"
              :options="menuOptions"
              :value="routeItem"
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
    </NMessageProvider>
  </NConfigProvider>
</template>

<style lang="sass" src="./App.sass" scoped />
