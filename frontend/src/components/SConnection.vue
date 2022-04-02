<script setup lang="ts">
import {
  FormInst,
  NForm,
  NFormItem,
  NInput,
  NButton,
  NInputNumber,
  FormRules,
  NIcon,
  NCard,
  NIconWrapper,
  NPageHeader,
} from 'naive-ui'
import { PropType, ref } from 'vue'
import { Flash } from '@vicons/ionicons5'
import { Connection } from '../types/Pipeline'
import useRest from '../use/rest'
const props = defineProps({
  connection: {
    type: Object as PropType<Connection>,
    default: { host: '', port: null, user: '', password: '', database: '' },
  },
  editable: { type: Boolean, default: false },
  preview: { type: Boolean, default: false },
})

const emit = defineEmits(['connectionStatus'])
const rest = useRest()
const formRef = ref<FormInst | null>(null)
const formValue = ref({
  host: props.connection.host,
  port: props.connection.port,
  user: props.connection.user,
  password: props.connection.password,
  database: props.connection.database,
})

const rules: FormRules = {
  host: {
    required: true,
    message: 'Please input host name',
    trigger: 'blur',
  },
  port: {
    required: true,
    type: 'number',
    trigger: 'blur',
    message: 'Please input port',
  },
  user: {
    required: true,
    message: 'Please input user',
    trigger: 'blur',
  },
  password: {
    required: false,
    message: 'Please input password',
    trigger: 'blur',
  },
  database: {
    required: true,
    message: 'Please input database',
    trigger: 'blur',
  },
}

const handleValidateClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      validateConnection()
    } else {
      console.log(errors)
      // message.error('Invalid')
    }
  })
}

const validateConnection = async () => {
  const result = await rest.testConnection(formValue.value)
  emit('connectionStatus', result)
}
</script>

<template>
  <NForm
    v-if="!props.preview"
    ref="formRef"
    :label-width="80"
    :model="formValue"
    :rules="rules"
    :disabled="!editable"
    :show-require-mark="editable"
  >
    <NFormItem label="Host" path="host">
      <NInput v-model:value="formValue.host" placeholder="Input host" />
    </NFormItem>
    <NFormItem label="Port" path="port">
      <NInputNumber
        v-model:value="formValue.port"
        placeholder="Input port"
        :show-button="false"
      />
    </NFormItem>
    <NFormItem label="User" path="user">
      <NInput
        v-model:value="formValue.user"
        placeholder="User name"
      /> </NFormItem
    ><NFormItem label="Password" path="password" :show-require-mark="false">
      <NInput
        v-model:value="formValue.password"
        placeholder="Password"
        type="password"
        show-password-on="mousedown"
      />
    </NFormItem>
    <NFormItem label="Target Database" path="database">
      <NInput v-model:value="formValue.database" placeholder="Database name" />
    </NFormItem>
    <NFormItem v-if="editable">
      <NButton @click="handleValidateClick"> Test Connection </NButton>
    </NFormItem>
  </NForm>
  <NCard v-else>
    <NPageHeader
      :subtitle="`${props.connection.user}:###@${props.connection.host}:${props.connection.port}/${props.connection.database}`"
    >
      <template #title>Connection: </template>
      <template #avatar>
        <NIconWrapper color="rgba(99, 226, 183, 0.16)" :size="40">
          <NIcon :size="32" color="#63e2b7">
            <Flash />
          </NIcon>
        </NIconWrapper>
        <!-- <NAvatar
          src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
        /> -->
      </template>
      <template #extra>
        <!-- <NSpace>
          <NButton v-if="!props.editor" @click="emit('open', props.pipeline.id)"
            >Open</NButton
          >
          <NSpace v-else>
            <NButton @click="emit('run', props.pipeline.id)">Run</NButton>
            <NButton @click="emit('close', props.pipeline.id)">Close</NButton>
          </NSpace>
        </NSpace> -->
      </template>
    </NPageHeader>
  </NCard>
</template>
<style></style>
