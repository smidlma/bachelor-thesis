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
import FileType from '../../types/File'
const props = defineProps({
  files: { type: Array as PropType<FileType[]>, required: true },
})
const emit = defineEmits(['add'])
const formRef = ref<FormInst | null>(null)
const rules: FormRules = {
  name: {
    required: true,
    message: 'Please input source name',
    trigger: 'blur',
  },
  fileName: {
    required: true,
    message: 'Please select a file',
    trigger: 'blur',
  },
}
const formValue = ref({
  name: null,
  fileName: null,
})

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    emit('add', { sourceType: 'csv', ...formValue.value })
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
    <NFormItem label="File name" path="fileName">
      <NSelect
        placeholder="Select the file"
        :options="
          props.files.map((x) => {
            return { label: x.fileName, value: x.fileName }
          })
        "
        v-model:value="formValue.fileName"
      ></NSelect>
    </NFormItem>
  </NForm>
  <NButton @click="handleValidateClick">Add</NButton>
</template>
<style></style>
