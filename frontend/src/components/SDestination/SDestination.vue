<script setup lang="ts">
import { PropType, ref } from 'vue'
import { Destination } from '../../types/Pipeline'
import {
  NDrawer,
  NDrawerContent,
  NButton,
  NDescriptions,
  NDescriptionsItem,
  NSpace,
  NInput,
} from 'naive-ui'
import SConnection from '../SConnection.vue'

const props = defineProps({
  destination: { type: Object as PropType<Destination> },
})

// console.log(props.destination)
</script>

<template>
  <SConnection :connection="props.destination?.connection" :editable="false" />
</template>
<style></style>
