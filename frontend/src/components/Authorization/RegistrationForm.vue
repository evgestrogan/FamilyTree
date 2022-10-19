<template>
  <form class="mt-8 space-y-6" @submit.prevent="confirmRegistration">
    <input type="hidden" name="remember" value="true" />
    <div class="rounded-md shadow-sm -space-y-px">
      <text-field
        v-model="username"
        id="username"
        name="username"
        type="text"
        autocomplete="username"
        placeholder="Логин пользователя"
        minlength="4"
        required
      ></text-field>
      <text-field
        v-model="email"
        id="email-address"
        name="email"
        type="email"
        autocomplete="email"
        placeholder="Email"
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
      <text-field
        v-model="confirmPassword"
        id="confirm-password"
        name="confirm-password"
        type="password"
        autocomplete="confirm-password"
        placeholder="Подтвердите пароль"
        minlength="8"
        required
      ></text-field>
    </div>

    <btn type="submit">Зарегестрироваться</btn>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import { ref } from "vue";
import { useAuthorizationStore } from "../../stores/authorization";

const store = useAuthorizationStore();

const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

function confirmRegistration() {
  if (password.value === confirmPassword.value) {
    store.registration({
      username: username.value,
      email: email.value,
      password: password.value,
    });
  }
}
</script>

<style scoped></style>
