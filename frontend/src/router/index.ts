import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import PipelineView from '../views/PipelineView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Pipelines',
    component: PipelineView,
  },
  {
    path: '/files',
    name: 'Files',
    component: () => import('../views/FileView.vue'),
  },
  {
    path: '/connections',
    name: 'Connections',
    component: () => import('../views/ConnectionsView.vue'),
  },
  {
    path: '/editor',
    name: 'Editor',
    component: () => import('../views/PipelineEditorView.vue'),
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
