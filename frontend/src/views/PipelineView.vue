<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'
import { Pipeline } from '../types/Pipeline'
import useRest from '../use/rest'
import SPipeline from '../components/SPipeline/SPipeline.vue'
import { NDivider, NSpace, useMessage } from 'naive-ui'
import { useStore } from 'vuex'
import { computed } from '@vue/reactivity'
import useSocket from '../use/socket'
import { OPEN_PIPELINE } from '../utils/commands'
import { useRouter } from 'vue-router'
const router = useRouter()
const socket = useSocket()
const rest = useRest()
const pipelines = ref<Pipeline[]>()
const store = useStore()
const pipelineOpened = computed(() => store.getters.currentPipeline)

const openedId = computed(() => {
  if (pipelineOpened.value) {
    return pipelineOpened.value.id
  }
  return null
})

const openPipeline = (id: string) => {
  socket.sendToServer(OPEN_PIPELINE, { id })
  router.push({ name: 'Editor' })
}

const message = useMessage()
onMounted(async () => {
  pipelines.value = await rest.getPipelines()
})
</script>

<template>
  <NDivider />
  <NSpace vertical :size="16">
    <div v-for="(item, index) in pipelines" :key="index">
      <SPipeline
        :pipeline="item"
        :is-opened="item.id === openedId"
        @open="openPipeline"
        :card="true"
      />
    </div>
  </NSpace>
</template>
