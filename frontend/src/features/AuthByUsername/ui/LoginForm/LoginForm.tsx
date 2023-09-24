import { classNames } from 'shared/lib/classNames/classNames';
import { useTranslation } from 'react-i18next';
import { Button, ButtonTheme } from 'shared/ui/Button/Button';
import { Input } from 'shared/ui/Input/Input';
import cls from './LoginForm.module.scss';
import { useDispatch, useSelector } from 'react-redux';
import { memo, useCallback, useEffect } from 'react';
import { authActions } from '../../model/slice/authSlice';
import { getAuthState } from '../../model/selectors/getLoginState/getLoginState';
import { Text, TextTheme } from 'shared/ui/Text/Text';
import { loginByUsername } from 'features/AuthByUsername/model/services/loginByUser/loginByUsername/loginByUsername';
import { registerUser } from 'features/AuthByUsername/model/services/registerUser/registerUser';

export enum FormTypes {
  AUTH = 'auth',
  REGISTER = 'register',
}
interface LoginFormProps {
  className?: string;
  typeForm: FormTypes;
  isVisible: boolean;
}

export const LoginForm = memo(({ className, typeForm, isVisible }: LoginFormProps) => {
  const { t } = useTranslation();
  const dispatch = useDispatch();

  const authForm = useSelector(getAuthState);
  const { username, password, error, isLoading } = authForm;

  const onChangeUsername = useCallback(
    (value: string) => {
      dispatch(authActions.setUsername(value));
    },
    [dispatch]
  );

  const onChangePassword = useCallback(
    (value: string) => {
      dispatch(authActions.setPassword(value));
    },
    [dispatch]
  );

  const onButtonClick = useCallback(() => {
    switch (typeForm) {
      case FormTypes.AUTH:
        dispatch(loginByUsername({ username, password }));
        break;
      case FormTypes.REGISTER:
        dispatch(registerUser({ username, password }));
        break;
    }
  }, [dispatch, username, password, typeForm]);

  useEffect(() => {
    return () => {
      dispatch(authActions.setUsername(''));
      dispatch(authActions.setPassword(''));
    };
  }, [dispatch, isVisible]);

  return (
    <div className={classNames(cls.LoginForm, {}, [className])}>
      {typeForm === FormTypes.AUTH && <Text title={t('Форма авторизации')} />}

      {typeForm === FormTypes.REGISTER && (
        <Text title={t('Форма регистрации')} />
      )}

      {error && <Text text={error} theme={TextTheme.ERROR} />}
      <Input
        autofocus
        type="text"
        className={cls.input}
        placeholder={t('Введите username')}
        onChange={onChangeUsername}
        value={username}
      />
      <Input
        type="text"
        className={cls.input}
        placeholder={t('Введите пароль')}
        onChange={onChangePassword}
        value={password}
      />
      <Button
        className={cls.loginBtn}
        theme={ButtonTheme.OUTLINE}
        onClick={onButtonClick}
        disabled={isLoading}
      >
        {typeForm === FormTypes.AUTH ? t('Войти') : t('Зарегистрироваться')}
      </Button>
    </div>
  );
});
