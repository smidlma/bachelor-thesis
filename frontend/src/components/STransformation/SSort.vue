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
} from 'naive-ui'
import { computed, onUpdated, PropType, ref } from 'vue'
import Field from '../../types/Field'

const props = defineProps({
  columns: { type: Array as PropType<Array<Field>>, required: true },
  transformation: { type: Object, default: { column: null, ascending: 1 } },
  editable: { type: Boolean, default: false },
})
const emit = defineEmits(['save'])

const formRef = ref<FormInst | null>(null)
const formValue = ref({
  column: props.transformation ? props.transformation.column : null,
  ascending: props.transformation ? props.transformation.ascending : true,
})

const rules = {
  column: {
    required: true,
    message: 'Please select column',
    trigger: 'blur',
  },
}

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      emit('save', { type: 'Sort', ...formValue.value })
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
      <NFormItem label="Order">
        <NSwitch v-model:value="formValue.ascending">
          <template #checked> ASC </template>
          <template #unchecked> DESC </template>
        </NSwitch>
      </NFormItem>
    </NForm>
    <NButton v-if="props.editable" @click="handleValidateClick"> Save</NButton>
  </template>
  <template v-else>
    <NFormItem label="Column">
      <NInput :value="props.transformation.column" :disabled="true"></NInput>
    </NFormItem>
    <NFormItem label="Order">
      <NSwitch :value="props.transformation.ascending" :disabled="true">
        <template #checked> ASC </template>
        <template #unchecked> DESC </template>
      </NSwitch>
    </NFormItem>
  </template>
</template>

<style></style>
