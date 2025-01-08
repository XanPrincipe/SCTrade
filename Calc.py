from tkinter import *
from tkinter.ttk import Combobox, Notebook
import pyperclip
from tkinter import filedialog as fd
import os
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *



# Основные цвета
PRIMARY_COLOR = "#1C1C1C"  # Тёмный фон
SECONDARY_COLOR = "#2A2A2A"  # Для второстепенных элементов
ACCENT_COLOR = "#DE9E07"  # Оранжевый акцент
TEXT_COLOR = "#FFFFFF"  # Белый текст
ENTRY_BG = "#333333"  # Цвет фона для полей ввода
HIGHLIGHT_COLOR = "#00FF00"  # Подсветка (зеленая)

# Определяем названия и соответствующие им ключи
prices = {
    'Огромные подарки': 'Huge',
    'Большие подарки': 'Big',
    'Старый скарб': 'Scarb',
    'Новогодний кейс': 'Winter_case',
    'Большие подарки наеб': 'Big2',
    'Запаски':'Zapaski',
    'Запаски наеб':'Zapaski2',
    'Запаски кента':'Zapaski3'
}
prices_dict = {'Huge': 10000, 'Big': 9000, 'Scarb': 26500, 'Winter_case': 120000, 'Big2': 8000, 'Zapaski':67000,
               'Zapaski2':66000, 'Zapaski3': 65000}

config_file = 'config.txt'
save_file = NONE


def move_focus_to_entry1(event=None):
    entry1.focus_set()


def move_focus_to_entry2(event=None):
    entry2.focus_set()


def move_focus_to_entry3(event=None):
    entry3.focus_set()


def move_focus_to_entry4(event=None):
    entry4.focus_set()


def move_focus_to_combobox1(event=None):
    combobox1.focus_set()


def move_focus_to_combobox2(event=None):
    combobox2.focus_set()


def move_focus_to_combobox3(event=None):
    combobox3.focus_set()


def move_focus_to_combobox4(event=None):
    combobox4.focus_set()


def show_copy_notification():
    notification_label.config(text="Текст скопирован в буфер обмена!")


def copy_to_clipboard(event=None):
    result_sum = result_label.cget("text")
    pyperclip.copy(result_sum)
    show_copy_notification()
    clear_entries()


def clear_entries():
    entry1_var.set("")
    entry2_var.set("")
    entry3_var.set("")
    entry4_var.set("")
    update_sum()


def update_sum(*args):
    try:
        selected_price1 = prices.get(combobox1.get(), 0)
        selected_price2 = prices.get(combobox2.get(), 0)
        selected_price3 = prices.get(combobox3.get(), 0)
        selected_price4 = prices.get(combobox4.get(), 0)

        n1 = int(entry1.get()) if entry1.get() else 0
        n2 = int(entry2.get()) if entry2.get() else 0
        n3 = int(entry3.get()) if entry3.get() else 0
        n4 = int(entry4.get()) if entry4.get() else 0

        total = (prices_dict.get(selected_price1, 0) * n1) + (prices_dict.get(selected_price2, 0) * n2) + (
                prices_dict.get(selected_price3, 0) * n3) + (prices_dict.get(selected_price4, 0) * n4)
        result_label.config(text=f"{total:,}".replace(',', ' '))
    except ValueError:
        result_label.config(text="Ошибка ввода!")
    except KeyError:
        result_label.config(text="Ошибка выбора!")


def choose_file():
    global save_file
    file_path = fd.askopenfilename(
        title="Выберите файл для загрузки текста",
        filetypes=[('Текстовые файлы', '*.txt'), ("Все файлы", "*.*")]
    )
    if file_path:
        save_file = file_path
        load_saved_text()
        save_config()


def load_config():
    global save_file
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding="UTF-8") as f:
            path = f.read().strip()
        if os.path.exists(path):
            save_file = path
            load_saved_text()


def save_text():
    global save_file
    if not save_file:
        save_file = fd.askopenfilename(
            title='Сохранить как',
            defaultextension='.txt',
            filetypes=[('Текстовые файлы', '*.txt'), ("Все файлы", "*.*")]
        )
    if save_file:
        content = copybook.get(1.0, "end-1c")
        with open(save_file, 'w', encoding="UTF-8") as f:
            f.write(content)


def save_config():
    if save_file:
        with open(config_file, 'w', encoding='UTF-8') as f:
            f.write(save_file)


def load_saved_text():
    global save_file
    if save_file and os.path.exists(save_file):
        with open(save_file, "r", encoding="utf-8") as f:
            content = f.read()
        copybook.delete(1.0, END)
        copybook.insert(1.0, content)


def copy_previous_text():
    previous_text = copybook.get(1.0, 'end-1c')
    if previous_text.strip():
        pyperclip.copy(previous_text)
        notification_label.config(text='Текст из вклакди спам скопирован!')
        clear_entries()
    else:
        notification_label.config(text='Вкладка "Спам" пуста!')

def open_window_calculator():
    subprocess.run('calc.exe')

# Применение тем оформления
def apply_theme(widget):
    widget.configure(
        bg=PRIMARY_COLOR,
        fg=TEXT_COLOR,
        insertbackground=HIGHLIGHT_COLOR,  # Цвет курсора в поле ввода
        highlightbackground=SECONDARY_COLOR,
        highlightthickness=0,
    )

# Применение тем для кнопок
def apply_button_theme(button):
    button.configure(
        bg=ACCENT_COLOR,
        fg=TEXT_COLOR,
        activebackground=HIGHLIGHT_COLOR,
        activeforeground=PRIMARY_COLOR,
        relief="flat",  # Плоский стиль кнопок
        borderwidth=0,
    )



window = ttk.Window(themename="darkly")
window.title("SCTrade - Аукцион")
window.geometry("500x600+750+300")
window.iconbitmap('images/ico.ico')

window.configure(bg="#1e1e1e")
# Создаем фрейм для центрирования содержимого


notebook = Notebook(window)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab1 = Frame(notebook,bg=PRIMARY_COLOR)
notebook.add(tab1, text='Главная')

tab2 = Frame(notebook,bg=PRIMARY_COLOR)
notebook.add(tab2, text='Спам')

tab3 = Frame(notebook,bg=PRIMARY_COLOR)
notebook.add(tab3, text='Цены')
# Главная форма


label_title = Label(tab1, font=("Consolas", 18), text="Расчет стоимости", fg=TEXT_COLOR,bg=PRIMARY_COLOR)
label_title.pack(pady=25)


# Извлекаем названия для отображения в Combobox
combobox_values = list(prices.keys())

combobox1 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
combobox1.pack(pady=5)
combobox1.bind("<<ComboboxSelected>>", move_focus_to_entry1)

entry1 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
entry1.pack(pady=5)
entry1.bind('<Return>', move_focus_to_entry2)
apply_theme(entry1)

combobox2 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
combobox2.pack(pady=5)
combobox2.bind("<<ComboboxSelected>>", move_focus_to_entry2)

entry2 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
entry2.pack(pady=5)
entry2.bind('<Return>', move_focus_to_entry3)
apply_theme(entry2)

combobox3 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
combobox3.pack(pady=5)
combobox3.bind("<<ComboboxSelected>>", move_focus_to_entry3)

entry3 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR)
entry3.pack(pady=5)
entry3.bind('<Return>', move_focus_to_entry4)
apply_theme(entry3)

combobox4 = Combobox(tab1, font=("Consolas", 12), values=combobox_values)
combobox4.pack(pady=5)
combobox4.bind("<<ComboboxSelected>>", move_focus_to_entry4)

entry4 = Entry(tab1, font=("Consolas", 12), width=22, bg=ENTRY_BG, fg=TEXT_COLOR,insertbackground="#00ff00")
entry4.pack(pady=5)
entry4.bind('<Return>', move_focus_to_entry1)
apply_theme(entry4)

# Обновляем сумму при изменении в полях ввода
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

result_label = Label(tab1, font=("Consolas", 12), text="0", fg=HIGHLIGHT_COLOR, bg=PRIMARY_COLOR, width=22, height=2, anchor='center')
result_label.pack(pady=2)
result_label.bind("<Button-1>", copy_to_clipboard)

button_copy_last_text = Button(tab1,text="Последний текст", font=("Consolas", 12),width=21, command=copy_previous_text)

apply_button_theme(button_copy_last_text)
button_copy_last_text.pack(pady=5)

button_open_calc = Button(tab1,text="Калькулятор", font=("Consolas", 12),width=21,command=open_window_calculator)

apply_button_theme(button_open_calc)
button_open_calc.pack(pady=5)

notification_label = Label(tab1, font=("Consolas", 12), text="", fg=ACCENT_COLOR, bg=PRIMARY_COLOR)
notification_label.pack(pady=7)

# Вкладка со спамом

spam_label = Label(tab2, text="Поле для текста", font=("Consolas", 12), fg=TEXT_COLOR, bg=PRIMARY_COLOR)
spam_label.pack(pady=5)

copybook = Text(tab2, font=("Consolas", 12), width=50, height=18, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="#00ff00")
copybook.pack(pady=5)

button_choose_file = Button(tab2, font=("Consolas", 12), text="Выбрать файл", width=22, bg="#E64961", fg="#ffffff",
                            activebackground="#D63E50", command=choose_file)
button_choose_file.pack(pady=5)

button_choose_file.pack(pady=5)
apply_button_theme(button_choose_file)

button_save = Button(tab2, font=("Consolas", 12), text="Сохранить", width=22, bg="#E64961", fg="#ffffff",
                     activebackground="#D63E50", command=save_text)
button_save.pack(pady=5)

button_save.pack(pady=5)
apply_button_theme(button_save)

# Вкладка с ценами

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

entry_widgets = {}

# Функция для сохранения цен в файл
def save_prices_to_file():
    global prices_dict
    for item, key in prices.items():
        if item in entry_widgets:
            try:
                new_price = int(entry_widgets[item].get())
                prices_dict[key] = new_price
            except ValueError:
                notification_label_tab3.config(text=f"Ошибка: Некорректное значение для '{item}'!")
                return

    with open("prices.txt", "w", encoding="utf-8") as file:
        for item, key in prices.items():
            file.write(f"{item}:{prices_dict[key]}\n")

    notification_label_tab3.config(text="Цены успешно сохранены!")

# Функция для обновления полей ввода на вкладке "Цены"
def update_price_entries():
    for item, key in prices.items():
        if item in entry_widgets:
            entry_widgets[item].delete(0, END)
            entry_widgets[item].insert(0, str(prices_dict[key]))



# Создаем поля для ввода цен
for idx, (item, key) in enumerate(prices.items()):
    Label(inner_frame_tab_3, text=item, font=("Consolas", 12), bg=SECONDARY_COLOR, fg=TEXT_COLOR, anchor="w").grid(
        row=idx, column=0, padx=10, pady=5, sticky="w"
    )

    entry_price = Entry(inner_frame_tab_3, font=("Consolas", 12), bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=HIGHLIGHT_COLOR, width=15)
    entry_price.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
    entry_widgets[item] = entry_price

# Обновляем значения полей ввода
update_price_entries()

def open_add_product_window():
    add_window = Toplevel(window)
    add_window.title('Добавить товар')
    add_window.iconbitmap('images/ico.ico')
    add_window.geometry('400x250+800+500')
    add_window.configure(bg=PRIMARY_COLOR)

    product_name = Label(add_window, text="Имя товара:", font=("Consolas", 12), bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack(pady=5)
    entry_name = Entry(add_window, font=("Consolas", 12), width=25, bg=ENTRY_BG, fg=TEXT_COLOR)
    entry_name.pack(pady=5)

    product_price = Label(add_window, text="Цена товара:", font=("Consolas", 12), bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack(pady=5)
    entry_price = Entry(add_window, font=("Consolas", 12), width=25, bg=ENTRY_BG, fg=TEXT_COLOR)
    entry_price.pack(pady=5)

    def add_product():
        name = entry_name.get().strip()
        price = entry_price.get().strip()
        if name and price.isdigit():
            # Добавить в prices и prices_dict
            key = name.replace(" ", "_")
            prices[name] = key
            prices_dict[key] = int(price)
            # Обновить интерфейс (например, через refresh)
            update_price_entries()
            add_window.destroy()
        else:
            print("Ошибка ввода!")

    button_frame_add_button = Frame(add_window, bg = 'green')
    button_frame_add_button.pack(pady=10)

    button_add = Button(button_frame_add_button, text="Добавить", font=("Consolas", 12), command=add_product)
    button_add.pack(side=LEFT,padx=10)
    apply_button_theme(button_add)

    button_cancel = Button(button_frame_add_button, text="Отмена",font=("Consolas", 12), command=add_window.destroy)
    button_cancel.pack(side=LEFT,padx=10)
    apply_button_theme(button_cancel)

# Кнопки управления ценами
button_frame_tab_3 = Frame(tab3, bg=PRIMARY_COLOR)
button_frame_tab_3.pack(fill=X, pady=10)

button_add_prices = Button(button_frame_tab_3, text="Добавить товар", font=("Consolas", 12),command=open_add_product_window)
button_add_prices.pack(side=LEFT, padx=10)
apply_button_theme(button_add_prices)

button_save_prices = Button(button_frame_tab_3, text="Сохранить цены", font=("Consolas", 12), command=save_prices_to_file)
button_save_prices.pack(side=LEFT, padx=10)
apply_button_theme(button_save_prices)

button_delete_prices = Button(button_frame_tab_3, text="Удалить товар", font=("Consolas", 12), command=save_prices_to_file)
button_delete_prices.pack(side=LEFT, padx=10)
apply_button_theme(button_delete_prices)

notification_label_tab3 = Label(tab3, text="", font=("Consolas", 12), bg=PRIMARY_COLOR, fg=ACCENT_COLOR)
notification_label_tab3.pack(pady=5)



load_config()
window.protocol("WM_DELETE_WINDOW", lambda: [save_text(), window.destroy()])

window.mainloop()

