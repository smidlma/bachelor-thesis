<script setup lang="ts">
import {
  NLayout,
  NButton,
  NLayoutHeader,
  NLayoutFooter,
  NMenu,
  NLayoutSider,
  GlobalTheme,
  NLayoutContent,
  NPageHeader,
  NSpace,
  NAvatar,
  MenuOption,
  NIcon,
  useLoadingBar,
  useNotification,
  NDrawer,
  NDrawerContent,
} from 'naive-ui'
import { ref, h, Component, PropType, watch, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Analytics, FileTray, Build } from '@vicons/ionicons5'
import { useStore } from 'vuex'
import { computed } from '@vue/reactivity'
import store from './store'
import SPipelineCreate from './components/SPipelineCreate/SPipelineCreate.vue'
import { Pipeline } from './types/Pipeline'
import useRest from './use/rest'
const rest = useRest()
const props = defineProps({
  theme: { type: Object as PropType<GlobalTheme | null>, default: null },
})

const emit = defineEmits(['changeTheme'])

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

const loadingBar = useLoadingBar()
const router = useRouter()
const routeItem = ref<string | undefined>('Pipelines')

router.beforeEach((to) => {
  loadingBar.start()
  routeItem.value = to.name?.toString().toLocaleLowerCase()
})
router.afterEach(() => {
  loadingBar.finish()
})
// const store = useStore()
const notification = useNotification()
const serverIsConnected = computed(() => store.getters.socketConnection)
watch(serverIsConnected, () => showConnInfo())

onMounted(() => showConnInfo())

const showConnInfo = () => {
  if (serverIsConnected.value) {
    notification.success({ content: 'Server connected', duration: 5000 })
  } else {
    notification.error({ content: 'Server is not connected', duration: 5000 })
  }
}

const activeDrawer = ref(false)

const createPipeline = async (data: Object) => {
  activeDrawer.value = false
  const result = await rest.createPipeline(data)
  if (result.created) {
    notification.success({ content: 'Pipeline created', duration: 2000 })
    router.push({ name: 'Editor' })
  } else {
    notification.error({
      content: `Not created: ${result.error}`,
      duration: 2000,
    })
  }
}
</script>

<template>
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
            <NButton @click="activeDrawer = true">Create pipeline</NButton>
            <NButton v-if="props.theme" @click="emit('changeTheme', 'light')"
              >Light</NButton
            >
            <NButton v-else @click="emit('changeTheme', 'dark')">Dark</NButton>
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
          :value="routeItem"
        />
      </NLayoutSider>
      <NLayout content-style="padding: 24px;">
        <NLayoutContent>
          <router-view />
          <NDrawer v-model:show="activeDrawer" :width="800" placement="right">
            <NDrawerContent title="Pipeline">
              <SPipelineCreate @create="createPipeline" />
            </NDrawerContent>
          </NDrawer>
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
</template>

<style lang="sass" src="./App.sass" scoped />
