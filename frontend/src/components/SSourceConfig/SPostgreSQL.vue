<script setup lang="ts">
import {
  FormInst,
  FormRules,
  NForm,
  NFormItem,
  NInput,
  NButton,
  NSelect,
} from 'naive-ui'
import { PropType, ref } from 'vue'
import { Connection } from '../../types/Pipeline'
const props = defineProps({
  connectios: { type: Array as PropType<Connection[]>, required: true },
})
const emit = defineEmits(['add'])
const formRef = ref<FormInst | null>(null)
const rules: FormRules = {
  name: {
    required: true,
    message: 'Please input source name',
    trigger: 'blur',
  },
  connection: {
    required: true,
    message: 'Please select a file',
    trigger: 'blur',
  },
  tableName: {
    required: true,
    message: 'Please input table name',
    trigger: 'blur',
  },
}
const formValue = ref({
  name: null,
  connection: null,
  tableName: null,
})

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    emit('add', { sourceType: 'postgresql', ...formValue.value })
    if (!errors) {
    } else {
      console.log(errors)
    }
  })
}
</script>

<template>
  <NForm ref="formRef" :model="formValue" :rules="rules">
    <NFormItem label="Source name" path="name">
      <NInput
        v-model:value="formValue.name"
        placeholder="Name of the source"
      ></NInput>
    </NFormItem>
    <NFormItem label="Connection" path="connection">
      <NSelect
        v-model:value="formValue.connection"
        :options="
          props.connectios.map((x) => ({
            label: `${x.user}:###@${x.host}:${x.port}/${x.database}`,
            value: x.id,
          }))
        "
        placeholder="Select from defined connections"
      >
      </NSelect>
    </NFormItem>
    <NFormItem label="Table name" path="tableName">
      <NInput
        v-model:value="formValue.tableName"
        placeholder="Table name to extract from"
      ></NInput>
    </NFormItem>
  </NForm>
  <NButton @click="handleValidateClick">Add</NButton>
</template>
<style></style>
