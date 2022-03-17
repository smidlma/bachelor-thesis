<script setup lang="ts">
import { computed } from 'vue'
import { useStore } from 'vuex'

import {
  NCard,
  NTabs,
  NTabPane,
  NButton,
  NDivider,
  NPageHeader,
  NAvatar,
  NSpace,
} from 'naive-ui'
import SSource from '../components/SSource/SSource.vue'

const store = useStore()

const pipeline = computed(() => store.getters.currentPipeline)
</script>

<template>
  <template v-if="pipeline">
    <NPageHeader :subtitle="`Uploaded files:`">
      <template #title>Pipeline: </template>
      <template #avatar>
        <NAvatar
          src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
        />
      </template>
      <template #extra>
        <NSpace>
          <NButton>Hello World</NButton>
        </NSpace>
      </template>
    </NPageHeader>
    <NDivider></NDivider>
    <NCard title="Sources">
      <template #header-extra>
        <NButton>Add Source</NButton>
      </template>
      <NTabs type="line" size="large">
        <NTabPane
          display-directive="if"
          v-for="(item, index) in pipeline.sources"
          :key="index"
          :name="item.name"
        >
          <SSource :source="item" />
        </NTabPane>
      </NTabs>
    </NCard>
    <NDivider></NDivider>
    <NCard title="Joins">
      <template #header-extra>
        <NButton>Add Join</NButton>
      </template>
      Joins
    </NCard>
    <NDivider></NDivider>
    <NCard title="Destination">
      <template #header-extra>
        <NButton>Configure</NButton>
      </template>
      Dest
    </NCard>
  </template>
  <template v-else> No pipeline opened </template>
</template>

<style></style>
