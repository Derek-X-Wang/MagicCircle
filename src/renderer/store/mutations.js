import * as types from './mutation-types';

const mutations = {
  [types.WORMHOLE_SEND](state) {
    state.interviewState = '';
  },
  [types.WORMHOLE_RECEIVE](state) {
    state.interviewState = '';
  },
  [types.WORMHOLE_GET_CODE](state) {
    state.interviewState = '';
  },
  [types.WORMHOLE_UPDATE_CODE](state, code) {
    state.code = code;
  },
};

export default mutations;