<template>
  <list class="border-b relative">
    <span class="px-2 text-xs text-gray-400">
      <slot></slot>
    </span>
    <template v-if="props.items.length">
      <list-item v-for="item in limitedItems" :key="item.id">
        <list-item-icon class="hidden md:block">
          <img
            class="w-8 h-8 ml-3 rounded-full"
            src="http://127.0.0.1:5173/src/assets/profile.jpg"
            alt="user photo"
          />
        </list-item-icon>
        <list-item-content>
          <list-item-content-title>
            {{ item.name }}
          </list-item-content-title>
          <list-item-content-subtitle>
            {{ item.date }}
          </list-item-content-subtitle>
        </list-item-content>
      </list-item>
      <router-link
        v-if="limit"
        :to="moreLink"
        class="absolute bottom-0 right-0 px-2 text-xs text-indigo-400"
      >
        Ещё {{ remainder }}
      </router-link>
    </template>

    <list-item v-else>
      <list-item-content>
        <list-item-content-title>Ничего не найдено</list-item-content-title>
      </list-item-content>
    </list-item>
  </list>
</template>

<script setup>
import List from "../../UI/ListItems/List.vue";
import ListItem from "../../UI/ListItems/ListItem.vue";
import ListItemIcon from "../../UI/ListItems/ListItemIcon.vue";
import ListItemContent from "../../UI/ListItems/ListItemContent.vue";
import ListItemContentTitle from "../../UI/ListItems/ListItemContentTitle.vue";
import ListItemContentSubtitle from "../../UI/ListItems/ListItemContentSubtitle.vue";
import { computed } from "vue";

const props = defineProps({
  limit: {
    type: Number,
    default: null,
  },
  items: {
    type: Array,
  },
  variant: {
    type: String,
  },
});

const limitedItems = computed(() => {
  if (props.limit) {
    return props.items.slice(0, props.limit);
  } else {
    return props.items;
  }
});
const moreLink = computed(() =>
  Object.assign({ name: "Search", params: { variant: props.variant } })
);
const remainder = computed(() => props.items.length - props.limit);
</script>

<style scoped></style>
