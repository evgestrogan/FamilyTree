import { ref } from "vue";
import { defineStore } from "pinia";

export const useSettingStore = defineStore("setting", () => {
  const mobileSideBar = ref(false);
  function setMobileSideBar(status) {
    mobileSideBar.value = status;
  }

  return { mobileSideBar, setMobileSideBar };
});
