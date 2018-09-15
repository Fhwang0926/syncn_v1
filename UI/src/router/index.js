import Vue from 'vue'
import Router from 'vue-router'

// Containers
const DefaultContainer = () => import('@/containers/DefaultContainer')

// Views - Pages
const Page404 = () => import('@/views/pages/Page404')
const Page500 = () => import('@/views/pages/Page500')

const home = () => import('@/views/base/home')
const download = () => import('@/views/base/download')
const translation = () => import('@/views/base/translation')


Vue.use(Router)

export default new Router({
  mode: 'hash', // https://router.vuejs.org/api/#mode
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/home',
      name: 'home', component: DefaultContainer, children: [
        { path: 'home', name: 'home', component: home },
        { path: 'download', name: 'download', component: download },
        { path: 'translation', name: 'translation', component: translation },
    ]}
  ]
})
