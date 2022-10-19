<template>
  <drop-down v-model="dropdown" close-on-click>
    <template v-slot:activator>
      <button
        @click="switchDropdown"
        type="button"
        class="flex items-center text-sm text-white"
        aria-expanded="false"
      >
        <span class="hidden sm:flex">Ivanov Ivan Ivanovich</span>
        <img
          class="w-8 h-8 ml-3 rounded-full"
          src="http://127.0.0.1:5173/src/assets/profile.jpg"
          alt="user photo"
        />
      </button>
    </template>
    <template v-slot:body>
      <list @click="closeDropdown">
        <control-item
          v-for="item in dropDownMenu"
          :key="item.icon"
          @click="item.action()"
          :title="item.title"
          :subtitle="item.subtitle"
          :icon="item.icon"
        ></control-item>
      </list>
    </template>
  </drop-down>
</template>

<script setup>
import DropDown from "../../DropDown.vue";
import List from "../../ListItems/List.vue";
import ControlItem from "./ControlItem.vue";
import { useAuthorizationStore } from "../../../../stores/authorization";
import { useRouter } from "vue-router";
import { ref } from "vue";

const dropdown = ref(false);

function switchDropdown() {
  dropdown.value = !dropdown.value;
}

function closeDropdown() {
  dropdown.value = false;
}

const store = useAuthorizationStore();
const router = useRouter();
const dropDownMenu = [
  {
    title: "Чат",
    subtitle: "Ваши переписки",
    icon: "mdi-message-outline",
    action: () => router.push({ name: "Chat" }),
  },
  {
    title: "Настройки",
    subtitle: "Настройки вашего профиля",
    icon: "mdi-account-cog-outline",
    action: () => router.push({ name: "Profile" }),
  },
  {
    title: "Выход",
    subtitle: "Выход из системы",
    icon: "mdi-logout",
    action: () => store.logout(),
  },
];
</script>

<style scoped></style>
