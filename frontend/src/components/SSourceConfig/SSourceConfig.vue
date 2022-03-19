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
const props = defineProps({
  source: { type: Object as PropType<Source>, default: null },
})
const rest = useRest()

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
  sourceName: '',
})

const addSource = (type: string) => {}
</script>

<template>
  <template v-if="props.source"> Edit source </template>
  <template v-else>
    <NTabs type="segment">
      <NTabPane name="csv" tab="CSV">
        <NDivider></NDivider>
        <NSpace vertical size="large">
          <NInput
            v-model:value="form.sourceName"
            placeholder="Name of the source"
          ></NInput>
          <NSelect :options="files"></NSelect>
          <NButton>Add</NButton>
        </NSpace>
      </NTabPane>
      <NTabPane name="postgresql" tab="PostgreSQL">
        <NDivider></NDivider>
        <NSpace vertical>
          <NInput placeholder="Name of the source"></NInput>
          <NSelect
            :options="files"
            placeholder="Select from defined connections"
          >
          </NSelect>
          <NSpace>
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
