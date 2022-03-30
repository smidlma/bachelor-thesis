<script setup lang="ts">
import { NForm, NFormItem, NInput } from 'naive-ui'
import { PropType, ref } from 'vue'
import { Destination } from '../types/Pipeline'
import SConnection from './SConnection.vue'

const props = defineProps({
  destination: { type: Object as PropType<Destination> },
})

const handleUpdate = (status: Object) => {
  console.log('status', status)
}

const targetTable = ref(props.destination?.targetTable)
</script>

<template>
  <NInput v-model:value="targetTable" />
  <SConnection
    :connection="props.destination?.connection"
    :editable="true"
    @connection-status="handleUpdate"
  />
</template>
<style></style>
