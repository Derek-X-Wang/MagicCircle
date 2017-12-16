import * as types from './mutation-types';

const actions = {
  startInterview({ commit }, { selected, selectedIndex, orientation }) {
    commit({
      type: types.WORMHOLE_SEND,
      selected,
      selectedIndex,
      orientation,
    });
  },
  pauseInterview({ commit }, { scene }) {
    commit({
      type: types.WORMHOLE_RECEIVE,
      scene,
    });
  },
  stopInterview({ commit }, { scene }) {
    commit({
      type: types.WORMHOLE_GET_CODE,
      scene,
    });
  },
  updateCode({ commit }, { code }) {
    commit({
      type: types.WORMHOLE_UPDATE_CODE,
      code,
    });
  },
};

export default actions;