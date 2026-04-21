import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Chat from './views/Chat.vue'
import CaseSearch from './views/CaseSearch.vue'
import LawSearch from './views/LawSearch.vue'
import Strategy from './views/Strategy.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/chat' },
    { path: '/chat', component: Chat },
    { path: '/case', component: CaseSearch },
    { path: '/law', component: LawSearch },
    { path: '/strategy', component: Strategy },
  ]
})

createApp(App).use(router).mount('#app')
