import { createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { User, userActions } from 'entitites/User';
import { API_URL } from 'shared/api/authApi';
import { USER_LOCALSTORAGE_KEY } from 'shared/const/localStorage';
import { AuthResponse } from '../../types/authSchema';

export const checkAuth = createAsyncThunk<User>(
  'auth/checkAuth',
  async (_, thunkAPI) => {
    try {
      const response = await axios.get<AuthResponse>(`${API_URL}/users/refresh`, {
        withCredentials: true,
      });

      localStorage.setItem(
        USER_LOCALSTORAGE_KEY,
        JSON.stringify(response.data.access_token)
      );
      thunkAPI.dispatch(userActions.setAuthData(response.data));
      return response.data;
    } catch (e) {
      console.log(e);
    }
  }
);
