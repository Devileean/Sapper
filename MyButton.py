import tkinter as tk  # используем библиотеку tkinter и  даём ей псевдоним tk


class MyButton(tk.Button):
    """
    Отдельный класс для кнопки.
    Чтобы понимать располоение по координатам и саму сущность кнопки(мина,цифра или пустота)
    :return:
    """

    def __init__(self, master, x, y, *args, **kwargs):
        """
        Переопределяем класс Button под себя.
        :return:
        """
        super(MyButton, self).__init__(master, width=3, height=3, font='Calibri 15', *args, **kwargs)  # делаем своего рода конструктор
        self.x = x
        self.y = y
        self.is_mine = False

    def __repr__(self):
        """
        Метод который будет показывать, как будет выглядить обьект внутри консоли.
        :return:
        """
        return f'MyButton ({self.x} {self.y})'  # выводит координаты кнопок в консоль
