<script setup lang="ts">
import {
  NPageHeader,
  NSpace,
  NButton,
  NEmpty,
  NGrid,
  NGi,
  NDivider,
  NUpload,
  NText,
  NP,
  NUploadDragger,
  NIconWrapper,
  NIcon,
} from 'naive-ui'
import { onMounted, ref } from 'vue'
import SFile from '../components/SFile/SFile.vue'
import FileType from '../types/File'
import useRest from '../use/rest'
import { Archive, FileTray } from '@vicons/ionicons5'
const rest = useRest()
const files = ref<FileType[]>([])

const loadFiles = async () => {
  files.value = await rest.getFiles()
}
onMounted(async () => {
  await loadFiles()
})
</script>
<template>
  <div>
    <NPageHeader :subtitle="`Uploaded files: ${files.length}`">
      <template #title>Uploaded Files</template>
      <template #avatar>
        <NIconWrapper color="rgba(99, 226, 183, 0.16)" :size="40">
          <NIcon :size="32" color="#63e2b7">
            <FileTray />
          </NIcon>
        </NIconWrapper>
      </template>
    </NPageHeader>
    <NDivider></NDivider>
    <template v-if="!files.length">
      <NEmpty description="You can't find anything">
        <template #extra>
          <NButton @click="loadFiles()" size="small">Refresh</NButton>
        </template>
      </NEmpty>
    </template>
    <template v-else>
      <NGrid
        x-gap="12"
        y-gap="12"
        cols="1 s:1 m:3 l:3 xl:5  "
        responsive="screen"
      >
        <NGi v-for="(file, index) in files" :key="index">
          <SFile
            :file-name="file.fileName"
            :file-size="file.fileSize"
            :file-preview="file.filePreview"
          ></SFile>
        </NGi>
      </NGrid>
    </template>
    <NDivider />

    <NUpload
      :action="`${rest.API_URL}/files/upload`"
      style="text-align: center"
      accept=".csv,.txt"
      :input-props="{ accept: '.csv' }"
    >
      <NUploadDragger>
        <div style="margin-bottom: 12px">
          <NIcon size="48" :depth="3">
            <Archive />
          </NIcon>
        </div>
        <NText style="font-size: 16px">
          Click or drag a file to this area to upload
        </NText>
        <NP depth="3" style="margin: 8px 0 0 0">
          Strictly prohibit from uploading sensitive information. For example,
          your bank card PIN or your credit card expiry date.
        </NP>
      </NUploadDragger>
    </NUpload>
  </div>
</template>

<style></style>
