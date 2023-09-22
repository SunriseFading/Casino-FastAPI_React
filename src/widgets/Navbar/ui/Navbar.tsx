import { classNames } from 'shared/lib/classNames/classNames';
import { useTranslation } from 'react-i18next';
import { useCallback, useState } from 'react';
import { Button, ButtonTheme } from 'shared/ui/Button/Button';
import { LoginModal } from 'features/AuthByUsername';
import cls from './Navbar.module.scss';
import { useDispatch, useSelector } from 'react-redux';
import { getUserAuthData, userActions } from 'entitites/User';

interface NavbarProps {
  className?: string;
}

export const Navbar = ({ className }: NavbarProps) => {
  const { t } = useTranslation();

  const [isAuthForm, setIsAuthForm] = useState(false);
  const [isRegisterForm, setIsRegisterForm] = useState(false);
  const [isOpenForm, setIsOpenForm] = useState(false);

  const dispatch = useDispatch();
  const authData = useSelector(getUserAuthData);

  const onCloseModal = useCallback(() => {
    setIsOpenForm(false);
  }, []);

  const onShowAuthForm = useCallback(() => {
    setIsRegisterForm(false);
    setIsAuthForm(true);
    setIsOpenForm(true);
  }, []);

  const onShowRegisterForm = useCallback(() => {
    setIsAuthForm(false);
    setIsRegisterForm(true);
    setIsOpenForm(true);
  }, []);

  const onLogout = useCallback(() => {
    dispatch(userActions.logout());
  }, [dispatch]);

  if (authData?.tokens?.accessToken) {
    return (
      <div className={classNames(cls.Navbar, {}, [className])}>
        <Button
          theme={ButtonTheme.CLEAR_INVERTED}
          className={cls.links}
          onClick={onLogout}
        >
          {t('Выйти')}
        </Button>
      </div>
    );
  }

  return (
    <div className={classNames(cls.Navbar, {}, [className])}>
      <Button
        theme={ButtonTheme.CLEAR_INVERTED}
        className={cls.links}
        onClick={onShowAuthForm}
      >
        {t('Войти')}
      </Button>
      <Button
        theme={ButtonTheme.CLEAR_INVERTED}
        className={cls.links}
        onClick={onShowRegisterForm}
      >
        {t('Зарегистрироваться')}
      </Button>

      <LoginModal
        isAuthForm={isAuthForm}
        isRegisterForm={isRegisterForm}
        isOpen={isOpenForm}
        onClose={onCloseModal}
      />
    </div>
  );
};
