<script setup lang="ts">
import { NCard, NDivider } from 'naive-ui'
import { PropType, ref } from 'vue'
import { Schema } from '../../types/Pipeline'
import SSort from './SSort.vue'
import SSelectTransformation from './SSelectTransformation.vue'
import useSocket from '../../use/socket'
import { ADD_TRANSFORMATION } from '../../utils/commands'
const props = defineProps({
  sourceId: { type: String, required: true },
  transformation: { type: Object, default: null },
  schema: {
    type: Object as PropType<Schema>,
    default: {},
  },
  editable: { type: Boolean, default: false },
})
const emit = defineEmits(['close'])
const { sendToServer } = useSocket()

const showType = ref(props.transformation ? props.transformation.name : 'Sort')
const updateType = (value: string) => {
  showType.value = value
}

const handleCreateOrUpdate = (data: any) => {
  let body = null
  if (props.transformation) {
    body = { id: props.transformation.id, ...data }
  } else {
    body = { id: null, ...data }
  }

  sendToServer(ADD_TRANSFORMATION, { sourceId: props.sourceId, ...body })
  emit('close')
}
</script>

<template>
  <NCard>
    <div v-if="!props.transformation">
      <SSelectTransformation @update-type="updateType" :default="'Sort'" />
      <NDivider />
    </div>
    <div v-if="showType === 'Sort'">
      <SSort
        :editable="props.editable"
        :columns="props.schema?.fields"
        :transformation="props.transformation"
        @save="handleCreateOrUpdate"
      />
    </div>
    <div v-else-if="showType === 'Mask'"></div>
  </NCard>
</template>

<style></style>
