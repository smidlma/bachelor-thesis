<script setup lang="ts">
import {
  NCard,
  NSpace,
  NH2,
  NText,
  NH5,
  NIcon,
  NPageHeader,
  NAvatar,
  NButton,
  NIconWrapper,
  NSpin,
} from 'naive-ui'
import { PropType } from 'vue'
import { Pipeline } from '../../types/Pipeline'
import { ChevronForward } from '@vicons/ionicons5'
import { Analytics } from '@vicons/ionicons5'
const props = defineProps({
  pipeline: { type: Object as PropType<Pipeline>, required: true },
  isOpened: { type: Boolean, default: false },
  card: { type: Boolean, default: false },
  editor: { type: Boolean, default: false },
  isRunning: { type: Boolean, default: false },
})

const emit = defineEmits(['open', 'close', 'run'])
</script>

<template>
  <NCard v-if="props.card" color="red">
    <NPageHeader
      :subtitle="`Sources: ${props.pipeline.sources.length} -> Destination: ${props.pipeline.destination.destinationName}`"
    >
      <template #title>Pipeline: {{ props.pipeline.name }}</template>
      <template #avatar>
        <NIconWrapper color="rgba(99, 226, 183, 0.16)" :size="40">
          <NIcon :size="32" color="#63e2b7">
            <Analytics />
          </NIcon>
        </NIconWrapper>
      </template>

      <template #extra>
        <NSpace>
          <div v-if="!props.editor">
            <NButton
              v-if="!props.isRunning"
              @click="emit('open', props.pipeline.id)"
              >Open</NButton
            >
            <NSpin v-else size="small" description="Running..." />
          </div>

          <NSpace v-else>
            <NButton
              :disabled="!props.pipeline.sources.length > 0"
              @click="emit('run', props.pipeline.id)"
              >Run</NButton
            >
            <NButton @click="emit('close', props.pipeline.id)">Close</NButton>
          </NSpace>
        </NSpace>
      </template>
    </NPageHeader>
    <template #header-extra> #header-extra </template>
  </NCard>
</template>
<style></style>
