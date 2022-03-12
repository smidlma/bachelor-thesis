<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import {
  NLayout, NButton, NLayoutHeader,
  NLayoutFooter, NMenu, darkTheme,
  NConfigProvider,
  NLayoutSider, GlobalTheme,
  NLayoutContent, NGrid, NGridItem, NH5
} from 'naive-ui'
import { ref } from 'vue';


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

const theme = ref<GlobalTheme | null>(darkTheme)

</script>

<template>
  <NConfigProvider :theme="theme">
    <NLayout>
      <NLayoutHeader
        bordered
        class="s-nav-header"
      >
        <NGrid
          cols="12"
          style="align-items: center;"
        >
          <NGridItem span="10">
            <h1>ETL tool</h1>
            <!-- <NH1>ETL tool</NH1> -->
          </NGridItem>
          <NGridItem>
            <NButton>Create pipeline</NButton>
          </NGridItem>
          <NGridItem>
            <div>
              <NButton
                v-if="theme"
                @click="theme = null"
              >
                Light
              </NButton>

              <NButton
                v-else
                @click="theme = darkTheme"
              >
                Dark
              </NButton>
            </div>
          </NGridItem>
        </NGrid>
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
          <NMenu
            :collapsed-width="64"
            :collapsed-icon-size="22"
            :options="menuOptions"
          />
        </NLayoutSider>
        <NLayoutContent content-style="padding: 24px;">
          <router-view />
        </NLayoutContent>
      </NLayout>
      <NLayoutFooter
        bordered
        style="padding: 12px;"
      >
        <NH5>@Martin Smidl</NH5>
      </NLayoutFooter>
    </NLayout>
  </NConfigProvider>
</template>

<style lang="sass" src="./App.sass" scoped />

