<template>
  <form class="mt-8 space-y-6" @submit.prevent="confirmLogin">
    <input type="hidden" name="remember" value="true" />
    <div class="rounded-md shadow-sm -space-y-px">
      <text-field
        v-model="username"
        id="username"
        name="username"
        type="username"
        autocomplete="username"
        placeholder="Username"
        minlength="4"
        required
      ></text-field>
      <text-field
        v-model="password"
        id="password"
        name="password"
        type="password"
        autocomplete="current-password"
        placeholder="Пароль"
        minlength="8"
        required
      ></text-field>
    </div>

    <div class="flex items-center justify-end text-sm">
      <nav-link :to="{ name: 'ForgotPassword' }">Забыли свой пароль?</nav-link>
    </div>

    <btn type="submit">Войти</btn>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import NavLink from "../UI/Link/NavLink.vue";
import { useAuthorizationStore } from "../../stores/authorization";
import { ref } from "vue";

const store = useAuthorizationStore();

const username = ref("");
const password = ref("");

function confirmLogin() {
  store.login({
    username: username.value,
    password: password.value,
  });
}
</script>

<style scoped></style>
