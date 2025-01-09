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




def create_main_tab(notebook, window, copybook):

    tab1 = Frame(notebook, bg=PRIMARY_COLOR)
    notebook.add(tab1, text='Главная')

    label_title = Label(tab1, font=("Consolas", 18), text="Расчет стоимости", fg="#FFFFFF", bg="#1C1C1C")
    label_title.pack(pady=25)

    notebook = Notebook(window)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)


    combobox1 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
    combobox1.pack(pady=5)


    entry1 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
    entry1.pack(pady=5)
    apply_theme(entry1)

    combobox2 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
    combobox2.pack(pady=5)


    entry2 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
    entry2.pack(pady=5)
    apply_theme(entry2)

    combobox3 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
    combobox3.pack(pady=5)


    entry3 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
    entry3.pack(pady=5)
    apply_theme(entry3)

    combobox4 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
    combobox4.pack(pady=5)

    entry4 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR,insertbackground="#00ff00")
    entry4.pack(pady=5)
    apply_theme(entry4)

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

    entry1_var = StringVar()
    entry2_var = StringVar()
    entry3_var = StringVar()
    entry4_var = StringVar()
    combobox1_var = StringVar()
    combobox2_var = StringVar()
    combobox3_var = StringVar()
    combobox4_var = StringVar()

    entry1.config(textvariable=entry1_var)
    entry2.config(textvariable=entry2_var)
    entry3.config(textvariable=entry3_var)
    entry4.config(textvariable=entry4_var)
    combobox1.config(textvariable=combobox1_var)
    combobox2.config(textvariable=combobox2_var)
    combobox3.config(textvariable=combobox3_var)
    combobox4.config(textvariable=combobox4_var)

    entry1_var.trace_add('write', update_sum)
    entry2_var.trace_add('write', update_sum)
    entry3_var.trace_add('write', update_sum)
    entry4_var.trace_add('write', update_sum)
    combobox1_var.trace_add('write', update_sum)
    combobox2_var.trace_add('write', update_sum)
    combobox3_var.trace_add('write', update_sum)
    combobox4_var.trace_add('write', update_sum)

    def show_copy_notification():
        notification_label.config(text="Текст скопирован в буфер обмена!")


    def clear_entries():
        entry1_var.set("")
        entry2_var.set("")
        entry3_var.set("")
        entry4_var.set("")
        update_sum()

    save_data_to_file(data_file,prices)

    return tab1