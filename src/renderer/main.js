import Vue from 'vue';

import App from './App';
import router from './router';
import store from './store';

const pythonServerPort = 4242;
const jsServerPort = 4243;

if (!process.env.IS_WEB) Vue.use(require('vue-electron'));
Vue.config.productionTip = false;

// Python Client
const zerorpc = require("zerorpc");
const client = new zerorpc.Client();
client.connect(`tcp://127.0.0.1:${pythonServerPort}`);
// test python client
client.invoke("echo", "server ready", (error, res) => {
  if(error || res !== 'server ready') {
    console.error(error);
  } else {
    console.log("server is ready");
  }
});
Vue.prototype.$python = client;

// js callback server
// need to pass store to callbackApi
var server = new zerorpc.Server({
  echo: function(text, reply) {
    console.log(text);
    reply(null, text);
  },
  updateCode: function(code, reply) {
      // send code to store
      console.log(`code is ${code}`);
      //store.dispatch('updateCode', { code });
      reply(null);
  },
  showDebugMessage: function(msg, reply) {
      reply(null, msg);
  },
});
server.bind(`tcp://127.0.0.1:${jsServerPort}`);
server.on("error", function(error) {
  console.error("RPC server error:", error);
});
// call when js server is ready
client.invoke("on_js_server_ready", `tcp://127.0.0.1:${jsServerPort}`, (error, res) => {
  if(error || !res) {
    console.error(error);
  } else {
    console.log("py-js client ready");
  }
});

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app');
