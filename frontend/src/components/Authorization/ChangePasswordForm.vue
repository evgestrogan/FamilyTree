<template>
  <form class="mt-8 space-y-6" @submit.prevent="confirmChangePassword">
    <input type="hidden" name="remember" value="true" />
    <div class="rounded-md shadow-sm -space-y-px">
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

    <btn type="submit">Изменить</btn>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import { useRoute } from "vue-router";
import { ref } from "vue";
import { useAuthorizationStore } from "../../stores/authorization";

const store = useAuthorizationStore();
const route = useRoute();

const password = ref("");
const confirmPassword = ref("");

function confirmChangePassword() {
  if (password.value === confirmPassword.value) {
    store.changePassword({ password: password.value, key: route.params.key });
  }
}
</script>

<style scoped></style>
