import axios from 'axios';
import { $api, API_URL } from 'shared/api/authApi';
import { USER_LOCALSTORAGE_KEY } from 'shared/const/localStorage';
import { AuthResponse } from '../model/types/authSchema';

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
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._isRetry) {
      originalRequest._isRetry = true;
      try {
        const response = await axios.get<AuthResponse>(
          `${API_URL}/users/refresh`,
          {
            withCredentials: true,
          }
        );
        localStorage.setItem(USER_LOCALSTORAGE_KEY, response.data.access_token);
        return await $api.request(originalRequest);
      } catch (e) {
        alert('Авторизуйтесь снова');
        localStorage.removeItem(USER_LOCALSTORAGE_KEY);
      }
    }
    throw error;
  }
);

export default $api;
