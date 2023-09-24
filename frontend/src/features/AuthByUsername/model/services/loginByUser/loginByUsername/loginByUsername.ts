import { $api } from 'shared/api/authApi';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { userActions } from 'entitites/User';
import i18n from 'shared/config/i18n/i18n';
import { USER_LOCALSTORAGE_KEY } from 'shared/const/localStorage';
import { AuthResponse } from 'features/AuthByUsername/model/types/authSchema';

interface LoginByUsernameRequest {
  username: string;
  password: string;
}
export const loginByUsername = createAsyncThunk<
  AuthResponse,
  LoginByUsernameRequest,
  { rejectValue: string }
>('auth/loginByUsername', async (authData, thunkAPI) => {
  try {
    const response = await $api.post<AuthResponse>('/users/login', authData);
    if (!response.data) {
      throw new Error();
    }
    localStorage.setItem(
      USER_LOCALSTORAGE_KEY,
      JSON.stringify(response.data.access_token)
    );
    thunkAPI.dispatch(userActions.setAuthData(response.data));
    return response.data;
  } catch (e) {
    console.log(e);
    return thunkAPI.rejectWithValue(
      i18n.t('Вы ввели неверный логин или пароль')
    );
  }
});
