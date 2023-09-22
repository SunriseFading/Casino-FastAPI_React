import { $api } from 'shared/api/authApi';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { User, userActions } from 'entitites/User';
import i18n from 'shared/config/i18n/i18n';
import { USER_LOCALSTORAGE_KEY } from 'shared/const/localStorage';

interface LoginByUsernameProps {
  username: string;
  password: string;
}
export const loginByUsername = createAsyncThunk<
  User,
  LoginByUsernameProps,
  { rejectValue: string }
>('auth/loginByUsername', async (authData, thunkAPI) => {
  try {
    const response = await $api.post<User>('/login', authData);
    if (!response.data) {
      throw new Error();
    }
    localStorage.setItem(
      USER_LOCALSTORAGE_KEY,
      JSON.stringify(response.data.tokens.accessToken)
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
