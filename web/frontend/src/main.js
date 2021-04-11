import Vue from 'vue'
import VueRouter from 'vue-router'
import VueAxios from 'vue-axios'
import axios from 'axios'

import NProgress from 'nprogress'

import App from './App.vue'
import PublicPosts from "./components/PublicPosts"

import VueSocketIO from 'vue-socket.io'

Vue.use(VueRouter)

Vue.use(VueAxios, axios.create({
    baseURL: 'http://localhost:8000/api',
    // headers: {
    //     Authorization: `Bearer ${localStorage.getItem('actoken')}`
    // }
}))

Vue.use(new VueSocketIO({
    debug: true,
    connection: 'http://localhost:8000',
    // vuex: {
    //     store,
    //     actionPrefix: 'SOCKET_',
    //     mutationPrefix: 'SOCKET_'
    // },
    options: { path: "/websock/socket.io" } //Optional options
}))


Vue.config.productionTip = true


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
