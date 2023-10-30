import "bootstrap/dist/css/bootstrap.css"

import { createApp } from 'vue'
import App from './App.vue'

import router from './router'
import axios from 'axios'
import jszip from 'jszip'

axios.defaults.baseURL = "http://127.0.0.1:8888/api/"

createApp(App).use(router, axios, jszip).mount('#app')
