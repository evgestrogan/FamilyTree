<template>
  <div class="h-full overflow-y-auto border">
    <list>
      <list-item v-for="i in 19" class="border-y my-1">
        <list-item-content class="whitespace-nowrap">
          <list-item-content-title>
            Petrov Petr Petrovich
          </list-item-content-title>
        </list-item-content>
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

<style scoped>

</style>