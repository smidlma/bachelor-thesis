<script setup lang="ts">
import {
  NForm,
  NSelect,
  NFormItem,
  FormInst,
  NButton,
  NInput,
  NSpace,
  NInputNumber,
  FormRules,
} from 'naive-ui'
import { computed, onUpdated, PropType, ref } from 'vue'
import Field from '../../types/Field'

const props = defineProps({
  columns: { type: Array as PropType<Array<Field>>, required: true },
  transformation: {
    type: Object,
    default: { column: null, op: 'gt', vals: [0, 0] },
  },
  editable: { type: Boolean, default: false },
})
const emit = defineEmits(['save'])

const formRef = ref<FormInst | null>(null)
const formValue = ref({
  column: props.transformation ? props.transformation.column : null,
  op: props.transformation ? props.transformation.op : null,
  vals: props.transformation ? props.transformation.vals : [0, 0],
})

const rules: FormRules = {
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
  vals: {
    type: 'array',
    required: true,
    message: 'Please select date',
    trigger: 'blur',
  },
}

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      console.log(formValue.value)
      emit('save', {
        type: 'ValueFilter',
        ...formValue.value,
      })
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
      <NFormItem label="Values" path="vals">
        <NSpace v-if="formValue.op === 'between'">
          <NInputNumber v-model:value="formValue.vals[0]" />
          <NInputNumber v-model:value="formValue.vals[1]" />
        </NSpace>
        <NInputNumber v-else v-model:value="formValue.vals[0]" />
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
    <NFormItem label="Values">
      <NSpace v-if="formValue.op === 'between'">
        <NInputNumber :value="props.transformation.vals[0]" :disabled="true" />
        <NInputNumber :value="props.transformation.vals[1]" :disabled="true" />
      </NSpace>
      <NInputNumber
        v-else
        :value="props.transformation.vals[0]"
        :disabled="true"
      />
    </NFormItem>
  </template>
</template>

<style></style>
