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
  NEmpty,
} from 'naive-ui'
import { Add } from '@vicons/ionicons5'
import SSourceConfig from '../SSourceConfig/SSourceConfig.vue'
import STransformation from '../STransformation/STransformation.vue'

const props = defineProps({
  source: { type: Object as PropType<Source>, required: true },
})

const activeDrawer: Ref<boolean> = ref(false)
const configItem = ref('')

const openDrawer = (config: string) => {
  configItem.value = config
  activeDrawer.value = true
}
</script>

<template>
  <div>
    <NSpace vertical :size="30">
      <!-- <NButton @click="activeDrawer = true">Configure</NButton> -->
      <NCollapse
        arrow-placement="right"
        :default-expanded-names="['mapper', 'preview', 'transformations']"
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
          <NSpace vertical>
            <STransformation
              v-for="(t, index) in props.source?.transformations"
              :key="index"
              :transformation="t"
              :schema="props.source?.mappedSchema"
              :source-id="props.source.id"
            />
            <NEmpty description="Add">
              <template #icon>
                <NIcon>
                  <Add />
                </NIcon>
              </template>
              <template #extra>
                <NButton size="large" @click="openDrawer('transformation')">
                  Select transformation
                </NButton>
              </template>
            </NEmpty>
          </NSpace>
        </NCollapseItem>
      </NCollapse>
    </NSpace>
    <!-- Drawer -->
    <NDrawer placement="right" :width="612" v-model:show="activeDrawer">
      <NDrawerContent>
        <template v-if="configItem === 'source'" #header>
          Source configuration
        </template>
        <template v-else-if="configItem === 'transformation'" #header>
          Transformation configuration
        </template>

        <SSourceConfig v-if="configItem === 'source'" />
        <STransformation
          v-else-if="configItem === 'transformation'"
          :source-id="props.source.id"
          :schema="props.source?.mappedSchema"
          :editable="true"
          @close="activeDrawer = false"
        />
      </NDrawerContent>
    </NDrawer>
    <!-- End of Drawer -->
  </div>
</template>

<style></style>
