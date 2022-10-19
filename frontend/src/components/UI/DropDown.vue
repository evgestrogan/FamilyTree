<template>
  <div class="relative" v-click-outside="clickOutside">
    <slot name="activator"></slot>
    <transition name="dropdown">
      <div
        v-show="dropdown"
        class="z-10 overflow-y-auto max-h-screen-2/3 absolute top-12 bg-white min-w-full divide-y divide-gray-100 shadow"
      >
        <slot name="body"></slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
  },
  closeOnClick: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:modelValue"]);

const dropdown = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});

function clickOutside() {
  if (props.closeOnClick) {
    dropdown.value = false;
  }
}
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.5s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-35px);
}
</style>
