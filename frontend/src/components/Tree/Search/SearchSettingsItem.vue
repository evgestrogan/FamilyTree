<template>
  <list-item @click.stop="value = !value">
    <list-item-icon>
      <icon class="text-xs" :icon="props.icon"></icon>
    </list-item-icon>
    <list-item-content>
      <list-item-content-subtitle class="text-xs text-left">{{
        props.name
      }}</list-item-content-subtitle>
    </list-item-content>
    <list-item-action>
      <input v-model="value" type="checkbox" class="cursor-pointer" />
    </list-item-action>
  </list-item>
</template>

<script setup>
import Icon from "../../UI/Icon.vue";
import ListItem from "../../UI/ListItems/ListItem.vue";
import ListItemIcon from "../../UI/ListItems/ListItemIcon.vue";
import ListItemContent from "../../UI/ListItems/ListItemContent.vue";
import ListItemContentSubtitle from "../../UI/ListItems/ListItemContentSubtitle.vue";
import ListItemAction from "../../UI/ListItems/ListItemAction.vue";
import { computed } from "vue";

const props = defineProps(["name", "icon", "modelValue"]);
const emit = defineEmits(["update:modelValue"]);

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});
</script>

<style scoped></style>
