<script setup lang="ts">
import {
  NForm,
  NSelect,
  NFormItem,
  FormInst,
  NButton,
  NSwitch,
  NInput,
} from 'naive-ui'
import { PropType, ref } from 'vue'
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
      emit('save', { type: 'Mask', ...formValue.value })
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
    </NForm>
    <NButton v-if="props.editable" @click="handleValidateClick"> Save</NButton>
  </template>
  <template v-else>
    <NFormItem label="Column">
      <NInput :value="props.transformation.column" :disabled="true"></NInput>
    </NFormItem>
  </template>
</template>

<style></style>
