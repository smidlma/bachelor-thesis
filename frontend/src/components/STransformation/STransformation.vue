<script setup lang="ts">
import { NCard, NSelect, NSpace, NInput } from 'naive-ui'
import { PropType } from 'vue'
import { Schema } from '../../types/Pipeline'
import SSort from './SSort.vue'
import SSelectTransformation from './SSelectTransformation.vue'

const template = [{ name: 'Sort' }]
const props = defineProps({
  transformation: { type: Object, default: {} },
  schema: {
    type: Object as PropType<Schema>,
    default: {},
  },
  select: { type: Boolean, default: false },
  editable: { type: Boolean, default: false },
})

const columns = props.schema?.fields.map((x) => {
  return { label: x.name, value: x.name }
})
</script>

<template>
  <div v-if="props.select">
    <SSelectTransformation />
  </div>
  <div v-else>
    <NCard :title="transformation.name">
      <div v-if="transformation.name === 'Sort'">
        <SSort />
      </div>
    </NCard>
  </div>
</template>

<style></style>
