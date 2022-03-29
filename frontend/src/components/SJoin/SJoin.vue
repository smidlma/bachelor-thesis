<script setup lang="ts">
import { FormInst, NForm, NFormItem, NSelect, NCard, NButton } from 'naive-ui'
import { PropType, ref } from 'vue'
import { Join, Source } from '../../types/Pipeline'
import SSourcePreview from '../SSourcePreview/SSourcePreview.vue'
import useSocket from '../../use/socket'
import { ADD_JOIN } from '../../utils/commands'
import { Add } from '@vicons/ionicons5'
const props = defineProps({
  editable: { type: Boolean, default: false },
  join: {
    type: Object as PropType<Join>,
    default: {
      s1: { id: null },
      s2: { id: null },
      how: null,
      on: null,
    },
  },
  sources: { type: Array as PropType<Array<Source>>, default: [] },
})
const socket = useSocket()

const emit = defineEmits(['add'])
const createForm = ref({
  s1: props.join?.s1.id,
  s2: props.join?.s2.id,
  how: props.join?.how,
})

const formRef = ref<FormInst | null>(null)

const rules = {
  s1: {
    required: true,
    trigger: ['blur', 'change'],
    message: 'Please select source',
  },
  s2: {
    required: true,
    trigger: ['blur', 'change'],
    message: 'Please select source',
  },
  how: {
    required: true,
    trigger: ['blur', 'change'],
    message: 'Please select type of join',
  },
}

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      //   message.success('Valid')
      socket.sendToServer(ADD_JOIN, { ...createForm.value })
      emit('add')
    } else {
      console.log(errors)
      //   message.error('Invalid')
    }
  })
}
</script>

<template>
  <NCard>
    <NForm
      ref="formRef"
      :model="createForm"
      :rules="rules"
      :disabled="!props.editable"
      :show-require-mark="props.editable"
    >
      <NFormItem label="Source 1" path="s1">
        <NSelect
          clearable
          :options="
            props.sources
              .map((x) => {
                return { label: x.name, value: x.id }
              })
              .filter((x) => x.value !== createForm.s2)
          "
          v-model:value="createForm.s1"
        ></NSelect>
      </NFormItem>
      <NFormItem label="Source 2" path="s2">
        <NSelect
          :options="
            props.sources
              .map((x) => {
                return { label: x.name, value: x.id }
              })
              .filter((x) => x.value !== createForm.s1)
          "
          v-model:value="createForm.s2"
          clearable
        ></NSelect>
      </NFormItem>
      <NFormItem label="How to join" path="how">
        <NSelect
          clearable
          :options="[
            { label: 'left', value: 'left' },
            { label: 'right', value: 'right' },
            { label: 'outer', value: 'outer' },
            { label: 'inner', value: 'inner' },
          ]"
          v-model:value="createForm.how"
        ></NSelect>
      </NFormItem>
      <!-- <NFormItem label="On"></NFormItem> -->
    </NForm>
    <NButton v-if="props.editable" @click="handleValidateClick">Save</NButton>
    <!-- <SSourcePreview
      :schema="props.join.defaultSchema"
      :data="props.join.preview"
    /> -->
  </NCard>
</template>

<style></style>
