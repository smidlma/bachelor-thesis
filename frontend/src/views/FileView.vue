<script setup lang="ts">
import {
  NPageHeader,
  NSpace,
  NButton,
  NAvatar,
  NEmpty,
  NGrid,
  NGi,
  NDivider,
} from 'naive-ui'
import { ref } from 'vue'
import SFile from '../components/SFile/SFile.vue'
import FileType from '../types/File'

const files = ref<FileType[]>([
  { fileName: 'Patients.csv', fileSize: '100MB' },
  { fileName: 'Patients.csv', fileSize: '100MB' },
  { fileName: 'Patients.csv', fileSize: '100MB' },
])
</script>
<template>
  <div>
    <NPageHeader :subtitle="`Uploaded files:    ${files.length}`">
      <template #title>Uploaded Files</template>
      <template #avatar>
        <NAvatar
          src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
        />
      </template>
      <template #extra>
        <NSpace>
          <NButton>Upload</NButton>
        </NSpace>
      </template>
    </NPageHeader>
    <NDivider></NDivider>
    <template v-if="!files.length">
      <NEmpty description="You can't find anything">
        <template #extra>
          <NButton size="small">Refresh</NButton>
        </template>
      </NEmpty>
    </template>
    <template v-else>
      <NGrid x-gap="12" cols="1 s:1 m:3 l:3 xl:6" responsive="screen">
        <NGi v-for="(file, index) in files" :key="index">
          <SFile :file-name="file.fileName" :file-size="file.fileSize"></SFile>
        </NGi>
      </NGrid>
    </template>
  </div>
</template>

<style></style>
