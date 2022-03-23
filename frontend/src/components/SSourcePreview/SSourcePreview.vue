<script setup lang="ts">
import { NDataTable, NResult, NEmpty, NCard } from 'naive-ui'
import { computed, PropType } from 'vue'
import { Schema } from '../../types/Pipeline'

const props = defineProps({
  schema: { type: Object as PropType<Schema> },
  data: { type: Array as PropType<Array<any>> },
})

const columns = computed(() =>
  props.schema?.fields.map((x) => {
    return { title: x.name.toUpperCase(), key: x.name }
  })
)
</script>

<template>
  <div style="padding-bottom: 18px">
    <NDataTable
      v-if="columns && columns.length > 0"
      :columns="columns"
      :data="props.data"
    />

    <n-card v-else>
      <NResult
        status="info"
        title="Use source mapper"
        description="To show data preview, you have to map source columns"
      >
      </NResult>
    </n-card>
  </div>
</template>

<style></style>
