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
        for i in range(MineSweeper.row + 2):  # перебираем по рядам
            temp = []
            for j in range(MineSweeper.columns + 2):  # перебираем по колонкам
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(
                    button))  # функция lamda является проводником для вызова функции click
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        # print(clicked_button)
        """
        Метод обработки нажатия кнопок.
        :return:
        """
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='blue', disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.number, disabledforeground='black')
        clicked_button.config(state='disabled')

    def create_widgets(self):
        """
        Метод интерфейса игры.
        :return:
        """
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]  # обращаемся к колонке по индексу
                btn.grid(row=i, column=j)

    def open_all_buttons(self):
        """
        временный метод для визуализации.
        :return:
        """
        for i in range(MineSweeper.row + 2):
            for j in range(MineSweeper.columns + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background='blue', disabledforeground='black')
                else:
                    btn.config(text=btn.count_bomb, disabledforeground='black')

    def start(self):
        """
        Метод запуска игры сапёр.
        :return:
        """
        self.create_widgets()  # вызываем виджеты
        self.insert_mines()  # вызываем мины
        self.count_mines_in_buttons()
        self.print_buttons()  # вызываем кнопки
        self.open_all_buttons()
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
        count = 1  # добавляем счетчик
        for i in range(1, MineSweeper.row + 1):  # обходим псевдо ряды
            for j in range(1, MineSweeper.columns + 1):  # обходим псевдо колонки
                btn = self.buttons[i][j]  # обращаемся к колонке по индексу
                btn.number = count
                if btn.number in index_mines:  # если у номер кнопки совпадает с номером индекса мины
                    btn.is_mine = True
                count += 1

    def count_mines_in_buttons(self):
        """
         Метод подсчета мин в потолках с вложенным циклом.

         :return:
         """
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:  # not создает отрицание
                    for row_dx in [-1, 0, 1]:  # вложенный цикл
                        for columns_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][
                                j + columns_dx]  # переменная для получения всех соседних кнопок
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

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
