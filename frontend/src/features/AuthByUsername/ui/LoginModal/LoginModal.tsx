import { classNames } from 'shared/lib/classNames/classNames';
import { Modal } from 'shared/ui/Modal/Modal';
import cls from './LoginModal.module.scss';
import { FormTypes, LoginForm } from '../LoginForm/LoginForm';

interface LoginModalProps {
  className?: string;
  isOpen: boolean;
  onClose: () => void;
  typeForm: FormTypes;
}

export const LoginModal = ({
  className,
  isOpen,
  onClose,
  typeForm,
}: LoginModalProps) => {
  return (
    <Modal
      className={classNames(cls.LoginModal, {}, [className])}
      isOpen={isOpen}
      onClose={onClose}
      lazy
    >
      <LoginForm isVisible={isOpen} typeForm={typeForm} />
    </Modal>
  );
};
