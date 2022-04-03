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
import SCSV from './SCSV.vue'
import SPostgreSQL from './SPostgreSQL.vue'
const props = defineProps({
  source: { type: Object as PropType<Source>, default: null },
})
const rest = useRest()
const socket = useSocket()
const files: any = ref([])
const connections: any = ref([])
const isTested = ref(false)

onMounted(async () => {
  files.value = await rest.getFiles()

  connections.value = await rest.getConnections()
})

const addSource = (data: Object) => {
  socket.sendToServer(ADD_SOURCE, data)
}
</script>

<template>
  <template v-if="props.source"> Edit source </template>
  <template v-else>
    <NTabs type="segment">
      <NTabPane name="csv" tab="CSV">
        <NDivider></NDivider>
        <SCSV :files="files" @add="addSource" />
      </NTabPane>
      <NTabPane name="postgresql" tab="PostgreSQL">
        <NDivider></NDivider>
        <SPostgreSQL :connectios="connections" @add="addSource" />
      </NTabPane>
    </NTabs>
  </template>
</template>

<style></style>
