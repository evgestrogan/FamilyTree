import { ref } from "vue";
import { defineStore } from "pinia";

export const useNotificationStore = defineStore("notification", () => {
  const alerts = ref([]);
  function addAlert(alert) {
    alerts.value.push(alert);
  }
  function removeAlert(alert) {
    alerts.value.splice(
      alerts.value.findIndex((a) => a === alert),
      1
    );
  }

  return { alerts, addAlert, removeAlert };
});
