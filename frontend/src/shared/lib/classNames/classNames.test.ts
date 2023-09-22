import { classNames } from 'shared/lib/classNames/classNames';

describe('classNames', () => {
  test('with only first param', () => {
    expect(classNames('someClass')).toBe('someClass');
  });

  test('with additional class', () => {
    const expected = 'someClass class1 class2';
    expect(classNames('someClass', {}, ['class1', 'class2'])).toBe(expected);
  });

  test('with mods', () => {
    const expected = 'someClass class1 class2 hovered visible';
    expect(
      classNames(
        'someClass',
        { hovered: true, scroll: false, visible: true },
        ['class1', 'class2']
      )
    ).toBe(expected);
  });

  test('with undefined mode', () => {
    const expected = 'someClass class1 class2 visible';
    expect(
      classNames(
        'someClass',
        { hovered: undefined, scroll: false, visible: true },
        ['class1', 'class2']
      )
    ).toBe(expected);
  });
});
