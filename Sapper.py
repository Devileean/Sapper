import tkinter as tk  # используем библиотеку tkinter и  даём ей псевдоним tk

from MyButton import *
from random import shuffle


class MineSweeper:
    """
    Основной класс игры сапёр.
    :return:
    """
    window = tk.Tk()
    row = 5  # ряды
    columns = 5  # колонки
    mines = 10  # мины

    def __init__(self):
        print('start MineSweeper')
        self.buttons = []  # массив кнопок
        count = 1  # добавляем счетчик
        for i in range(MineSweeper.row):  # перебираем по рядам
            temp = []
            for j in range(MineSweeper.columns):  # перебираем по колонкам
                btn = MyButton(MineSweeper.window, x=i, y=j, namber=count)
                btn.config(command=lambda button=btn: self.click(
                    button))  # функция lamda является проводником для вызова функции click
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        # print(clicked_button)
        """
        Метод обработки нажатия кнопок.
        :return:
        """
        if clicked_button.is_mine:
            clicked_button.config(text="*",background='blue', disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.number, disabledforeground='black')
        clicked_button.config(state='disabled')

    def create_widgets(self):
        """
        Метод интерфейса игры.
        :return:
        """
        for i in range(MineSweeper.row):
            for j in range(MineSweeper.row):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        """
        Метод запуска игры сапёр.
        :return:
        """
        self.create_widgets()  # вызываем виджеты
        self.insert_mines()  # вызываем мины
        self.print_buttons()  # вызываем кнопки
        MineSweeper.window.mainloop()

    def print_buttons(self):
        """
         Метод распечатки кнопок игры сапёр.
         :return:
         """
        for row_btn in self.buttons:
            print(row_btn)

    def insert_mines(self):
        """
         Метод расставления мин.
         :return:
         """
        index_mines = self.get_mines_places()
        for row_btn in self.buttons:
            for btn in row_btn:
                if btn.number in index_mines:  # если у номер кнопки совпадает с номером индекса мины
                    btn.is_mine = True

    @staticmethod
    def get_mines_places():
        """
         Метод получения расположения мин.
         Возвращает только индексы мин.
         :return:
         """
        indexes = list(range(1, MineSweeper.columns * MineSweeper.row + 1))
        shuffle(indexes)
        return indexes[:MineSweeper.mines]


game = MineSweeper()  # запуск класса
game.start()  # в момент запуска - запускается mainloop
