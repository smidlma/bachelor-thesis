<script setup lang="ts">
import { NSelect, NCard } from 'naive-ui'

const options = ['Sort', 'Mask']

const selectOptions = options.map((x) => {
  return { label: x, value: x }
})

const emit = defineEmits(['updatType'])
</script>

<template>
  <NCard>
    <NSelect :options="selectOptions" @change="emit('updatType')"></NSelect>
  </NCard>
</template>

<style></style>
