<template>
  <div class="h-full overflow-y-auto border">
    <list>
      <list-item v-for="i in 19" :key="i" class="border-y my-1">
        <list-item-content class="whitespace-nowrap">
          <list-item-content-title>
            Ivanov Ivan Ivanovich {{ i }}
          </list-item-content-title>
          <list-item-content-subtitle>
            27.12.1988 - 20.11.2020
          </list-item-content-subtitle>
        </list-item-content>
        <list-item-action>
          <input type="checkbox" class="w-5 h-5" />
        </list-item-action>
      </list-item>
    </list>
  </div>
</template>

<script setup>
import List from "../UI/ListItems/List.vue";
import ListItem from "../UI/ListItems/ListItem.vue";
import ListItemContent from "../UI/ListItems/ListItemContent.vue";
import ListItemContentTitle from "../UI/ListItems/ListItemContentTitle.vue";
import ListItemContentSubtitle from "../UI/ListItems/ListItemContentSubtitle.vue";
import ListItemAction from "../UI/ListItems/ListItemAction.vue";
</script>

<style scoped></style>
