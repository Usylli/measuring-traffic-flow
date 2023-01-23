import { createStore, ActionContext } from 'vuex';
import Cookies from 'js-cookie'

const state = () => ({
  access_token: '',
  refresh_token: '',
  isLoggedIn: false
});

const mutations = {
  setAccessToken(state: any, token: string) {
    state.access_token = token;
    Cookies.set("access_token", token);
    state.isLoggedIn = true
  },
  setRefreshToken(state: any, token: string) {
    state.refresh_token = token;
    Cookies.set("refresh_token", token);
    state.isLoggedIn = true
  },
  deleteTokens(state: any) {
    state.access_token = '';
    state.refresh_token = '';
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    state.isLoggedIn = false
  }
};

const actions = {
  setTokens(context: ActionContext<any, any>, payload: {access_token: string; refresh_token: string;}) {
    context.commit('setAccessToken', payload.access_token);
    context.commit('setRefreshToken', payload.refresh_token);
  },
  getTokens(context: ActionContext<any, any>) {
    const access_token = Cookies.get("access_token");
    const refresh_token = Cookies.get("refresh_token");
    if (access_token && refresh_token) {
      context.commit('setAccessToken', access_token);
      context.commit('setRefreshToken', refresh_token);
    }
  },
  logout(context: ActionContext<any, any>) {
    context.commit('deleteTokens');
  }
};

const getters = {
  access_token: (state: any) => state.access_token,
  refresh_token: (state: any) => state.refresh_token,
  isLoggedIn: (state: any) => state.isLoggedIn
};

export default createStore({
  state,
  mutations,
  actions,
  getters,
});
