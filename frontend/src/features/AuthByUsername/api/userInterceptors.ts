import axios from 'axios';
import { User } from 'entitites/User';
import { $api, API_URL } from 'shared/api/authApi';
import { USER_LOCALSTORAGE_KEY } from 'shared/const/localStorage';

$api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem(
    USER_LOCALSTORAGE_KEY
  )}`;
  return config;
});

$api.interceptors.response.use(
  (config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem(
      USER_LOCALSTORAGE_KEY
    )}`;
    return config;
  },
  async (err) => {
    const originalRequest = err.config;
    if (err.response.status === 401 && !originalRequest._isRetry) {
      originalRequest._isRetry = true;
      try {
        const response = await axios.get<User>(`${API_URL}/refresh`, {
          withCredentials: true,
        });
        localStorage.setItem(
          USER_LOCALSTORAGE_KEY,
          response.data.tokens.accessToken
        );
        return await $api.request(originalRequest);
      } catch (e) {
        alert('Не авторизован');
      }
    }
    throw err;
  }
);

export default $api;
