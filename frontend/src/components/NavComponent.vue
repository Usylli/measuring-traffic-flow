<template>
  <nav>
    <ul>
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li v-if="!isLoggedIn">
        <router-link to="/login">Login</router-link>
      </li>
      <li v-else>
        <button @click="logout">Logout</button>
      </li>
      <li v-if="!isLoggedIn">
        <router-link to="/register">Register</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import {onMounted} from 'vue';
import { useStore } from 'vuex'
import {useRouter} from "vue-router";

export default {
  setup(){
    const { state, dispatch } = useStore();
    const router = useRouter();
    dispatch('getTokens');
    let isLoggedIn = state.isLoggedIn

    async function logout() {
      dispatch('logout');
      await router.push('/login');
    }

    return {
      isLoggedIn,
      logout
    }
  }
}
</script>

<style scoped>
  nav {
    background-color: #333;
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 20px;
  }

  nav ul {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  nav ul li {
    margin-right: 20px;
  }

  nav ul li a {
    color: #fff;
    text-decoration: none;
    font-size: 1.2rem;
  }

  nav ul li a:hover {
    color: #4CAF50;
  }

  button {
    width: 100%;
    background-color: #af4c4c;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    border: none;
    border-radius: 4px;
  }

  button:hover {
    background-color: #a04545;
  }
</style>