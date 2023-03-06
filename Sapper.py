import tkinter as tk  # используем библиотеку tkinter и  даём ей псевдоним tk


class MineSweeper:
    """
    Основной класс игры сапёр.
    :return:
    """
    window = tk.Tk()
    row = 10                                                            # ряды
    columns = 10                                                        # колонки

    def __init__(self):
        print('start MineSweeper')
        self.buttons = []                                               # массив кнопок
        for i in range(MineSweeper.row):                                # перебираем по рядам
            temp = []
            for j in range(MineSweeper.columns):                        # перебираем по колонкам
                btn = tk.Button(MineSweeper.window, width=3, height=3)  # ширина кнопок и высота font='Calibri 15 bold'
                temp.append(btn)
            self.buttons.append(temp)

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
        self.create_widgets()
        self.print_buttons()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        """
         Метод распечатки кнопок игры сапёр.
         :return:
         """
        for row_btn in self.buttons:
            print(row_btn)


game = MineSweeper()                                                  # запуск класса
game.start()                                                          # в момент запуска - запускается mainloop




