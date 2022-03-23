<script setup lang="ts">
import { h, PropType, Ref, ref } from 'vue'
import { Source } from '../../types/Pipeline'
import SSourceMapper from '../SSourceMapper/SSourceMapper.vue'
import SSourcePreview from '../SSourcePreview/SSourcePreview.vue'
import {
  NSpace,
  NButton,
  NDrawer,
  NDrawerContent,
  NText,
  NH1,
  NH2,
  NCollapseTransition,
  NSwitch,
  NCollapse,
  NCollapseItem,
  NIcon,
} from 'naive-ui'
import { ArrowDown } from '@vicons/ionicons5'
import SSourceConfig from '../SSourceConfig/SSourceConfig.vue'

const props = defineProps({
  source: { type: Object as PropType<Source> },
})

const activeDrawer: Ref<boolean> = ref(false)

const title = h(NH1, { prefix: 'bar' }, { default: () => 'hello' })
</script>

<template>
  <div>
    <NSpace vertical :size="30">
      <!-- <NButton @click="activeDrawer = true">Configure</NButton> -->
      <NCollapse
        arrow-placement="right"
        :default-expanded-names="['mapper', 'preview']"
      >
        <template #arrow> </template>
        <NCollapseItem name="mapper">
          <template #header>
            <NH2 prefix="bar" align-text>
              <NText type="primary">Source mapper </NText>
            </NH2>
          </template>
          <SSourceMapper
            :default-schema="props.source?.defaultSchema"
            :mapped-schema="props.source?.mappedSchema"
            :source-id="props.source?.id"
          />
        </NCollapseItem>
        <NCollapseItem name="preview">
          <template #header>
            <NH2 prefix="bar" align-text>
              <NText type="primary">Source preview </NText>
            </NH2>
          </template>
          <SSourcePreview
            :schema="props.source?.mappedSchema"
            :data="props.source?.preview"
          />
        </NCollapseItem>
        <NCollapseItem name="transformations">
          <template #header>
            <NH2 prefix="bar" align-text>
              <NText type="primary">Source transformations</NText>
            </NH2>
          </template>
        </NCollapseItem>
      </NCollapse>
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
