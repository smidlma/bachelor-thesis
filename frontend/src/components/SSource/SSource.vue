<script setup lang="ts">
import { PropType } from 'vue'
import { Source } from '../../types/Pipeline'
import SSourceMapper from '../SSourceMapper/SSourceMapper.vue'

const props = defineProps({
  source: { type: Object as PropType<Source> },
})
</script>

<template>
  <div>
    <SSourceMapper
      :default-schema="props.source?.defaultSchema"
      :mapped-schema="props.source?.mappedSchema"
      :source-id="props.source?.id"
    />
  </div>
</template>

<style></style>
