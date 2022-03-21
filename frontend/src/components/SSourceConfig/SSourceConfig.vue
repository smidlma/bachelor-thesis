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
  console.log(c)
})
const form = ref({
  name: '',
  fileName: null,
})
const a = { v: 1, f: 3 }
const addSource = (type: string) => {
  socket.sendToServer(ADD_SOURCE, { sourceType: type, ...form.value })
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
            v-model:value="form.name"
            placeholder="Name of the source"
          ></NInput>
          <NSelect
            placeholder="Select the file"
            :options="files"
            v-model:value="form.fileName"
          ></NSelect>
          <NButton @click="addSource('csv')">Add</NButton>
        </NSpace>
      </NTabPane>
      <NTabPane name="postgresql" tab="PostgreSQL">
        <NDivider></NDivider>
        <NSpace vertical size="large">
          <NInput placeholder="Name of the source"></NInput>
          <NSelect
            :options="files"
            placeholder="Select from defined connections"
          >
          </NSelect>
          <NSpace size="large">
            <NInput placeholder="Host"></NInput>
            <NInput placeholder="Port"></NInput>
            <NInput placeholder="User"></NInput>
            <NInput placeholder="Password"></NInput>
            <NInput placeholder="Database"></NInput>
          </NSpace>
          <NInput placeholder="Table name to extract from"></NInput>
          <NSpace>
            <NButton>Test Connection</NButton>
            <NButton :disabled="!isTested">Add</NButton>
          </NSpace>
        </NSpace>
      </NTabPane>
    </NTabs>
  </template>
</template>

<style></style>
