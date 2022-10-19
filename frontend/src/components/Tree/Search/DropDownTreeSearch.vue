<template>
  <drop-down v-model="dropdown" close-on-click>
    <template v-slot:activator>
      <text-field
        v-model="request"
        @focusin="dropdown = true"
        type="text"
        class="!py-2.5 !px-10"
        placeholder="Поиск"
      ></text-field>
      <router-link :to="requestLink">
        <button
          @click="clearRequest"
          type="submit"
          class="flex absolute inset-y-0 left-2 items-center"
        >
          <icon icon="mdi-magnify" class="text-indigo-500"></icon>
        </button>
      </router-link>
    </template>
    <template v-slot:body>
      <div class="hidden sm:block">
        <div>
          <button @click.stop="switchSettings" class="w-full hover:bg-gray-100">
            <span class="px-2 text-xs text-indigo-400">Настройки поиска</span>
          </button>
          <search-settings v-show="settings"></search-settings>
        </div>
        <div @click.prevent="clearRequest">
          <div v-for="result in searchResults" :key="result.variant">
            <search-list
              v-if="result.condition"
              :items="result.items"
              :variant="result.variant"
              :limit="result.limit"
            >
              {{ result.title }}
            </search-list>
          </div>

          <router-link :to="requestLink">
            <btn class="rounded-none">Просмотреть все результаты</btn>
          </router-link>
        </div>
      </div>
    </template>
  </drop-down>
</template>

<script setup>
import Icon from "../../UI/Icon.vue";
import DropDown from "../../UI/DropDown.vue";
import TextField from "../../UI/Input/TextField.vue";
import SearchSettings from "./SearchSettings.vue";
import SearchList from "./SearchList.vue";
import Btn from "../../UI/Button/Btn.vue";
import { useSearchStore } from "../../../stores/search";
import { ref, computed } from "vue";

const store = useSearchStore();

const requestLink = { name: "Search", params: { variant: "all" } };
const searchRequest = ref("");
const request = computed({
  get() {
    return searchRequest.value;
  },
  set(value) {
    store.setSearchRequest(value);
    searchRequest.value = value;
  },
});
function clearRequest() {
  searchRequest.value = "";
  closeDropdown();
}

const dropdown = ref(false);
function closeDropdown() {
  dropdown.value = false;
}

const settings = ref(false);
function switchSettings() {
  settings.value = !settings.value;
}

const searchResults = computed(() => [
  {
    items: [],
    variant: "graph",
    limit: 2,
    title: "Объекты на графе",
    condition: store.searchGraph,
  },
  {
    items: store.selfPeople,
    variant: "self",
    limit: 2,
    title: "Ваши объекты",
    condition: store.searchSelf,
  },
  {
    items: store.globalPeople,
    variant: "global",
    limit: 2,
    title: "Объекты глобального поиска",
    condition: store.searchGlobal,
  },
]);
</script>

<style scoped></style>
