<script setup lang="ts">
import { onMounted, PropType, ref } from 'vue'
import { Source } from '../../types/Pipeline'
import {
  NInput,
  NSelect,
  NTabs,
  NTabPane,
  NSpace,
  NButton,
  NDivider,
} from 'naive-ui'
import useRest from '../../use/rest'
import useSocket from '../../use/socket'
import { ADD_SOURCE } from '../../utils/commands'
import { Add } from '@vicons/ionicons5'
import SConnection from '../SConnection.vue'
const props = defineProps({
  source: { type: Object as PropType<Source>, default: null },
})
const rest = useRest()
const socket = useSocket()
const files: any = ref([])
const connections: any = ref([])
const isTested = ref(false)

onMounted(async () => {
  const d = await rest.getFiles()
  files.value = d.map((x) => {
    return { label: x.fileName, value: x.fileName }
  })

  const c = await rest.getConnections()
  connections.value = c.map((x) => {
    return { label: x.database, value: x.id }
  })
})
const formCSV = ref({
  name: '',
  fileName: null,
})
const addSource = (type: string) => {
  socket.sendToServer(ADD_SOURCE, { sourceType: type, ...formCSV.value })
}
</script>

<template>
  <template v-if="props.source"> Edit source </template>
  <template v-else>
    <NTabs type="segment">
      <NTabPane name="csv" tab="CSV">
        <NDivider></NDivider>
        <NSpace vertical size="large">
          <NInput
            v-model:value="formCSV.name"
            placeholder="Name of the source"
          ></NInput>
          <NSelect
            placeholder="Select the file"
            :options="files"
            v-model:value="formCSV.fileName"
          ></NSelect>
          <NButton @click="addSource('csv')">Add</NButton>
        </NSpace>
      </NTabPane>
      <NTabPane name="postgresql" tab="PostgreSQL">
        <NDivider></NDivider>
        <NSpace vertical size="large">
          <NInput placeholder="Name of the source"></NInput>
          <NSelect
            :options="connections"
            placeholder="Select from defined connections"
          >
          </NSelect>
          <NInput placeholder="Table name to extract from"></NInput>
          <NSpace>
            <NButton>Add</NButton>
          </NSpace>
        </NSpace>
      </NTabPane>
    </NTabs>
  </template>
</template>

<style></style>
