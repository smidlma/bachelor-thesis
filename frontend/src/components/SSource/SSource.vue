<script setup lang="ts">
import { PropType, Ref, ref } from 'vue'
import { Source } from '../../types/Pipeline'
import SSourceMapper from '../SSourceMapper/SSourceMapper.vue'
import SSourcePreview from '../SSourcePreview/SSourcePreview.vue'
import { NSpace, NButton, NDrawer, NDrawerContent } from 'naive-ui'
import SSourceConfig from '../SSourceConfig/SSourceConfig.vue'

const props = defineProps({
  source: { type: Object as PropType<Source> },
})

const activeDrawer: Ref<boolean> = ref(false)
</script>

<template>
  <div>
    <NSpace vertical :size="30">
      <NButton @click="activeDrawer = true">Configure</NButton>
      <SSourceMapper
        :default-schema="props.source?.defaultSchema"
        :mapped-schema="props.source?.mappedSchema"
        :source-id="props.source?.id"
      />
      <SSourcePreview
        :schema="props.source?.mappedSchema"
        :data="props.source?.preview"
      />
    </NSpace>
    <!-- Drawer -->
    <NDrawer placement="right" :width="612" v-model:show="activeDrawer">
      <NDrawerContent>
        <template #header> Source configuration </template>
        <SSourceConfig />
      </NDrawerContent>
    </NDrawer>
    <!-- End of Drawer -->
  </div>
</template>

<style></style>
