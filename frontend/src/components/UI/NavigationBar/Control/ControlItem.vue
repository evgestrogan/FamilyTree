<template>
  <list-item>
    <list-item-icon>
      <icon :icon="icon"></icon>
    </list-item-icon>
    <list-item-content class="hidden sm:flex">
      <list-item-content-title>{{ title }}</list-item-content-title>
      <list-item-content-subtitle>{{ subtitle }}</list-item-content-subtitle>
    </list-item-content>
  </list-item>
</template>

<script setup>
import Icon from "../../Icon.vue";
import ListItem from "../../ListItems/ListItem.vue";
import ListItemIcon from "../../ListItems/ListItemIcon.vue";
import ListItemContent from "../../ListItems/ListItemContent.vue";
import ListItemContentTitle from "../../ListItems/ListItemContentTitle.vue";
import ListItemContentSubtitle from "../../ListItems/ListItemContentSubtitle.vue";

const { title, subtitle, icon } = defineProps({
  title: String,
  subtitle: String,
  icon: String,
});
</script>

<style scoped></style>
