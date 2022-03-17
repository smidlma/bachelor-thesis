<script setup lang="ts">
import { computed, h, onMounted, PropType, ref, watch } from 'vue'
import { Schema } from '../../types/Pipeline'
import { pandasDataTypes } from '../../utils/pandas'
import type Field from '../../types/Field'
import {
  NDataTable,
  NGrid,
  NGi,
  DataTableColumns,
  NTag,
  NSelect,
} from 'naive-ui'

const props = defineProps({
  defaultSchema: { type: Object as PropType<Schema> },
  mappedSchema: { type: Object as PropType<Schema>, default: { fields: [] } },
})

const columns: DataTableColumns<Field> = [
  {
    type: 'selection',
  },
  {
    title: 'Name',
    key: 'name',
  },
  {
    title: 'Type',
    key: 'type',
    render(row) {
      return h(
        NTag,
        { type: 'success' },
        {
          default: () => row.type,
        }
      )
    },
  },
]

const columnsMapped: DataTableColumns<Field> = [
  {
    title: 'Name',
    key: 'name',
  },
  {
    title: 'Type',
    key: 'type',
    render(row) {
      return h(NSelect, {
        value: row.type,
        options: pandasDataTypes,
        onUpdateValue: (value) => {
          const temp = { ...row, newType: value }
          console.log(temp)
        },
      })
    },
  },
]

const toMapped = (rowKey: any) => {
  console.log(rowKey)
}

// const test: Array<Field> = [{ name: 'name', type: 'string' }]

const checked = ref([])

// console.log(props.defaultSchema?.fields.map((x) => x.name))
</script>

<template>
  <NGrid x-gap="12" cols="s:1 m:2" responsive="screen">
    <NGi>
      <NDataTable
        ref="table"
        :columns="columns"
        :data="defaultSchema?.fields"
        :row-key="(row:Field) => row.name"
        @update:checked-row-keys="toMapped"
      />
    </NGi>
    <NGi>
      <NDataTable
        ref="table2"
        :columns="columnsMapped"
        :data="mappedSchema.fields"
        :row-key="(row:Field) => row.name"
      />
    </NGi>
  </NGrid>
</template>

<style></style>
