<template>
  <div class="h-full w-full">
    <router-view></router-view>
    <v-network-graph
      class="!static"
      :nodes="nodes"
      :edges="edges"
      :layouts="layouts"
      :configs="configs"
      :event-handlers="eventHandlers"
    >
      <defs>
        <clipPath id="faceCircle" clipPathUnits="objectBoundingBox">
          <circle cx="0.5" cy="0.5" r="0.5" />
        </clipPath>
      </defs>
      <template #override-node="{ nodeId, scale, config, ...slotProps }">
        <image
          class="face-picture"
          :x="-config.radius * scale"
          :y="-config.radius * scale"
          :width="config.radius * scale * 2"
          :height="config.radius * scale * 2"
          :xlink:href="`http://127.0.0.1:5173/src/assets/${nodes[nodeId].face}`"
          clip-path="url(#faceCircle)"
        />
        <circle
          class="face-circle"
          :r="config.radius * scale"
          fill="none"
          :stroke-width="1 * scale"
          v-bind="slotProps"
        />
      </template>
    </v-network-graph>
    <context-menu v-model="ctxMenuShow" :conf="ctxMenuConf">
      <component :is="ctxMenuComponent"></component>
    </context-menu>
  </div>
</template>

<script setup>
import ContextMenu from "../UI/Context/ContextMenu.vue";
import NodeCtxMenu from "./CtxMenu/NodeCtxMenu.vue";
import EdgeCtxMenu from "./CtxMenu/EdgeCtxMenu.vue";
import ViewCtxMenu from "./CtxMenu/ViewCtxMenu.vue";
import * as vNG from "v-network-graph";
import { reactive, ref, shallowRef, nextTick } from "vue";

const ctxMenuShow = ref(false);
const ctxMenuComponent = shallowRef(ViewCtxMenu);
const ctxMenuConf = reactive({ x: 0, y: 0 });

function showCtxMenu(component) {
  function setPositionCtxMenu({ event }) {
    event.stopPropagation();
    event.preventDefault();
    ctxMenuShow.value = true;
    ctxMenuComponent.value = component;
    nextTick(() => {
      ctxMenuConf.x = event.x;
      ctxMenuConf.y = event.y;
    });
    const handler = (event) => {
      if (!event.target) {
        ctxMenuShow.value = false;
        document.removeEventListener("pointerdown", handler, { capture: true });
      }
    };
    document.addEventListener("pointerdown", handler, {
      passive: true,
      capture: true,
    });
  }

  return setPositionCtxMenu;
}

const eventHandlers = {
  "view:contextmenu": showCtxMenu(ViewCtxMenu),
  "node:contextmenu": showCtxMenu(NodeCtxMenu),
  "edge:contextmenu": showCtxMenu(EdgeCtxMenu),
};
const nodes = {
  node1: { name: "Dionysios Tijs Ruya", face: "1.jpeg" },
  node2: { name: "Roeland Caradoc Hafza", face: "2.jpeg" },
  node3: { name: "Ginnie Kalyana Hadewig", face: "3.jpeg" },
  node4: { name: "Toros Sigilind Davonte", face: "4.jpeg" },
};
const edges = {
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
};
const layouts = {
  nodes: {
    node1: { x: 0, y: 0 },
    node2: { x: 200, y: 200 },
    node3: { x: 400, y: 0 },
    node4: { x: 600, y: 200 },
  },
};
const configs = reactive(
  vNG.defineConfigs({
    view: {
      scalingObjects: true,
      minZoomLevel: 0.1,
      maxZoomLevel: 16,
      autoPanAndZoomOnLoad: "fit-content",
    },
  })
);
</script>

<style scoped>
.face-circle,
.face-picture {
  transition: all 0.1s linear;
}

.face-picture {
  pointer-events: none;
  border-radius: 50%;
}
</style>
