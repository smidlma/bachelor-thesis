<script setup lang="ts">
import { NSelect } from 'naive-ui'

const props = defineProps({
  default: { type: String, default: 'Sort' },
})
const options = ['Sort', 'Mask']

const selectOptions = options.map((x) => {
  return { label: x, value: x }
})

const emit = defineEmits(['updateType'])
</script>

<template>
  <NSelect
    :default-value="props.default"
    :options="selectOptions"
    @update-value="(val) => emit('updateType', val)"
  ></NSelect>
</template>

<style></style>
