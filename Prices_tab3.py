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
    """Загрузка цен из файла."""
    prices = {}
    try:
        with open(FILENAME, "r", encoding="UTF-8") as file:
            for line in file:
                key, value = line.strip().split(":", 1)
                try:
                    num_value = float(value)
                    if num_value.is_integer():
                        value = str(int(num_value))  # Убираем .0
                    else:
                        value = str(num_value)
                except ValueError:
                    pass  # Если вдруг значение не число, оставляем как есть
                prices[key] = value
    except FileNotFoundError:
        pass
    return prices


def save_prices(prices):
    """Сохранение цен в файл."""
    with open(FILENAME, "w", encoding='UTF-8') as file:
        for key, value in prices.items():
            file.write(f"{key}:{value}\n")


def create_prices_tab(notebook, window):
    tab3 = Frame(notebook, bg=PRIMARY_COLOR, padx=5)

    # Загружаем иконку и изменяем размер
    original_image = Image.open("images/trash.png")  # Путь к иконке
    resized_image = original_image.resize((20, 20))  # Новый размер
    trash_icon = ImageTk.PhotoImage(resized_image)

    # Хранилище цен
    prices = load_prices()

    def update_entries():
        """Обновляет список полей ввода."""
        for widget in inner_frame_tab_3.winfo_children():
            widget.destroy()

        # Обертка для центрирования
        wrapper_frame = Frame(inner_frame_tab_3, bg=SECONDARY_COLOR)
        wrapper_frame.pack(expand=True, pady=10)  # Центрируем контент

        for idx, (key, value) in enumerate(prices.items()):
            row_frame = Frame(wrapper_frame, bg=SECONDARY_COLOR)
            row_frame.pack(fill=X, padx=50, pady=5)  # Добавляем отступы

            name_entry = Entry(row_frame, font=("Consolas", 12), width=22,
                               bg=ENTRY_BG, fg=TEXT_COLOR)
            name_entry.insert(0, key)
            name_entry.pack(side=LEFT, padx=5)  # Используем pack вместо grid
            apply_theme(name_entry)

            price_entry = Entry(row_frame, font=("Consolas", 12), width=10,
                                bg=ENTRY_BG, fg=TEXT_COLOR)
            price_entry.insert(0, value)
            price_entry.pack(side=LEFT, padx=5)
            apply_theme(price_entry)

            delete_button = Button(row_frame, image=trash_icon, command=lambda k=key: delete_entry(k),
                                   highlightthickness=0, borderwidth=0)
            delete_button.image = trash_icon
            delete_button.pack(side=LEFT, padx=5)

    def add_entry():
        """Добавляет новую запись."""
        prices[""] = ""  # Добавляем новую пустую запись
        update_entries()

    def delete_entry(key):
        """Удаляет запись."""
        if key in prices:
            del prices[key]
        update_entries()

    def save_all_entries():
        """Сохраняет все текущие записи, выводит ошибку при пустых полях."""
        new_prices = {}
        empty_fields = False  # Флаг для проверки пустых полей

        for idx, (key, value) in enumerate(prices.items()):
            # Ищем все Entry в каждом ряду
            row_frame = inner_frame_tab_3.winfo_children()[idx]  # Каждый ряд (Frame)

            name_entry = row_frame.winfo_children()[0]  # Первое поле в ряду (название)
            price_entry = row_frame.winfo_children()[1]  # Второе поле в ряду (цена)

            new_key = name_entry.get().strip()
            new_value = price_entry.get().strip()

            if not new_key or not new_value:  # Если хотя бы одно поле пустое
                empty_fields = True
                break  # Достаточно одной ошибки, выходим из цикла

            new_prices[new_key] = new_value

        if empty_fields:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        else:
            save_prices(new_prices)
            update_entries()

    def update_scroll_region(event=None):
        """Обновляет область прокрутки"""
        canvas_tab_3.configure(scrollregion=canvas_tab_3.bbox("all"))

    def on_mouse_scroll(event):
        """Позволяет прокручивать колесиком мыши"""
        canvas_tab_3.yview_scroll(-1 * (event.delta // 120), "units")

    frame_canvas_tab_3 = Frame(tab3, bg=PRIMARY_COLOR)
    frame_canvas_tab_3.pack(expand=True, fill=BOTH, padx=10, pady=10)

    canvas_tab_3 = Canvas(frame_canvas_tab_3, bg=SECONDARY_COLOR, highlightthickness=0)
    canvas_tab_3.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar_tab_3 = Scrollbar(frame_canvas_tab_3, orient=VERTICAL, command=canvas_tab_3.yview, bg=SECONDARY_COLOR)
    scrollbar_tab_3.pack(side=RIGHT, fill=Y)

    canvas_tab_3.configure(yscrollcommand=scrollbar_tab_3.set)

    inner_frame_tab_3 = Frame(canvas_tab_3, bg=SECONDARY_COLOR)
    canvas_tab_3.create_window((0, 0), window=inner_frame_tab_3, anchor="nw")

    inner_frame_tab_3.bind("<Configure>", update_scroll_region)
    canvas_tab_3.bind_all("<MouseWheel>", on_mouse_scroll)

    # Панель кнопок
    button_frame = Frame(tab3, bg=PRIMARY_COLOR)
    button_frame.pack(fill=X, padx=10, pady=5)

    add_button = Button(button_frame, font=("Consolas", 12), text="Добавить запись", width=22, bg="#E64961",
                        fg="#ffffff", activebackground="#D63E50", command=add_entry)
    add_button.pack(side=LEFT, padx=5)
    apply_button_theme(add_button)

    save_button = Button(button_frame, font=("Consolas", 12), text="Сохранить", width=22, bg="#E64961",
                         fg="#ffffff", activebackground="#D63E50", command=save_all_entries)
    save_button.pack(side=LEFT, padx=5)
    apply_button_theme(save_button)

    update_entries()

    return tab3
