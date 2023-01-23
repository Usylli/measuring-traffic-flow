<template>
  <div>
    <NavComponent/>
    <div class="container">
      <form @submit.prevent="login">
        <h1>Login</h1>
        <label for="email">Email</label>
        <input v-model="data.email" type="email" id="email" name="email" required>
        <label for="password">Password</label>
        <input v-model="data.password" type="password" id="password" name="password" required>
        <button type="submit">Sign in</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
  import NavComponent from "../components/NavComponent.vue";
  import {reactive} from 'vue';
  import {useRouter} from "vue-router";
  import axios from 'axios';
  import { useStore } from 'vuex';

  export default {
    components: {NavComponent},
    setup() {
      const { state, dispatch } = useStore();
      const data = reactive({
        email: '',
        password: ''
      });
      const router = useRouter();

      async function login() {
        try {
          const response = await axios.post('http://10.128.0.2:8000/api/v1/jwt/create/', {
            email: data.email,
            password: data.password
          });
          dispatch('setTokens', { access_token: response.data.access, refresh_token: response.data.refresh });
          await router.push('/');
        } catch (error) {
          console.error(error);
        }
      }

      return {
        data,
        login,
      }
    }
  };
</script>

<style scoped>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  .container {
    background-color: #f1f1f1;
    font-family: Arial, sans-serif;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
  }

  form {
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    align-items: center;
  }

  label {
    width: 100%;
    margin-bottom: 10px;
    font-size: 1.2rem;
  }

  input {
    width: 100%;
    padding: 12px 20px;
    margin-bottom: 20px;
    font-size: 1.2rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    width: 100%;
    padding: 12px 20px;
    background-color: #4CAF50;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    border: none;
    border-radius: 4px;
  }

  button:hover {
    background-color: #45a049;
  }

</style>