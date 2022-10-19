import { useAuthorizationStore } from "../stores/authorization";
import { useNotificationStore } from "../stores/notification";
import axios from "axios";
import config from "./config";

const http = axios.create({
  baseURL: "http://127.0.0.1:8000/",
  withCredentials: true,
});

http.interceptors.request.use(
  async function (requestConfig) {
    const store = useAuthorizationStore();
    if (!config.EXTEND_ACCESS_URL.includes(requestConfig.url)) {
      await store.refreshToken();
      requestConfig.headers["x-access-token"] = store.accessToken;
    }
    return requestConfig;
  },
  function (error) {
    return Promise.reject(error);
  }
);

function findValueByPrefix(prefix) {
  for (const property in config.MESSAGE_STATUS_CODE) {
    if (
      config.MESSAGE_STATUS_CODE.hasOwnProperty(property) &&
      prefix.startsWith(property)
    ) {
      return config.MESSAGE_STATUS_CODE[property];
    }
  }
}

http.interceptors.response.use(
  function (response) {
    return response;
  },
  async function (er) {
    const store = useNotificationStore();
    const error = er.toJSON();
    const type = "error";
    const code = error.status;
    const time = new Date().toLocaleString("ru-RU", {
      dateStyle: "short",
      timeStyle: "short",
    });
    const body =
      findValueByPrefix(error.config.url)[code] || "Неизвестная ошибка сервера";
    await store.addAlert({ type, time, body, code });
    return Promise.reject(er);
  }
);

export default http;
