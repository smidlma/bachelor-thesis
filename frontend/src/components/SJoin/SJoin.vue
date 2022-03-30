<script setup lang="ts">
import {
  FormInst,
  NForm,
  NFormItem,
  NSelect,
  NCard,
  NButton,
  NDrawer,
  NDrawerContent,
  NDivider,
} from 'naive-ui'
import { PropType, ref } from 'vue'
import { Join, Source } from '../../types/Pipeline'
import useSocket from '../../use/socket'
import { ADD_JOIN } from '../../utils/commands'
const props = defineProps({
  editable: { type: Boolean, default: false },
  join: {
    type: Object as PropType<Join>,
    default: {
      id: null,
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

const activeDrawer = ref(false)
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

const handleCreateOrUpdate = (data: any) => {
  let body = null
  if (props.join.id) {
    body = { id: props.join.id, ...data }
  } else {
    body = { id: null, ...data }
  }

  socket.sendToServer(ADD_JOIN, body)
}

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      handleCreateOrUpdate(createForm.value)
      emit('add')
    } else {
      console.log(errors)
    }
  })
}
</script>

<template>
  <NCard>
    <NButton v-if="!props.editable" @click="activeDrawer = true">Edit</NButton>
    <NDivider></NDivider>
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
    <NDrawer placement="right" :width="612" v-model:show="activeDrawer">
      <NDrawerContent>
        <template #header> Join configuration </template>
        <SJoin :join="props.join" :sources="props.sources" :editable="true" />
      </NDrawerContent>
    </NDrawer>
    <!-- <SSourcePreview
      :schema="props.join.defaultSchema"
      :data="props.join.preview"
    /> -->
  </NCard>
</template>

<style></style>
