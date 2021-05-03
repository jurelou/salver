<template>
    <div id="app">
        <Nav/>

        <transition name="fade">
            <div class="gap">
                <div class="container mt-4 d-flex justify-content-center">
                    <router-view></router-view>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    import Nav from "./components/Nav";
    export default {
        name: 'App',
        components: {
            VuebaseLayout,
            Nav
        },
        computed: {
            component() {
                return VuebaseLayout
            }
        }

        components: {Nav}
    };
</script>

<style>
</style>
