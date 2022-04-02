<script setup lang="ts">
import {
  NDivider,
  NSpace,
  NIcon,
  NIconWrapper,
  NPageHeader,
  NButton,
  NDrawer,
  NDrawerContent,
} from 'naive-ui'
import { onMounted, ref } from 'vue'
import { Connection } from '../types/Pipeline'
import useRest from '../use/rest'
import SConnection from '../components/SConnection.vue'
import { Flash } from '@vicons/ionicons5'

const rest = useRest()
const connections = ref<Array<Connection>>([])
onMounted(async () => {
  connections.value = await rest.getConnections()
})

const activeDrawer = ref(false)
</script>
<template>
  <NPageHeader :subtitle="`Number of connections: ${connections.length}`">
    <template #title>Connections</template>
    <template #avatar>
      <NIconWrapper color="rgba(99, 226, 183, 0.16)" :size="40">
        <NIcon :size="32" color="#63e2b7">
          <Flash />
        </NIcon>
      </NIconWrapper>
    </template>
    <template #extra>
      <NSpace>
        <NButton @click="activeDrawer = true">Connect</NButton>
      </NSpace>
    </template>
  </NPageHeader>
  <NDivider />
  <NSpace vertical :size="16">
    <div v-for="(item, index) in connections" :key="index">
      <SConnection :preview="true" :connection="item" />
    </div>
  </NSpace>
  <NDrawer v-model:show="activeDrawer" :width="800" placement="right">
    <NDrawerContent title="Stoner">
      Stoner is a 1965 novel by the American writer John Williams.
    </NDrawerContent>
  </NDrawer>
</template>

<style></style>
