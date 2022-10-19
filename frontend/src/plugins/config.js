const URL = {
  LOGIN: "authentication/login",
  REGISTRATION: "authentication/registration",
  LOGOUT: "authentication/logout",
  ACTIVATE: "authentication/activate",
  REFRESH: "authentication/refresh",
  FORGOT_PASSWORD_EMAIL: "authentication/start_recovery_password",
  CHANGE_PASSWORD_PERMISSION: "authentication/check_recovery_password",
  CHANGE_PASSWORD: "authentication/recovery_password",
};

const EXTEND_ACCESS_URL = [
  URL.ACTIVATE,
  URL.REFRESH,
  URL.REGISTRATION,
  URL.FORGOT_PASSWORD_EMAIL,
  URL.CHANGE_PASSWORD_PERMISSION,
  URL.CHANGE_PASSWORD,
];

const MESSAGE_STATUS_CODE = {
  [URL.LOGIN]: {
    403: "Проверьте введенные данные",
  },
  [URL.REGISTRATION]: {
    409: "Данный email уже зарегистрирован в системе",
  },
  [URL.LOGOUT]: {
    403: "Вы не аутентифицированы",
  },
  [URL.ACTIVATE]: {
    404: "У вас нет доступа к данному ресурсу",
    408: "Время подтверждения вышло. Пройдите регистрацию повторно",
    422: "Вы не имеете права на доступ к данному ресурсу",
  },
  [URL.FORGOT_PASSWORD_EMAIL]: {
    404: "Данный email отсутствует в системе",
  },
  [URL.CHANGE_PASSWORD_PERMISSION]: {
    403: "Для изменения пароля, перейдите по ссылке, указанной в письме",
  },
  [URL.CHANGE_PASSWORD]: {
    403: "У вас нет прав для данного действия",
    406: "Вы не можете изменить пароль на тот же, который был",
  },
};
export default {
  URL,
  EXTEND_ACCESS_URL,
  MESSAGE_STATUS_CODE,
};
