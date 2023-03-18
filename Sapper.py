import tkinter

from MyButton import *
from random import shuffle
from tkinter.messagebox import showinfo, showerror  # позволят создавать диалоговое окно

colors = {  # переменная для хранения словаря для присвоения цвета цифрам
    1: '#cc103f',
    2: '#0ccfcf',
    3: '#0f6bdb',
    4: '#c606d4',
    5: '#d3d60d',
    6: '#ed8224',
    7: '#5cc406',
    8: '#6f3dc4'
}


class MineSweeper:
    """
    Основной класс игры сапёр.
    :return:
    """
    window = tk.Tk()
    row = 10  # ряды
    columns = 10  # колонки
    mines = 20  # мины
    is_game_over = False  # если подрыв или конец игры
    is_first_click = True  # чтобы исключить мину при первом нажатии

    def __init__(self):
        print('start MineSweeper')
        self.buttons = []  # массив кнопок
        for i in range(MineSweeper.row + 2):  # перебираем по рядам
            temp = []
            for j in range(MineSweeper.columns + 2):  # перебираем по колонкам
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(
                    button))  # функция lamda является проводником для вызова функции click
                btn.bind('<Button-2>', self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):
        """
        Метод чтобы помечать кнопки флажком правой кнопкой мышки.
        :return:
        """
        if MineSweeper.is_game_over:
            return
        current_btn = event.widget
        if current_btn['state'] == 'normal':
            current_btn['state'] = 'disabled'
            current_btn['text'] = '🚩'
        elif current_btn['text'] == '🚩':
            current_btn['text'] = ''
            current_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):
        """
        Метод обработки нажатия кнопок.
        :return:
        """
        if MineSweeper.is_game_over:
            return

        if MineSweeper.is_first_click:
            self.insert_mines(clicked_button.number)  # вызываем мины
            self.count_mines_in_buttons()
            self.print_buttons()  # вызываем кнопки
            MineSweeper.is_first_click = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", highlightbackground="red", disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.is_game_over = True
            showinfo('game over', 'Вы проиграли')
            for i in range(1, MineSweeper.row + 1):  # этот цикл открывает все мины при подрыве
                for j in range(1, MineSweeper.columns + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
                        btn['highlightbackground'] = 'red'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        """
        Метод поиск в ширину.
        :return:
        """
        queue = [btn]  # создаем очередь
        while queue:
            current_btn = queue.pop()  # создаем переменную дя текущей кнопки
            color = colors.get(current_btn.count_bomb, 'black')
            if current_btn.count_bomb:
                current_btn.config(text=current_btn.count_bomb, disabledforeground=color)
            else:
                current_btn.config(text='', disabledforeground=color)
            current_btn.is_open = True
            current_btn.config(state='disabled')
            current_btn.config(relief=tk.SUNKEN)

            if current_btn.count_bomb == 0:
                x = current_btn.x
                y = current_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:  #  не позволяло открывать на искосок
                        #     continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.row and \
                                1 <= next_btn.y <= MineSweeper.columns and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        """
        Метод перезапуска игры.
        :return:
        """
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.is_first_click = True
        MineSweeper.is_game_over = False

    def create_settings_window(self):
        """
        Метод создания отдельного окна с настройками игры.
        :return:
        """
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')

        tk.Label(win_settings, text='Количество строк:').grid(row=0, column=0)
        row_entry = tkinter.Entry(win_settings)
        row_entry.insert(0, MineSweeper.row)
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество колонок:').grid(row=1, column=0)
        columns_entry = tkinter.Entry(win_settings)
        columns_entry.insert(0, MineSweeper.columns)
        columns_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество мин:').grid(row=2, column=0)
        mines_entry = tkinter.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.mines)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, columns_entry, mines_entry))
        save_btn.grid(row=3, column=2, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, columns: tk.Entry, mines: tk.Entry):
        """
        Метод инициализации настроек игры.
        :return:
        """
        try:
            int(row.get()), int(columns.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение!')
            return
        MineSweeper.row = int(row.get())
        MineSweeper.columns = int(columns.get())
        MineSweeper.mines = int(mines.get())
        self.reload()

    def create_widgets(self):
        """
        Метод интерфейса игры.
        :return:
        """
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        setting_menu = tk.Menu(menu_bar, tearoff=0)
        setting_menu.add_command(label='Играть', command=self.reload)
        setting_menu.add_command(label='Настройки', command=self.create_settings_window)
        setting_menu.add_command(label='Выход', command=self.window.destroy)
        menu_bar.add_cascade(label='Файл', menu=setting_menu)

        count = 1  # добавляем счетчик
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]  # обращаемся к колонке по индексу
                btn.number = count
                btn.grid(row=i, column=j, stick='NWSE')
                count += 1

        for i in range(1, MineSweeper.row + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

            for i in range(1, MineSweeper.columns + 1):
                tk.Grid.rowconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        """
        временный метод для визуализации.
        :return:
        """
        for i in range(MineSweeper.row + 2):
            for j in range(MineSweeper.columns + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", highlightbackground='blue', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        """
        Метод запуска игры сапёр.
        :return:
        """
        self.create_widgets()  # вызываем виджеты
        # self.open_all_buttons()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        """
         Метод распечатки кнопок игры сапёр.
         Помогает смотреть вывод игрового поля в консоли.
         :return:
         """
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.columns + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('*', end=' ')  # параметром end= убераем переносы строк
                else:
                    print(btn.count_bomb, end=' ')
            print()  # делаем пустой принт чтобы разделить вывод информации по рядам

    def insert_mines(self, number: int):
        """
         Метод расставления мин.
         :return:
         """
        index_mines = self.get_mines_places(number)
        for i in range(1, MineSweeper.row + 1):  # обходим псевдо ряды
            for j in range(1, MineSweeper.columns + 1):  # обходим псевдо колонки
                btn = self.buttons[i][j]  # обращаемся к колонке по индексу
                if btn.number in index_mines:  # если у номер кнопки совпадает с номером индекса мины
                    btn.is_mine = True

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
    def get_mines_places(exclude_number: int):
        """
         Метод получения расположения мин.
         Возвращает только индексы мин.
         :return:
         """
        indexes = list(range(1, MineSweeper.columns * MineSweeper.row + 1))
        print(f'Исключаем кнопку номер {exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.mines]


game = MineSweeper()  # запуск класса
game.start()  # в момент запуска - запускается mainloop
