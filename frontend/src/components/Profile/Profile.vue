<template>
    <div class="container w-full m-2">
      <card class="w-10/12 mx-auto flex flex-col md:w-1/2 md:flex-row items-center">
        <div class="p-4">
          <img class="object-cover h-48 md:h-auto md:w-48" src="http://127.0.0.1:5173/src/assets/profile.jpg" alt="">
          <icon icon="mdi-pencil" color="text-indigo-800"></icon>
        </div>
        <div class="flex flex-col justify-between leading-normal w-full">
          <text-field placeholder="Имя" class="mb-2"></text-field>
          <text-field placeholder="Фамилия" class="mb-2"></text-field>
          <text-field placeholder="Отчество" class="mb-2"></text-field>
          <text-field placeholder="Пол" class="mb-2"></text-field>
        </div>
      </card>
    </div>

</template>

<script setup>
import Card from "../UI/Card.vue";
import TextField from "../UI/Input/TextField.vue";
import IconBtn from "../UI/Button/IconBtn.vue";
import Icon from "../UI/Icon.vue";
</script>

<style scoped></style>
