<template>
  <div
    ref="ctx"
    v-show="show"
    v-click-outside="close"
    class="absolute bg-white py-2 rounded-md shadow-xl"
    :style="position"
  >
    <slot></slot>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

const emit = defineEmits(["update:modelValue"]);
const props = defineProps(["modelValue", "conf"]);
const ctx = ref(null);

const position = computed(() => {
  let offsetX = 0;
  let offsetY = 0;
  if (ctx.value) {
    let tempOffsetX =
      document.body.clientWidth - (props.conf.x + ctx.value.clientWidth);
    let tempOffsetY =
      document.body.clientHeight - (props.conf.y + ctx.value.clientHeight);
    if (tempOffsetX < 0) {
      offsetX = tempOffsetX;
    }
    if (tempOffsetY < 0) {
      offsetY = tempOffsetY;
    }
  }
  return {
    left: `${props.conf.x + offsetX}px`,
    top: `${props.conf.y + offsetY}px`,
  };
});

const show = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});
function close() {
  show.value = false;
}
</script>

<style scoped></style>
