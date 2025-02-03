from tkinter import *
from utils2 import apply_theme, apply_button_theme, update_sum
from PIL import Image, ImageTk
from tkinter import messagebox


PRIMARY_COLOR = "#1C1C1C"  # Тёмный фон
SECONDARY_COLOR = "#2A2A2A"  # Для второстепенных элементов
ACCENT_COLOR = "#DE9E07"  # Оранжевый акцент
TEXT_COLOR = "#FFFFFF"  # Белый текст
ENTRY_BG = "#333333"  # Цвет фона для полей ввода

FILENAME = "prices.txt"


def load_prices():
    """Загружаем данные из файла и убираем .0 у целых чисел."""
    prices = {}
    try:
        with open(FILENAME, "r", encoding="UTF-8") as file:
            for line in file:
                key, value = line.strip().split(":", 1)
                try:
                    num_value = float(value)
                    if num_value.is_integer():
                        value = str(int(num_value))  # Преобразуем в целое
                    else:
                        value = str(num_value)  # Оставляем как есть
                except ValueError:
                    pass  # Если не число, оставляем как есть
                prices[key] = value
    except FileNotFoundError:
        pass  # Если файла нет, возвращаем пустой словарь
    return prices

def create_prices_tab(notebook, window, update_main_tab, clear_entries):
    """Создаёт вкладку с редактированием цен."""
    tab3 = Frame(notebook, bg=PRIMARY_COLOR, padx=5, pady=5)
    notebook.add(tab3, text="Редактирование цен")

    # Фрейм с канвасом и скроллбаром
    frame_canvas = Frame(tab3, bg=PRIMARY_COLOR)
    frame_canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)

    canvas = Canvas(frame_canvas, bg=SECONDARY_COLOR, highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame_canvas, orient=VERTICAL, command=canvas.yview, bg=SECONDARY_COLOR)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = Frame(canvas, bg=SECONDARY_COLOR)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def update_scroll_region(event=None):
        """Обновляет область прокрутки."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", update_scroll_region)

    def load_prices():
        """Загружает данные из файла и убирает лишние нули после запятой."""
        prices = {}
        try:
            with open(FILENAME, "r", encoding="UTF-8") as file:
                for line in file:
                    key, value = line.strip().split(":", 1)
                    try:
                        num_value = float(value)
                        if num_value.is_integer():
                            value = str(int(num_value))  # Преобразуем в целое, если возможно
                        else:
                            value = str(num_value)  # Иначе оставляем как есть
                    except ValueError:
                        pass  # Если не число, оставляем строку как есть
                    prices[key] = value
        except FileNotFoundError:
            pass  # Если файла нет, возвращаем пустой словарь
        return prices

    def save_prices():
        """Сохраняет данные из полей ввода в файл."""
        new_prices = {}

        for row_frame in inner_frame.winfo_children():
            widgets = row_frame.winfo_children()
            if len(widgets) < 2:
                continue  # Пропускаем некорректные строки

            name = widgets[0].get().strip()
            price = widgets[1].get().strip()

            if not name or not price:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            new_prices[name] = price

        # Записываем в файл
        with open(FILENAME, "w", encoding="UTF-8") as file:
            for key, value in new_prices.items():
                file.write(f"{key}:{value}\n")

        update_main_tab()
        clear_entries()

    def delete_entry(row_frame):
        """Удаляет строку из интерфейса и обновляет файл."""
        row_frame.destroy()
        save_prices()  # После удаления сразу пересохраняем файл

    def add_entry(name="", price=""):
        """Добавляет новую строку."""
        row_frame = Frame(inner_frame, bg=SECONDARY_COLOR)
        row_frame.pack(fill=X, padx=50, pady=5)

        name_entry = Entry(row_frame, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
        name_entry.pack(side=LEFT, padx=5)
        name_entry.insert(0, name)

        price_entry = Entry(row_frame, font=("Consolas", 12), width=10, bg=ENTRY_BG, fg=TEXT_COLOR)
        price_entry.pack(side=LEFT, padx=5)
        price_entry.insert(0, price)

        delete_button = Button(row_frame, text="Удалить", font=("Consolas", 12), width=10, bg="#E64961", fg="#ffffff",
                               activebackground="#D63E50", command=lambda: delete_entry(row_frame))
        delete_button.pack(side=RIGHT, padx=5)

        update_scroll_region()

    # Загружаем данные и создаём строки
    prices = load_prices()
    for key, value in prices.items():
        add_entry(key, value)

    # Панель кнопок
    button_frame = Frame(tab3, bg=PRIMARY_COLOR)
    button_frame.pack(fill=X, padx=10, pady=5)

    add_button = Button(button_frame, font=("Consolas", 12), text="Добавить запись", width=22, bg="#E64961",
                        fg="#ffffff", activebackground="#D63E50", command=lambda: add_entry())
    apply_button_theme(add_button)
    add_button.pack(side=LEFT, padx=5)

    save_button = Button(button_frame, font=("Consolas", 12), text="Сохранить", width=22, bg="#E64961",
                         fg="#ffffff", activebackground="#D63E50", command=save_prices)
    apply_button_theme(save_button)
    save_button.pack(side=LEFT, padx=5)

    return tab3
