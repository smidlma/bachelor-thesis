<script setup lang="ts">
import { h, PropType, ref } from 'vue'
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
import useScocket from '../../use/socket'
import { SOURCE_SCHEMA_MAPPING } from '../../utils/commands'
const props = defineProps({
  sourceId: { type: String },
  defaultSchema: { type: Object as PropType<Schema> },
  mappedSchema: { type: Object as PropType<Schema>, default: { fields: [] } },
})

const { sendToServer } = useScocket()

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
  const data = props.defaultSchema?.fields.filter((x) =>
    rowKey.includes(x.name)
  )
  const msg = {
    sourceId: props.sourceId,
    schema: { fields: data, primaryKey: props.defaultSchema?.primaryKey },
  }
  console.log(msg)

  sendToServer(SOURCE_SCHEMA_MAPPING, msg)
}

const defaultSelectedKeys = props.mappedSchema.fields.map((x) => x.name)

// const test: Array<Field> = [{ name: 'name', type: 'string' }]
</script>

<template>
  <NGrid x-gap="12" cols="s:1 m:2" responsive="screen">
    <NGi>
      <NDataTable
        ref="table"
        :columns="columns"
        :data="props.defaultSchema?.fields"
        :row-key="(row:Field) => row.name"
        @update:checked-row-keys="toMapped"
        :default-checked-row-keys="defaultSelectedKeys"
      />
    </NGi>
    <NGi>
      <NDataTable
        ref="table2"
        :columns="columnsMapped"
        :data="props.mappedSchema.fields"
        :row-key="(row:Field) => row.name"
      />
    </NGi>
  </NGrid>
</template>

<style></style>
