<script setup lang="ts">
import { computed, onMounted, ref, Ref } from 'vue'
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
  NDrawer,
  NDrawerContent,
  NEmpty,
  useMessage,
} from 'naive-ui'
import SSource from '../components/SSource/SSource.vue'
import SSourceConfig from '../components/SSourceConfig/SSourceConfig.vue'
import SDestination from '../components/SDestination/SDestination.vue'
import SDestinationConfig from '../components/SDestinationConfig.vue'
import SJoin from '../components/SJoin/SJoin.vue'
import SPipeline from '../components/SPipeline/SPipeline.vue'
import useSocket from '../use/socket'
import {
  ADD_DESTINATION,
  CLOSE_PIPELINE,
  RUN_PIPELINE,
} from '../utils/commands'
import { useRouter } from 'vue-router'

const store = useStore()

const pipeline = computed(() => store.getters.currentPipeline)

// const sources = computed(() => log)

const activeDrawer: Ref<boolean> = ref(false)
const configItem: Ref<string> = ref('source')

const openConfig = (item: string) => {
  configItem.value = item
  activeDrawer.value = true
}
const message = useMessage()

onMounted(() => message.success('mounted'))
const socket = useSocket()
const closePipeline = (id: string) => {
  socket.sendToServer(CLOSE_PIPELINE, { id })
}

const runPipeline = () => {
  socket.sendToServer(RUN_PIPELINE, {})
  // closePipeline(pipeline.value.id)
}

const router = useRouter()
const goToPipelines = () => {
  router.push({ name: 'Pipelines' })
}

const updateDestination = (dest: any) => {
  socket.sendToServer(ADD_DESTINATION, dest)
  activeDrawer.value = false
}
</script>

<template>
  <template v-if="pipeline">
    <SPipeline
      :pipeline="pipeline"
      :card="true"
      :editor="true"
      @close="closePipeline"
      @run="runPipeline"
    />
    <NDivider></NDivider>
    <NCard title="Sources">
      <template #header-extra>
        <NButton @click="openConfig('source')">Add Source</NButton>
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
        <NButton
          @click="openConfig('join')"
          :disabled="
            pipeline.sources.length === 1 ||
            pipeline.sources.length - 1 === pipeline.joins.length
          "
          >Add Join</NButton
        >
      </template>
      <NSpace size="large" vertical>
        <SJoin
          v-for="(item, index) in pipeline.joins"
          :key="index"
          :join="item"
          :sources="pipeline.sources"
          :editable="false"
        />
      </NSpace>
    </NCard>
    <NDivider></NDivider>
    <NCard title="Destination">
      <template #header-extra>
        <NButton @click="openConfig('destination')">Configure</NButton>
      </template>
      <SDestination :destination="pipeline.destination" />
    </NCard>
    <!-- Drawer -->
    <NDrawer placement="right" :width="612" v-model:show="activeDrawer">
      <NDrawerContent>
        <template v-if="configItem === 'source'" #header>
          Source configuration
        </template>
        <template v-else-if="configItem === 'destination'" #header>
          Destination configuration
        </template>
        <template v-else-if="configItem === 'join'" #header>
          Join configuration
        </template>

        <div v-if="configItem === 'source'">
          <SSourceConfig />
        </div>
        <div v-else-if="configItem === 'destination'">
          <SDestination
            :destination="pipeline.destination"
            :editable="true"
            @update="updateDestination"
          />
        </div>
        <div v-else-if="configItem === 'join'">
          <SJoin
            :sources="pipeline.sources"
            :editable="true"
            @add="activeDrawer = false"
          />
        </div>
      </NDrawerContent>
    </NDrawer>
    <!-- End of Drawer -->
  </template>
  <template v-else>
    <NEmpty description="All pipelines are closed" style="padding-top: 48px">
      <template #extra>
        <NButton size="medium" @click="goToPipelines"> Show Pipelines </NButton>
      </template>
    </NEmpty>
  </template>
</template>

<style></style>
