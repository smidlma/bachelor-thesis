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
  useNotification,
} from 'naive-ui'
import { onMounted, ref } from 'vue'
import { Connection } from '../types/Pipeline'
import useRest from '../use/rest'
import SConnection from '../components/SConnection.vue'
import { Flash } from '@vicons/ionicons5'

const rest = useRest()
const connections = ref<Array<Connection>>([])
const loadConnections = async () => {
  connections.value = await rest.getConnections()
}
onMounted(async () => await loadConnections())
const nt = useNotification()
const activeDrawer = ref(false)

const checkAndAddConnection = async (status: any) => {
  if (status.connected) {
    nt.success({ content: 'Connection tested and created', duration: 2000 })
    const result = await rest.createConnection(status.connection)
    console.log(result)
    await loadConnections()
    activeDrawer.value = false
  } else {
    nt.error({ content: 'Connection test failed', duration: 2000 })
  }
}

const handleUpdate = (conn: any) => {
  console.log(conn)
}
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
    <NDrawerContent title="Connection configuration">
      <SConnection
        :editable="true"
        @connection-status="checkAndAddConnection"
      />
    </NDrawerContent>
  </NDrawer>
</template>

<style></style>
