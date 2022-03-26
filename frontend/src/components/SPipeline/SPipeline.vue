<script setup lang="ts">
import {
  NCard,
  NSpace,
  NH2,
  NText,
  NH5,
  NIcon,
  NGrid,
  NGi,
  NButton,
} from 'naive-ui'
import { PropType } from 'vue'
import { Pipeline } from '../../types/Pipeline'
import { ChevronForward } from '@vicons/ionicons5'
const props = defineProps({
  pipeline: { type: Object as PropType<Pipeline>, required: true },
  isOpened: { type: Boolean, default: false },
})

const emit = defineEmits(['open', 'close'])
</script>

<template>
  <NCard>
    <NGrid cols="4" responsive="screen">
      <NGi>
        <NSpace vertical>
          <NH2 prefix="bar">
            <NText>{{ props.pipeline.name }}</NText>
          </NH2>
        </NSpace>
      </NGi>
      <NGi style="text-align: center">
        <NIcon size="80"><ChevronForward /></NIcon>
      </NGi>
      <NGi style="text-align: center">
        <NH2>
          <NText>{{ props.pipeline.destination.destinationName }} </NText>
        </NH2>
      </NGi>
      <NGi>
        <NButton @click="emit('open', props.pipeline.id)">Open</NButton>
      </NGi>
    </NGrid>
  </NCard>
</template>
<style></style>
