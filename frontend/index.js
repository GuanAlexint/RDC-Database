import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import SearchPage from '../views/SearchPage.vue'
import DetailPage from '../views/DetailPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/search',
    name: 'Search',
    component: SearchPage
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: DetailPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

