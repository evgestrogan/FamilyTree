<template>
  <div
    class="flex items-center w-full max-w-sm p-4 text-gray-800 backdrop-blur-sm bg-white/50 rounded-lg shadow my-2"
    role="alert"
  >
    <div :class="classes">
      <Icon :icon="icon"></Icon>
    </div>
    <div class="mx-2">
      <div class="flex flex-row justify-between items-center">
        <span class="font-semibold">Ошибка {{ code }}</span>
        <span class="ml-2 text-xs font-normal text-gray-400">{{ time }}</span>
      </div>
      <span class="text-sm font-normal text-gray-500">{{ body }}</span>
    </div>
  </div>
</template>

<script setup>
import Icon from "../Icon.vue";
import { computed } from "vue";

const props = defineProps(["alert"]);
const type = props.alert.type;
const body = props.alert.body;
const code = props.alert.code;
const time = props.alert.time;

const alertSettings = {
  error: {
    icon: "mdi-alert-circle-outline",
    classes: ["text-orange-500", "bg-orange-100"],
  },

  success: {
    icon: "mdi-check-circle-outline",
    classes: ["text-green-500", "bg-green-100"],
  },
};

const listClasses = [
  "inline-flex",
  "items-center",
  "justify-center",
  "flex-shrink-0",
  "w-8",
  "h-8",
  "rounded-lg",
];

const classes = computed(() => {
  return listClasses.concat(alertSettings[type].classes).join(" ");
});
const icon = computed(() => {
  return alertSettings[type].icon;
});
</script>

<style scoped></style>
