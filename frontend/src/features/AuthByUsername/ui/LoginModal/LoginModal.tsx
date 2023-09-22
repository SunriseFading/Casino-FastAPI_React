import { classNames } from 'shared/lib/classNames/classNames';
import { Modal } from 'shared/ui/Modal/Modal';
import cls from './LoginModal.module.scss';
import { FormTypes, LoginForm } from '../LoginForm/LoginForm';

interface LoginModalProps {
  className?: string;
  isOpen: boolean;
  onClose: () => void;
  isAuthForm: boolean;
  isRegisterForm: boolean;
}

export const LoginModal = ({
  className,
  isOpen,
  onClose,
  isRegisterForm,
  isAuthForm,
}: LoginModalProps) => {
  const typeForm = isAuthForm ? FormTypes.AUTH : FormTypes.REGISTER;
  return (
    <Modal
      className={classNames(cls.LoginModal, {}, [className])}
      isOpen={isOpen}
      onClose={onClose}
      lazy
    >
      <LoginForm typeForm={typeForm} />
    </Modal>
  );
};
