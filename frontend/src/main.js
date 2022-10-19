import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import axios from "./plugins/axios";
import VueAxios from "vue-axios";
import vClickOutside from "click-outside-vue3";
import VNetworkGraph from "v-network-graph";

import "@mdi/font/css/materialdesignicons.css";
import "v-network-graph/lib/style.css";
import "./assets/main.css";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(VueAxios, axios);
app.use(vClickOutside);
app.use(VNetworkGraph);

app.mount("#app");
