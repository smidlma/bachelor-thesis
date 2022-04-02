<script setup lang="ts">
import { Document } from '@vicons/ionicons5'
import { NCard, NIcon, NButton, NSpace, NEllipsis, NModal, NP } from 'naive-ui'
import { h, ref } from 'vue'
const props = defineProps({
  fileName: {
    type: String,
    required: true,
  },
  fileSize: {
    type: Number,
    required: true,
  },
  filePreview: {
    type: Array,
  },
})

const formatBytes = (bytes: any, decimals = 2) => {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

const showPreview = ref(false)
</script>

<template>
  <NCard class="s-file">
    <template #header>
      <NEllipsis style="max-width: 180px">
        {{ props.fileName }}
      </NEllipsis>
    </template>
    <template #cover>
      <NIcon class="s-file__icon">
        <Document></Document>
      </NIcon>
    </template>
    {{ formatBytes(props.fileSize) }}
    <template #action>
      <NSpace justify="center">
        <NButton @click="showPreview = true">View</NButton>
      </NSpace>
    </template>
  </NCard>
  <NModal v-model:show="showPreview">
    <NCard style="width: 1000px">
      <NP v-for="(item, index) in props.filePreview" :key="index">{{
        item
      }}</NP>
    </NCard>
  </NModal>
</template>

<style lang="sass" scoped>

.s-file
    text-align: center
    padding: 12px

.s-file__icon
    font-size: 26px
</style>
