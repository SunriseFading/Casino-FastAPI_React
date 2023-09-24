import { classNames } from 'shared/lib/classNames/classNames';
import { useTranslation } from 'react-i18next';
import { useCallback, useState } from 'react';
import { Button, ButtonTheme } from 'shared/ui/Button/Button';
import { FormTypes, LoginModal } from 'features/AuthByUsername';
import cls from './Navbar.module.scss';
import { useDispatch, useSelector } from 'react-redux';
import { getUserAuthData, userActions } from 'entitites/User';

interface NavbarProps {
  className?: string;
}

export const Navbar = ({ className }: NavbarProps) => {
  const { t } = useTranslation();

  const [typeForm, setTypeForm] = useState<FormTypes>(FormTypes.REGISTER);
  const [isOpenForm, setIsOpenForm] = useState(false);

  const dispatch = useDispatch();
  const authData = useSelector(getUserAuthData);

  const onCloseModal = useCallback(() => {
    setIsOpenForm(false);
  }, []);

  const onShowAuthForm = useCallback(() => {
    setTypeForm(FormTypes.AUTH);
    setIsOpenForm(true);
  }, []);

  const onShowRegisterForm = useCallback(() => {
    setTypeForm(FormTypes.REGISTER);
    setIsOpenForm(true);
  }, []);

  const onLogout = useCallback(() => {
    dispatch(userActions.logout());
    setIsOpenForm(false);
  }, [dispatch]);

  if (authData?.access_token) {
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
        typeForm={typeForm}
        isOpen={isOpenForm}
        onClose={onCloseModal}
      />
    </div>
  );
};
