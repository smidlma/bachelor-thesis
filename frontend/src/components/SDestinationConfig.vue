<script setup lang="ts">
import { PropType } from 'vue'
import { Destination } from '../types/Pipeline'
import SConnection from './SConnection.vue'

const props = defineProps({
  destination: { type: Object as PropType<Destination> },
})
</script>

<template>
  <SConnection :connection="props.destination?.connection" :editable="true" />
</template>
<style></style>
