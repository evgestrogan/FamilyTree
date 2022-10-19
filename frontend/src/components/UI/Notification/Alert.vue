<template>
  <div class="absolute right-5 bottom-5 cursor-pointer">
    <transition-group name="list" tag="div">
      <alert-item
        v-for="alert in alerts"
        :key="alert"
        :alert="alert"
        @click="remove(alert)"
      ></alert-item>
    </transition-group>
  </div>
</template>

<script setup>
import AlertItem from "./AlertItem.vue";
import { useNotificationStore } from "../../../stores/notification";

const store = useNotificationStore();

const alerts = store.alerts;

function remove(alert) {
  store.removeAlert(alert);
}
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-35px);
}
</style>
