import { createWebHistory, createRouter } from "vue-router";
import { useAuthorizationStore } from "../stores/authorization";
import authorization from "../router/authorization";
import workspace from "./workspace";

const routes = [
  workspace,
  authorization,
  // {
  //     path: '/:catchAll(.*)*',
  //     name: "PageNotFound",
  //     component: PageNotFound,
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const store = useAuthorizationStore();
  await store.refreshToken();
  if (store.accessToken) {
    if (to.meta.isAuth) {
      next();
    } else {
      next({ name: "Tree" });
    }
  } else {
    if (to.meta.isAuth) {
      next({ name: "Login" });
    } else {
      next();
    }
  }
});

export default router;
