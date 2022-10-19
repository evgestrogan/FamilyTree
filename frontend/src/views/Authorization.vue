<template>
  <div
    class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <img
          class="mx-auto h-24 w-auto"
          src="http://127.0.0.1:5173/src/assets/logo.png"
          alt="FamilyTree Logo"
        />
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          {{ title }}
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          <nav-link :to="link">{{ textLink }}</nav-link>
        </p>
      </div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import NavLink from "../components/UI/Link/NavLink.vue";
import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();
const title = computed(() => route.meta.title);
const link = computed(() => Object.assign({ name: route.meta.link }));
const textLink = computed(() => route.meta.textLink);
</script>

<style></style>
