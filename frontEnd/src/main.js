import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import libgif from 'libgif'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Object.defineProperty(Vue.prototype, '$libgif', { value: libgif });
Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(BootstrapVue);
new Vue({
	render: h => h(App),
}).$mount('#app')