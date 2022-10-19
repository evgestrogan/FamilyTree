<template>
  <div
    class="fixed z-10 inset-0 overflow-y-auto"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <div
      class="flex items-start justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
    >
      <div
        class="fixed inset-0 bg-gray-500 bg-opacity-50 transition-opacity"
        aria-hidden="true"
      ></div>
      <span
        class="hidden sm:inline-block sm:align-middle sm:h-screen"
        aria-hidden="true"
        >&#8203;</span
      >
      <div
        @click.stop
        v-click-outside="closeModal"
        class="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
      >
        <div class="flex sm:hidden justify-end p-1">
          <button
            @click="closeModal"
            type="button"
            class="text-gray-400 hover:text-gray-900 inline-flex items-center"
          >
            <icon icon="mdi-close"></icon>
          </button>
        </div>
        <div class="bg-white pb-4 px-4 sm:px-6 sm:pt-4">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Icon from "./Icon.vue";
import { useRouter } from "vue-router";

const router = useRouter();

function closeModal() {
  router.push({ name: "Tree" });
}
</script>

<style scoped></style>
