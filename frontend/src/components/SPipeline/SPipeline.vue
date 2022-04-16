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
})

const emit = defineEmits(['open', 'close', 'run'])
</script>

<template>
  <NCard v-if="props.card">
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
        <!-- <NAvatar
          src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
        /> -->
      </template>
      <template #extra>
        <NSpace>
          <NButton v-if="!props.editor" @click="emit('open', props.pipeline.id)"
            >Open</NButton
          >
          <NSpace v-else>
            <NButton @click="emit('run', props.pipeline.id)">Run</NButton>
            <NButton @click="emit('close', props.pipeline.id)">Close</NButton>
          </NSpace>
        </NSpace>
      </template>
    </NPageHeader>
  </NCard>
</template>
<style></style>
