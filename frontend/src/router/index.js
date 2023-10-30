import {createRouter, createWebHistory} from 'vue-router';

import PostcardConstructor from "../views/PostcardConstructor.vue"
import PostcardShow from "../views/PostcardShow.vue"
import Home from "../views/Home.vue"

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home
    },
    {
        path: "/postcard_constructor",
        name: "PostcardConstructor",
        component: PostcardConstructor
    },
    {
        path: "/postcard_show",
        name: "PostcardShow",
        component: PostcardShow
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
