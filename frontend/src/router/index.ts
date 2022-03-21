import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/files',
    name: 'Files',
    component: () => import('../views/FileView.vue'),
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
