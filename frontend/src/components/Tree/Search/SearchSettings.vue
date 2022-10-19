<template>
  <list>
    <search-settings-item
      v-for="setting in settings"
      :key="setting.icon"
      v-model="setting.state"
      :name="setting.description"
      :icon="setting.icon"
    ></search-settings-item>
  </list>
</template>

<script setup>
import List from "../../UI/ListItems/List.vue";
import SearchSettingsItem from "./SearchSettingsItem.vue";
import { computed, reactive } from "vue";
import { useSearchStore } from "../../../stores/search";

const store = useSearchStore();

const graph = computed({
  get() {
    return store.searchGraph;
  },
  set(state) {
    store.setSearchGraph(state);
  },
});

const self = computed({
  get() {
    return store.searchSelf;
  },
  set(state) {
    store.setSearchSelf(state);
  },
});

const global = computed({
  get() {
    return store.searchGlobal;
  },
  set(state) {
    store.setSearchGlobal(state);
  },
});

const settings = reactive([
  {
    description: "Поиск по графу",
    icon: "mdi-graph",
    state: graph,
  },
  {
    description: "Поиск по вашим объектам",
    icon: "mdi-database-search-outline",
    state: self,
  },
  {
    description: "Глобальный поиск",
    icon: "mdi-account-search-outline",
    state: global,
  },
]);
</script>

<style scoped></style>
