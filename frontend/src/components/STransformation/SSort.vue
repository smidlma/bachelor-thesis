<script setup lang="ts">
import { NForm, NSelect, NFormItem } from 'naive-ui'
import { PropType } from 'vue'

const props = defineProps({
  columns: { type: Array as PropType<Array<String>>, default: [] },
  tSort: { type: Object, default: { column: null, ascending: true } },
  editable: { type: Boolean, default: false },
})

const formRef = null

const form = {
  column: props.tSort.column,
  ascending: props.tSort.column,
}
</script>
<template>
  <NForm :disabled="!props.editable" :show-require-mark="props.editable">
    <NFormItem>
      <NSelect
        :options="
          props.columns.length > 0
            ? props.columns.map((x) => {
                return { label: x, value: x }
              })
            : []
        "
      ></NSelect>
    </NFormItem>
    <NFormItem>
      <NSelect></NSelect>
    </NFormItem>
  </NForm>
</template>

<style></style>
