<script setup lang="ts">
import { computed, onMounted, ref, Ref } from 'vue'
import { useStore } from 'vuex'

import {
  NCard,
  NTabs,
  NTabPane,
  NButton,
  NDivider,
  NSpace,
  NDrawer,
  NDrawerContent,
  NEmpty,
  NSkeleton,
  useNotification,
} from 'naive-ui'
import SSource from '../components/SSource/SSource.vue'
import SSourceConfig from '../components/SSourceConfig/SSourceConfig.vue'
import SDestination from '../components/SDestination/SDestination.vue'
import SJoin from '../components/SJoin/SJoin.vue'
import SPipeline from '../components/SPipeline/SPipeline.vue'
import useSocket from '../use/socket'
import { ADD_DESTINATION, CLOSE_PIPELINE } from '../utils/commands'
import { useRouter } from 'vue-router'
import useRest from '../use/rest'

const store = useStore()
const rest = useRest()
const pipeline = computed(() => store.getters.currentPipeline)

const activeDrawer: Ref<boolean> = ref(false)
const configItem: Ref<string> = ref('source')

const openConfig = (item: string) => {
  configItem.value = item
  activeDrawer.value = true
}
const notification = useNotification()
const loading = ref(true)

onMounted(() => {
  setTimeout(() => (loading.value = false), 500)
})
const socket = useSocket()
const closePipeline = (id: string) => {
  socket.sendToServer(CLOSE_PIPELINE, { id })
}

const runPipeline = async (id: string) => {
  // socket.sendToServer(RUN_PIPELINE, {})
  store.commit('addRunningPipeline', id)
  goToPipelines()
  notification.success({ content: 'Starting pipeline', duration: 2000 })
  const res = await rest.runPipeline(id)
  if (res.success) {
    notification.success({
      content: `${res.message}`,
      duration: 5000,
    })
  } else {
    notification.error({
      content: `Error: ${res.error}`,
    })
  }
  store.commit('removeRunningPipeline', id)
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
  <div v-if="!loading">
    <template v-if="pipeline">
      <SPipeline
        :pipeline="pipeline"
        :card="true"
        :editor="true"
        @close="closePipeline"
        @run="runPipeline(pipeline.id)"
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
            :sources="[...pipeline.sources, ...pipeline.joins]"
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
              :sources="[...pipeline.sources, ...pipeline.joins]"
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
          <NButton size="medium" @click="goToPipelines">
            Show Pipelines
          </NButton>
        </template>
      </NEmpty>
    </template>
  </div>
  <div v-else>
    <NDivider />
    <NSpace vertical size="large">
      <NSkeleton :sharp="false" height="50px" />
      <NSkeleton :sharp="false" height="250px" />
      <NSkeleton :sharp="false" height="450px" />
      <NSkeleton :sharp="false" height="250px" />
    </NSpace>
  </div>
</template>

<style></style>
