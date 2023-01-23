<template>
    <div>
        <NavComponent/>
        <div class="container">
            <form @submit.prevent="register">
                <h1>Register</h1>
                <label for="username">Username</label>
                <input v-model="formData.username" type="text" id="username" name="username" required>
                <label for="firstname">First Name</label>
                <input v-model="formData.firstname" type="text" id="firstname" name="firstname" required>
                <label for="lastname">Last Name</label>
                <input v-model="formData.lastname" type="text" id="lastname" name="lastname" required>
                <label for="email">Email</label>
                <input v-model="formData.email" type="email" id="email" name="email" required>
                <label for="password">Password</label>
                <input v-model="formData.password" type="password" id="password" name="password" required>
                <label for="re_password">Re-enter Password</label>
                <input v-model="formData.re_password" type="password" id="re_password" name="re_password" required>
                <button type="submit">Register</button>
            </form>
        </div>
    </div>
  </template>

<script>
import NavComponent from "../components/NavComponent.vue";
import {reactive} from 'vue';
import {useRouter} from "vue-router";
import axios from 'axios';

export default {
  components: {NavComponent},
  setup() {
    const formData = reactive({
      username: '',
      firstname: '',
      lastname: '',
      email: '',
      password: '',
      re_password: '',
    });
    const router = useRouter();

    async function register() {
        try {
            if (formData.password !== formData.re_password) {
                alert("Passwords do not match, please try again.")
                return;
            }
            const response = await axios.post('http://10.128.0.2:8000/api/v1/users/', {
                username: formData.username,
                first_name: formData.firstname,
                last_name: formData.lastname,
                email: formData.email,
                password: formData.password,
                re_password: formData.password
            });
            console.log(response.data)
            await router.push('/login');
        } catch (error) {
            console.error(error);
        }
    }

    return {
      formData,
      register
    }
  }
}
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