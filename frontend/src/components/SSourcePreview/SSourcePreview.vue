<script setup lang="ts">
import { NDataTable } from 'naive-ui'
import { computed, PropType } from 'vue'
import { Schema } from '../../types/Pipeline'

const props = defineProps({
  schema: { type: Object as PropType<Schema> },
  data: { type: Array as PropType<Array<any>> },
})

const columns = computed(() =>
  props.schema?.fields.map((x) => {
    return { title: x.name.toUpperCase(), key: x.name.toLowerCase() }
  })
)
</script>

<template>
  <div>
    <n-data-table :columns="columns" :data="props.data" />
  </div>
</template>

<style></style>
