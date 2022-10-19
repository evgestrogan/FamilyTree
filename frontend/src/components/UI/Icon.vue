<template>
  <span class="mdi text-2xl" :class="props.icon"></span>
</template>

<script setup>
const props = defineProps(["icon"]);
</script>

<style scoped></style>
