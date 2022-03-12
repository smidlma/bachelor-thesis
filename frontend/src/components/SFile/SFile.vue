<script setup lang='ts'>
import { Document } from '@vicons/ionicons5'
import { NCard, NIcon, NButton, NSpace } from 'naive-ui'
const props = defineProps({
    fileName: {
        type: String,
        required: true
    },
    fileSize: {
        type: String,
        required: true
    }
})
</script>

<template>
    <NCard :title="props.fileName" class="s-file">
        <template #cover>
            <NIcon class="s-file__icon">
                <Document></Document>
            </NIcon>
        </template>
        {{ props.fileSize }}
        <template #action>
            <NSpace justify="center">
                <NButton>View</NButton>
                <NButton secondary type="error">Delete</NButton>
            </NSpace>
        </template>
    </NCard>
</template>
    

    
<style lang="sass" scoped>

.s-file
    text-align: center
    padding: 12px

.s-file__icon
    font-size: 26px
</style>