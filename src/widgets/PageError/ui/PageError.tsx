import { classNames } from 'shared/lib/classNames/classNames';
import cls from './PageError.module.scss';
import { Button, ButtonTheme } from 'shared/ui/Button/Button';
import { useTranslation } from 'react-i18next';

interface PageErrorProps {
  className?: string;
}

export const PageError: React.FC<PageErrorProps> = ({ className }) => {
  const { t } = useTranslation();

  const reloadPage = () => {
    location.reload();
  };

  return (
    <div className={classNames(cls.PageError, {}, [className])}>
      <p>{t('Произошла непредвиденная ошибка')}</p>
      <Button theme={ButtonTheme.CLEAR} onClick={reloadPage}>{t('Обновить страницу')}</Button>
    </div>
  );
};
