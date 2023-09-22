import cls from './Loader.module.scss';

interface LoaderProps {
  className?: string;
}

export const Loader: React.FC<LoaderProps> = ({ className }) => {
  return <div className={cls.loader}></div>;
};
