import Vue from 'vue'
import VueRouter from 'vue-router'
import VueAxios from 'vue-axios'
import axios from 'axios'

import NProgress from 'nprogress'

import App from './App.vue'
import PublicPosts from "./components/PublicPosts";


Vue.use(VueRouter)

Vue.use(VueAxios, axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        Authorization: `Bearer ${localStorage.getItem('actoken')}`
    }
}))


Vue.config.productionTip = false


const routes = [
    {
        name: 'Home',
        path: '/',
        component: PublicPosts
    }
]


const router = new VueRouter({mode: 'history', routes: routes})

router.beforeResolve((to, from, next) => {
    if (to.name) {
        NProgress.start()
    }
    next()
})

router.afterEach(() => {
    NProgress.done()
})

new Vue({
    render: h => h(App),
    router
}).$mount('#app')
