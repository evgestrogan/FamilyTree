<template>
  <span :class="classes"></span>
</template>

<script setup>
import {computed, reactive} from "vue";

const props = defineProps(["icon", "color"]);

const listClasses = reactive([
    "mdi",
    "text-2xl",
    props.icon,
    props.color,
])

const classes = computed(() => {
  return listClasses.join(" ");
});
</script>

<style scoped></style>
