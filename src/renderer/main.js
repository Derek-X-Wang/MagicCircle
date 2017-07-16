import Vue from 'vue'

import App from './App'
import router from './router'
import store from './store'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.config.productionTip = false

// Python Client
const zerorpc = require("zerorpc")
const client = new zerorpc.Client();

client.connect("tcp://127.0.0.1:4242");

client.invoke("echo", "server ready", (error, res) => {
  if(error || res !== 'server ready') {
    console.error(error);
  } else {
    console.log("server is ready");
  }
});

Vue.prototype.$python = client;

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
