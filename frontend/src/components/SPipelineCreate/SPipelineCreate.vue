<script setup lang="ts">
import {
  FormInst,
  FormRules,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NButton,
} from 'naive-ui'
import { onMounted, ref } from 'vue'
import { Connection } from '../../types/Pipeline'
import useRest from '../../use/rest'
import { insertOptions } from '../../utils/pandas'
const emit = defineEmits(['create'])
const rest = useRest()
const formRef = ref<FormInst | null>(null)
const formValue = ref({
  pipelineName: null,
  destinationName: null,
  connectionId: null,
  targetTable: null,
  insertOption: null,
})
const rules: FormRules = {
  pipelineName: {
    required: true,
    message: 'Please input pipeline name',
    trigger: 'blur',
  },
  destinationName: {
    required: true,
    message: 'Please input destination name',
    trigger: 'blur',
  },
  connectionId: {
    required: true,
    message: 'Please select connection',
    trigger: 'blur',
  },
  targetTable: {
    required: true,
    message: 'Please input target table name',
    trigger: 'blur',
  },
  insertOption: {
    required: true,
    message: 'Please select connection',
    trigger: 'blur',
  },
}
const connections = ref<Array<Connection>>()
onMounted(async () => {
  connections.value = await rest.getConnections()
})

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      emit('create', {
        ...formValue.value,
        //@ts-ignore
        targetTable: formValue.value.targetTable
          .toLowerCase()
          .replace(/\s/g, ''),
      })
    } else {
      console.log(errors)
    }
  })
}
</script>

<template>
  <NForm ref="formRef" :model="formValue" :rules="rules">
    <NFormItem label="Pipeline name" path="pipelineName">
      <NInput v-model:value="formValue.pipelineName" />
    </NFormItem>
    <NFormItem label="Destination name" path="destinationName">
      <NInput v-model:value="formValue.destinationName" />
    </NFormItem>
    <NFormItem label="Connection" path="connectionId">
      <NSelect
        :options="
          connections?.map((x) => {
            return {
              label: `${x.user}:###@${x.host}:${x.port}/${x.database}`,
              value: x.id,
            }
          })
        "
        v-model:value="formValue.connectionId"
      />
    </NFormItem>
    <NFormItem label="Target table" path="targetTable">
      <NInput v-model:value="formValue.targetTable" />
    </NFormItem>
    <NFormItem label="Insert options" path="insertOption">
      <NSelect
        :options="insertOptions"
        v-model:value="formValue.insertOption"
      />
    </NFormItem>
    <NButton @click="handleValidateClick">Create</NButton>
  </NForm>
</template>

<style></style>
