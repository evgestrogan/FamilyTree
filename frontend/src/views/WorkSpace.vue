<template>
  <header class="h-16 drop-shadow-md">
    <nav-bar>
      <router-view
        name="navContent"
        class="grow relative mx-8 sm:mx-16 md:mx-24 lg:mx-48 xl:mx-64 2xl:mx-96"
      ></router-view>
    </nav-bar>
  </header>
  <main class="flex h-main">
    <router-view name="sidebar" v-slot="{ Component }">
      <side-bar>
        <component :is="Component" />
      </side-bar>
    </router-view>
    <router-view></router-view>
  </main>
</template>

<script setup>
import NavBar from "../components/UI/NavigationBar/NavBar.vue";
import SideBar from "../components/UI/SideBar.vue";
</script>

<style scoped></style>
