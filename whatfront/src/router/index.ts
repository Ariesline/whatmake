import { createRouter,createWebHistory,type RouteRecordRaw } from 'vue-router'

//createRouter创建路由实例，===> new VueRouter()
// history是路由模式,hash模式,history模式
// createwebHistory(是开启history模块
// createwebHashHistory(是开启hash模式
const routes = [
    {
        path: '/',
        name:'Home',
        component: () =>import('../veiws/homepage/index.vue')
    },
    {
        path: '/Edit',
        name: 'Edit',
        component: () =>import('../veiws/edit/index.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () =>import('../veiws/homepage/register.vue')
    },
    {
        path: '/settings',
        name: 'Settings',
        component: () =>import('../veiws/UserSettings/index.vue')
    }
]as RouteRecordRaw[]
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})
export default router
