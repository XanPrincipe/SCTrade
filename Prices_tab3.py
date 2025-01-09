from tkinter import *
from utils2 import apply_theme, apply_button_theme

PRIMARY_COLOR = "#1C1C1C"  # Тёмный фон
SECONDARY_COLOR = "#2A2A2A"  # Для второстепенных элементов
ACCENT_COLOR = "#DE9E07"  # Оранжевый акцент
TEXT_COLOR = "#FFFFFF"  # Белый текст
ENTRY_BG = "#333333"  # Цвет фона для полей ввода
HIGHLIGHT_COLOR = "#00FF00"  # Подсветка (зеленая)

FILENAME = "prices.txt"

def load_prices():
    """Загрузка цен из файла."""
    prices = {}
    try:
        with open(FILENAME, "r",encoding='UTF-8') as file:
            for line in file:
                key, value = line.strip().split(":", 1)
                prices[key] = value
    except FileNotFoundError:
        pass
    return prices

def save_prices(prices):
    """Сохранение цен в файл."""
    with open(FILENAME, "w", encoding='UTF-8') as file:
        for key, value in prices.items():
            file.write(f"{key}:{value}\n")

def create_prices_tab(notebook):
    tab3 = Frame(notebook, bg=PRIMARY_COLOR)

    # Хранилище цен
    prices = load_prices()

    def update_entries():
        """Обновляет список полей ввода."""
        for widget in inner_frame_tab_3.winfo_children():
            widget.destroy()

        for idx, (key, value) in enumerate(prices.items()):

            name_entry = Entry(inner_frame_tab_3,font=("Consolas", 12), width=18,
                               bg=ENTRY_BG, fg=TEXT_COLOR)
            name_entry.insert(0, key)
            name_entry.grid(row=idx, column=1, padx=5, pady=5)
            apply_theme(name_entry)

            price_entry = Entry(inner_frame_tab_3,font=("Consolas", 12), width=18,
                                bg=ENTRY_BG, fg=TEXT_COLOR)
            price_entry.insert(0, value)
            price_entry.grid(row=idx, column=2, padx=5, pady=5)
            apply_theme(price_entry)

            delete_button = Button(inner_frame_tab_3,font=("Consolas", 12), width=18,
                                   text="Удалить", command=lambda k=key: delete_entry(k),
                                   bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
            delete_button.grid(row=idx, column=3, padx=5, pady=5)
            apply_button_theme(delete_button)

    def add_entry():
        """Добавляет новую запись."""
        prices[f"{len(prices) + 1}"] = "0"
        update_entries()

    def delete_entry(key):
        """Удаляет запись."""
        if key in prices:
            del prices[key]
        update_entries()

    def save_all_entries():
        """Сохраняет все текущие записи."""
        new_prices = {}
        for idx, (key, value) in enumerate(prices.items()):
            name_entry = inner_frame_tab_3.grid_slaves(row=idx, column=1)[0]
            price_entry = inner_frame_tab_3.grid_slaves(row=idx, column=2)[0]
            new_key = name_entry.get()
            new_value = price_entry.get()
            if new_key and new_value:
                new_prices[new_key] = new_value
        save_prices(new_prices)
        update_entries()

    frame_canvas_tab_3 = Frame(tab3, bg=PRIMARY_COLOR)
    frame_canvas_tab_3.pack(expand=True, fill=BOTH, padx=10, pady=10)

    canvas_tab_3 = Canvas(frame_canvas_tab_3, bg=SECONDARY_COLOR, highlightthickness=0)
    canvas_tab_3.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar_tab_3 = Scrollbar(frame_canvas_tab_3, orient=VERTICAL, command=canvas_tab_3.yview, bg=SECONDARY_COLOR)
    scrollbar_tab_3.pack(side=RIGHT, fill=Y)

    canvas_tab_3.configure(yscrollcommand=scrollbar_tab_3.set)
    canvas_tab_3.bind(
        "<Configure>",
        lambda e: canvas_tab_3.configure(scrollregion=canvas_tab_3.bbox("all"))
    )

    inner_frame_tab_3 = Frame(canvas_tab_3, bg=SECONDARY_COLOR)
    canvas_tab_3.create_window((0, 0), window=inner_frame_tab_3, anchor="nw")

    # Панель кнопок
    button_frame = Frame(tab3, bg=PRIMARY_COLOR)
    button_frame.pack(fill=X, padx=10, pady=5)

    add_button = Button(button_frame, text="Добавить запись", command=add_entry, bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    add_button.pack(side=LEFT, padx=5)

    save_button = Button(button_frame, text="Сохранить", command=save_all_entries, bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    save_button.pack(side=LEFT, padx=5)

    update_entries()

    return tab3