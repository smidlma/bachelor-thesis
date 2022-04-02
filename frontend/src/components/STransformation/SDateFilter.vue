<script setup lang="ts">
import {
  NForm,
  NSelect,
  NFormItem,
  FormInst,
  NButton,
  NSwitch,
  NInput,
  NSpace,
  NDatePicker,
  FormRules,
} from 'naive-ui'
import { computed, onUpdated, PropType, ref } from 'vue'
import Field from '../../types/Field'

const props = defineProps({
  columns: { type: Array as PropType<Array<Field>>, required: true },
  transformation: { type: Object, default: { column: null, ascending: true } },
  editable: { type: Boolean, default: false },
})
const emit = defineEmits(['save'])

const formRef = ref<FormInst | null>(null)
const formValue = ref({
  column: props.transformation ? props.transformation.column : null,
  op: props.transformation ? props.transformation.op : null,
  datetimes: props.transformation ? props.transformation.datetimes : null,
})

const rules = computed<FormRules>(() => {
  return {
    column: {
      required: true,
      message: 'Please select column',
      trigger: 'blur',
    },
    op: {
      required: true,
      message: 'Please select operator',
      trigger: 'blur',
    },
    datetimes: {
      type: formValue.value.op === 'between' ? 'array' : 'number',
      required: true,
      message: 'Please select date',
      trigger: 'blur',
    },
  }
})

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      console.log(formValue.value)

      if (formValue.value.op === 'between') {
        emit('save', {
          type: 'DateFilter',
          ...formValue.value,
        })
      } else {
        emit('save', {
          type: 'DateFilter',
          column: formValue.value.column,
          op: formValue.value.op,
          datetimes: [formValue.value.datetimes],
        })
      }
    } else {
      console.log(errors)
    }
  })
}
</script>
<template>
  <template v-if="props.editable">
    <NForm
      ref="formRef"
      :model="formValue"
      :rules="rules"
      :disabled="!props.editable"
      :show-require-mark="props.editable"
    >
      <NFormItem path="column" label="Column">
        <NSelect
          :options="
            props.columns.map((x) => {
              return { label: x.name, value: x.name }
            })
          "
          v-model:value="formValue.column"
        ></NSelect>
      </NFormItem>
      <NFormItem label="Operator" path="op">
        <NSelect
          :options="[
            { label: 'gt', value: 'gt' },
            { label: 'lt', value: 'lt' },
            { label: 'between', value: 'between' },
          ]"
          v-model:value="formValue.op"
        ></NSelect>
      </NFormItem>
      <NFormItem label="Dates" path="datetimes">
        <NDatePicker
          v-if="formValue.op === 'between'"
          v-model:value="formValue.datetimes"
          type="datetimerange"
          clearable
        />
        <NDatePicker
          v-else
          v-model:value="formValue.datetimes"
          type="datetime"
          clearable
        />
      </NFormItem>
    </NForm>
    <NButton v-if="props.editable" @click="handleValidateClick"> Save</NButton>
  </template>
  <template v-else>
    <NFormItem label="Column">
      <NInput :value="props.transformation.column" :disabled="true"></NInput>
    </NFormItem>
    <NFormItem label="Operator">
      <NInput :value="props.transformation.op" :disabled="true" />
    </NFormItem>
    <NFormItem label="Dates">
      <NDatePicker
        v-if="props.transformation.op === 'between'"
        :value="props.transformation.datetimes"
        type="datetimerange"
        :disabled="true"
      />
      <NDatePicker
        v-else
        :value="props.transformation.datetimes[0]"
        type="datetime"
        :disabled="true"
      />
    </NFormItem>
  </template>
</template>

<style></style>
