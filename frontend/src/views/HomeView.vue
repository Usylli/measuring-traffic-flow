<template>
  <div>
    <NavComponent/>
    <div class="container">
      <div class="welcome-message">
        {{ message }}
      </div>
    </div>
  </div>

</template>

<script lang="ts">
import NavComponent from "../components/NavComponent.vue";
import {onMounted, ref} from 'vue';
import axios from 'axios';
import {useStore} from "vuex";

export default {
  name: "HomeView",
  components: {NavComponent},
  setup() {
    const message = ref('You are not logged in!');
    const { state, dispatch } = useStore();

    onMounted(async () => {
      try {
          dispatch('getTokens');
          const response = await axios.get('http://10.128.0.2:8000/api/v1/users/me/', {
            headers: {
              'Authorization': `Bearer ${state.access_token}`
            }
          });
          message.value = `Hi, ${response.data.username}`;
        } catch (error) {
          message.value = `You are not logged in!`;
          console.error(error);
        }
    });

    return {
      message
    }
  }
}
</script>

<style scoped>
  .container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
  }

  .welcome-message {
    font-size: 2rem;
    color: #4CAF50;
  }
</style>