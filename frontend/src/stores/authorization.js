import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "../plugins/axios";
import config from "../plugins/config";
import router from "../router";

export const useAuthorizationStore = defineStore("authorization", () => {
  const accessToken = ref(null);
  const accessTimeOut = ref(null);

  function setAuthenticationData({ time_out: timeOut, access_token: access }) {
    accessToken.value = access;
    accessTimeOut.value = new Date(timeOut * 1000);
  }

  function removeAuthenticationData() {
    accessToken.value = false;
    accessTimeOut.value = null;
  }

  async function refresh() {
    await axios
      .get(config.URL.REFRESH)
      .then((r) => setAuthenticationData(r.data))
      .catch((e) => removeAuthenticationData());
  }

  async function refreshToken() {
    if (accessToken.value) {
      if (accessTimeOut.value - new Date() - 600000 <= 0) {
        await refresh();
      }
    } else if (accessToken.value === null) {
      await refresh();
    }
  }

  async function activate(key) {
    return await axios.put(`${config.URL.ACTIVATE}/${key}`);
  }

  async function changePassword({ password, key }) {
    return await axios
      .put(`${config.URL.CHANGE_PASSWORD}/${key}`, { password })
      .then((r) => {
        if (r.status === 200) {
          router.push({ name: "ChangePasswordConfirm", params: { key } });
        }
      });
  }

  async function login(user) {
    await axios
      .post(config.URL.LOGIN, user)
      .then((r) => {
        setAuthenticationData(r.data);
        router.push({ name: "Tree" });
      })
      .catch((e) => removeAuthenticationData());
  }

  async function logout() {
    await axios.get(config.URL.LOGOUT).finally((r) => {
      removeAuthenticationData();
      router.push({ name: "Login" });
    });
  }

  async function registration(user) {
    return await axios
      .post(config.URL.REGISTRATION, user)
      .then((r) => router.push({ name: "RegistrationConfirm" }))
      .catch((e) => {});
  }

  async function changePasswordPermission(key) {
    return await axios.get(`${config.URL.CHANGE_PASSWORD_PERMISSION}/${key}`);
  }

  async function forgotPasswordEmail(email) {
    await axios
      .post(config.URL.FORGOT_PASSWORD_EMAIL, { email })
      .then((r) => router.push({ name: "ForgotPasswordConfirm" }))
      .catch((e) => {});
  }

  return {
    accessToken,
    accessTimeOut,
    refreshToken,
    activate,
    login,
    logout,
    registration,
    changePassword,
    forgotPasswordEmail,
    changePasswordPermission,
  };
});
