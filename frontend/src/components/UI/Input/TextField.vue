<template>
  <input :class="classes" v-model="value" />
</template>

<script setup>
import { reactive, computed } from "vue";

const props = defineProps(["modelValue"]);
const emit = defineEmits(["update:modelValue"]);

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});

const listClasses = reactive([
  "appearance-none",
  "rounded-none",
  "block",
  "w-full",
  "px-3",
  "py-2",
  "border",
  "border-gray-300",
  "placeholder-gray-500",
  "text-gray-900",
  "focus:outline-none",
  "focus:ring-indigo-500",
  "focus:border-indigo-500",
  "focus:z-10",
  "text-sm",
]);

const classes = computed(() => {
  return listClasses.join(" ");
});
</script>

<style scoped></style>
