<script setup lang="ts">
import { onMounted, PropType, ref } from 'vue'
import { Connection, Destination } from '../../types/Pipeline'
import {
  NInput,
  NForm,
  NFormItem,
  FormInst,
  FormRules,
  NSelect,
  NButton,
} from 'naive-ui'
import SConnection from '../SConnection.vue'
import { insertOptions } from '../../utils/pandas'
import useRest from '../../use/rest'
const props = defineProps({
  destination: { type: Object as PropType<Destination> },
  editable: { type: Boolean, default: false },
})
const emit = defineEmits(['update'])

const rest = useRest()
const formRef = ref<FormInst | null>(null)
const formValue = ref({
  name: props.destination?.destinationName,
  connection: props.destination?.connection.id,
  targetTable: props.destination?.targetTable,
  insertOption: props.destination?.insertOption,
})
const rules: FormRules = {
  name: {
    required: true,
    message: 'Please input destination name',
    trigger: 'blur',
  },
  connection: {
    required: true,
    message: 'Please select connection',
    trigger: 'blur',
  },
  targetTable: {
    required: true,
    message: 'Please input target table',
    trigger: 'blur',
  },
  insertOption: {
    required: true,
    message: 'Please select inser option',
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
      emit('update', { id: props.destination?.id, ...formValue.value })
    } else {
      console.log(errors)
    }
  })
}
</script>

<template>
  <NForm
    ref="formRef"
    :model="formValue"
    :rules="rules"
    :disabled="!props.editable"
  >
    <NFormItem label="Name" path="name">
      <NInput v-model:value="formValue.name" />
    </NFormItem>
    <NFormItem label="Connection" path="connection">
      <NSelect
        v-model:value="formValue.connection"
        :options="
          connections?.map((x) => {
            return {
              label: `${x.user}:###@${x.host}:${x.port}/${x.database}`,
              value: x.id,
            }
          })
        "
      />
    </NFormItem>
    <NFormItem label="Target table" path="targetTable">
      <NInput v-model:value="formValue.targetTable" />
    </NFormItem>
    <NFormItem label="Inser Options" path="insertOption">
      <NSelect
        v-model:value="formValue.insertOption"
        :options="insertOptions"
      />
    </NFormItem>
  </NForm>
  <NButton v-if="props.editable" @click="handleValidateClick">Save</NButton>
</template>
<style></style>
