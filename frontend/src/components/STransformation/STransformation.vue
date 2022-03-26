<script setup lang="ts">
import { NCard, NDivider, NButton, NDrawer, NDrawerContent } from 'naive-ui'
import { PropType, ref } from 'vue'
import { Schema } from '../../types/Pipeline'
import SSort from './SSort.vue'
import SSelectTransformation from './SSelectTransformation.vue'
import useSocket from '../../use/socket'
import { ADD_TRANSFORMATION } from '../../utils/commands'
import SMask from './SMask.vue'
const props = defineProps({
  sourceId: { type: String, required: false },
  transformation: { type: Object, default: null },
  schema: {
    type: Object as PropType<Schema>,
    default: {},
  },
  editable: { type: Boolean, default: false },
})
const emit = defineEmits(['close', 'edit'])
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

const activeDrawer = ref(false)
</script>

<template>
  <NCard :title="showType">
    <div v-if="!props.transformation">
      <SSelectTransformation @update-type="updateType" :default="'Sort'" />
    </div>
    <NButton v-if="!props.editable" @click="activeDrawer = true">Edit</NButton>
    <NDivider />
    <div v-if="showType === 'Sort'">
      <SSort
        :editable="props.editable"
        :columns="props.schema?.fields"
        :transformation="props.transformation"
        @save="handleCreateOrUpdate"
      />
    </div>
    <div v-else-if="showType === 'Mask'">
      <SMask
        :editable="props.editable"
        :columns="props.schema?.fields"
        :transformation="props.transformation"
        @save="handleCreateOrUpdate"
      />
    </div>
  </NCard>
  <NDrawer placement="right" :width="612" v-model:show="activeDrawer">
    <NDrawerContent>
      <template #header> Transformation configuration </template>
      <STransformation
        :transformation="props.transformation"
        :source-id="props.sourceId"
        :schema="props.schema"
        :editable="true"
        @close="activeDrawer = false"
      />
    </NDrawerContent>
  </NDrawer>
</template>

<style></style>
