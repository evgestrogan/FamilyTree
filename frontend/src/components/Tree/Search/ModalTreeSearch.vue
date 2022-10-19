<template>
  <modal>
    <div class="flex">
      <text-field
        v-model="request"
        type="text"
        placeholder="Поиск"
      ></text-field>
      <button type="submit" class="flex inset-y-0 pl-4 items-center">
        <icon icon="mdi-magnify" class="text-indigo-500 text-4xl"></icon>
      </button>
    </div>
    <template v-if="showSettings">
      <button @click="switchSettings" class="w-full hover:bg-gray-100">
        <span class="px-2 text-xs text-indigo-400">Настройки поиска</span>
      </button>
      <search-settings v-show="settings"></search-settings>
    </template>

    <div class="pt-5">
      <template v-for="(result, key) in searchResults" :key="key">
        <search-list v-if="result.condition" :items="result.items">{{
          result.title
        }}</search-list>
      </template>
    </div>
  </modal>
</template>

<script setup>
import Icon from "../../UI/Icon.vue";
import Modal from "../../UI/Modal.vue";
import TextField from "../../UI/Input/TextField.vue";
import SearchSettings from "./SearchSettings.vue";
import SearchList from "./SearchList.vue";
import { useSearchStore } from "../../../stores/search";
import { ref, computed } from "vue";
import { useRoute } from "vue-router";

const store = useSearchStore();
const route = useRoute();

const request = computed({
  get() {
    return store.searchRequest;
  },
  set(value) {
    store.setSearchRequest(value);
  },
});

const settings = ref(false);
const showSettings = computed(() => route.params.variant === "all");
function switchSettings() {
  settings.value = !settings.value;
}

const searchResults = computed(() => [
  {
    items: [],
    title: "Объекты на графе",
    condition:
      (route.params.variant === "all" || route.params.variant === "graph") &&
      store.searchGraph,
  },
  {
    items: store.selfPeople,
    title: "Ваши объекты",
    condition:
      (route.params.variant === "all" || route.params.variant === "self") &&
      store.searchSelf,
  },
  {
    items: store.globalPeople,
    title: "Объекты глобального поиска",
    condition:
      (route.params.variant === "all" || route.params.variant === "global") &&
      store.searchGlobal,
  },
]);
</script>

<style scoped></style>
