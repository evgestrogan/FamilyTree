<template>
  <form class="mt-8 space-y-6" @submit.prevent="confirmForgotPassword">
    <input type="hidden" name="remember" value="true">
    <div class="rounded-md shadow-sm -space-y-px">
      <text-field
        v-model="email"
        id="email-address"
        name="email"
        type="email"
        autocomplete="email"
        placeholder="Email"
        required
      ></text-field>
    </div>

    <btn type="submit">Отправить</btn>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import {useStore} from 'vuex';
import {ref} from "vue";

const store = useStore()

const email = ref("")

function confirmForgotPassword() {
  store.dispatch('forgotPasswordEmail', email.value)
}
</script>

<style scoped>

</style>