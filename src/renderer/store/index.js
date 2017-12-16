import Vue from 'vue';
import Vuex from 'vuex';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

import modules from './modules';

Vue.use(Vuex);

const state = {
  code: 'unknown',
  interviewState: 'none',
};

export default new Vuex.Store({
  state,
  actions,
  getters,
  mutations,
  modules,
  strict: process.env.NODE_ENV !== 'production',
});
