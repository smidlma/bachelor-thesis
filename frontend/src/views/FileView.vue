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
  NUpload,
  NText,
  NP,
  NUploadDragger,
  NIcon,
} from 'naive-ui'
import { onMounted, ref } from 'vue'
import SFile from '../components/SFile/SFile.vue'
import FileType from '../types/File'
import useRest from '../use/rest'
import { Archive } from '@vicons/ionicons5'
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
        <NAvatar
          src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
        />
      </template>
      <template #extra>
        <NSpace>
          <NUpload
            action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
            :headers="{
              'naive-info': 'hello!',
            }"
            :data="{
              'naive-data': 'cool! naive!',
            }"
          >
            <NButton>Upload</NButton>
          </NUpload>
        </NSpace>
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

    <n-upload
      :action="`${rest.API_URL}/files/upload`"
      style="text-align: center"
    >
      <n-upload-dragger>
        <div style="margin-bottom: 12px">
          <n-icon size="48" :depth="3">
            <Archive />
          </n-icon>
        </div>
        <n-text style="font-size: 16px">
          Click or drag a file to this area to upload
        </n-text>
        <n-p depth="3" style="margin: 8px 0 0 0">
          Strictly prohibit from uploading sensitive information. For example,
          your bank card PIN or your credit card expiry date.
        </n-p>
      </n-upload-dragger>
    </n-upload>
  </div>
</template>

<style></style>
