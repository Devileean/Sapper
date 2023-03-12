import tkinter as tk  # используем библиотеку tkinter и  даём ей псевдоним tk


class MyButton(tk.Button):
    """
    Отдельный класс для кнопки.
    Чтобы понимать располоение по координатам и саму сущность кнопки(мина,цифра или пустота)
    :return:
    """

    def __init__(self, master, x, y, namber=0, *args, **kwargs):
        """
        Переопределяем класс Button под себя.
        :return:
        """
        super(MyButton, self).__init__(master, width=2, height=2, *args,
                                       **kwargs)  # делаем своего рода конструктор
        self.x = x  # координата по х
        self.y = y  # координата по y
        self.number = namber  # каждая кнопка будет иметь свой номер
        self.is_mine = False

    def __repr__(self):
        """
        Метод который будет показывать, как будет выглядить обьект внутри консоли.
        :return:
        """
        return f'MyButton:{self.number}({self.x};{self.y}) bomb({self.is_mine})'  # выводит координаты кнопок в консоль
