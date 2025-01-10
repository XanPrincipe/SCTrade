from tkinter import *
from tkinter.ttk import Combobox, Notebook
from utils2 import update_sum, apply_theme, apply_button_theme, open_window_calculator, load_data_from_file,save_data_to_file
import pyperclip

PRIMARY_COLOR = "#1C1C1C"  # Тёмный фон
SECONDARY_COLOR = "#2A2A2A"  # Для второстепенных элементов
ACCENT_COLOR = "#DE9E07"  # Оранжевый акцент
TEXT_COLOR = "#FFFFFF"  # Белый текст
ENTRY_BG = "#333333"  # Цвет фона для полей ввода
HIGHLIGHT_COLOR = "#00FF00"  # Подсветка (зеленая)

font = ("Consolas", 12)
entry_width = 22
data_file = 'prices.txt'

prices = load_data_from_file(data_file)
combobox_values = list(prices.keys())

comboboxes = []
entries = []


def create_main_tab(notebook, window, copybook):

    tab1 = Frame(notebook, bg=PRIMARY_COLOR)
    notebook.add(tab1, text='Главная')

    label_title = Label(tab1, font=("Consolas", 18), text="Расчет стоимости", fg="#FFFFFF", bg="#1C1C1C")
    label_title.pack(pady=25)

    notebook = Notebook(window)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    for _ in range(4):
        combobox = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
        combobox.pack(pady=5)
        comboboxes.append(combobox)  # Добавляем в список

        entry = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
        entry.pack(pady=5)
        apply_theme(entry)
        entries.append(entry)


    def copy_to_clipboard(event=None):
        result_sum = result_label.cget("text")
        pyperclip.copy(result_sum)
        show_copy_notification()
        clear_entries()

    def copy_previous_text():
        previous_text = copybook.get(1.0, 'end-1c')
        if previous_text.strip():
            pyperclip.copy(previous_text)
            notification_label.config(text='Текст из вклакди спам скопирован!')
            clear_entries()
        else:
            notification_label.config(text='Вкладка "Спам" пуста!')


    result_label = Label(tab1, font=("Consolas", 12), text="0", fg=HIGHLIGHT_COLOR, bg=PRIMARY_COLOR, width=22,
                         height=2, anchor='center')
    result_label.pack(pady=2)
    result_label.bind("<Button-1>", copy_to_clipboard)

    button_copy_last_text = Button(tab1, text="Последний текст", font=("Consolas", 12), width=21,
                                   command=copy_previous_text)

    apply_button_theme(button_copy_last_text)
    button_copy_last_text.pack(pady=5)

    button_open_calc = Button(tab1, text="Калькулятор", font=("Consolas", 12), width=21, command=open_window_calculator)

    apply_button_theme(button_open_calc)
    button_open_calc.pack(pady=5)

    notification_label = Label(tab1, font=("Consolas", 12), text="", fg=ACCENT_COLOR, bg=PRIMARY_COLOR)
    notification_label.pack(pady=7)

    def update_sum(*args):
        try:
            # Получаем цены, связанные с выбранными элементами
            selected_prices = [prices.get(cb.get(), 0) for cb in comboboxes]

            # Получаем количества из полей ввода
            quantities = [int(entry.get()) if entry.get() else 0 for entry in entries]

            # Считаем общую сумму
            total = sum(price * qty for price, qty in zip(selected_prices, quantities))

            total_str = f"{int(total):,}".replace(",", " ")

            # Обновляем текст метки с результатом
            result_label.config(text=total_str)
        except ValueError:
            result_label.config(text="Ошибка ввода!")
        except KeyError:
            result_label.config(text="Ошибка выбора!")


    for combobox in comboboxes:
        combobox.bind("<<ComboboxSelected>>", update_sum)
    for entry in entries:
        entry.bind("<KeyRelease>", update_sum)

    def show_copy_notification():
        notification_label.config(text="Текст скопирован в буфер обмена!")

    def clear_entries():
        for entry in entries:
            entry.delete(0, END)
        update_sum()

    save_data_to_file(data_file,prices)

    return tab1