<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import {
  NLayout, NButton, NLayoutHeader,
  NLayoutFooter, NMenu, darkTheme,
  NConfigProvider,
  NLayoutSider, GlobalTheme,
  NLayoutContent, NGrid, NGridItem, NH5, NPageHeader, NSpace, NAvatar
} from 'naive-ui'
import { ref, useTransitionState, getCurrentInstance, ComponentInternalInstance, onMounted } from 'vue';


const menuOptions = [
  {
    label: 'Pipelines',
    key: 'pipelines',
  },
  {
    label: 'Connections',
    key: 'connections',
  },
  {
    label: 'Files',
    key: 'files'
  }
]


onMounted(() => {
  // const { proxy } = getCurrentInstance() as ComponentInternalInstance;
  // // @ts-ignore: Unreachable code error
  // proxy.$socket.sendObj({ msg: "Hello" })

})

const theme = ref<GlobalTheme | null>(darkTheme)

</script>

<template>
  <NConfigProvider :theme="theme">
    <NLayout>
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
                @click="() => {
                  // @ts-ignore: Unreachable code error
                  $socket.sendObj({ cmd: 'INIT_STATE' })
                }"
              >Create pipeline</NButton>
              <NButton v-if="theme" @click="theme = null">Light</NButton>
              <NButton v-else @click="theme = darkTheme">Dark</NButton>
            </NSpace>
          </template>
        </NPageHeader>
      </NLayoutHeader>

      <NLayout has-sider>
        <NLayoutSider
          bordered
          show-trigger
          collapse-mode="width"
          :collapsed-width="64"
          :width="240"
          :native-scrollbar="false"
        >
          <NMenu :collapsed-width="64" :collapsed-icon-size="22" :options="menuOptions" />
        </NLayoutSider>
        <NLayoutContent content-style="padding: 24px; min-height: 640px">
          <router-view />
        </NLayoutContent>
      </NLayout>
      <NLayoutFooter bordered style="padding: 12px;">
        <NH5>@Martin Smidl</NH5>
      </NLayoutFooter>
    </NLayout>
  </NConfigProvider>
</template>

<style lang="sass" src="./App.sass" scoped />

