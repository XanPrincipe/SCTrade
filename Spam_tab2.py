from tkinter import *
import os
from tkinter import filedialog as fd
from ttkbootstrap.constants import *
from tkinter.ttk import Combobox, Notebook

from utils2 import apply_button_theme,apply_theme

config_file = 'config.txt'
save_file = None


PRIMARY_COLOR = "#1C1C1C"  # Тёмный фон
SECONDARY_COLOR = "#2A2A2A"  # Для второстепенных элементов
ACCENT_COLOR = "#DE9E07"  # Оранжевый акцент
TEXT_COLOR = "#FFFFFF"  # Белый текст
ENTRY_BG = "#333333"  # Цвет фона для полей ввода
HIGHLIGHT_COLOR = "#00FF00"  # Подсветка (зеленая)



def save_config():
    if save_file:
        with open(config_file, 'w', encoding='UTF-8') as f:
            f.write(save_file)



def create_spam_tab(notebook):


    tab2 = Frame(notebook,bg=PRIMARY_COLOR)
    notebook.add(tab2, text='Спам')

    spam_label = Label(tab2, text="Поле для текста", font=("Consolas", 12), fg=TEXT_COLOR, bg=PRIMARY_COLOR)
    spam_label.pack(pady=5)

    copybook = Text(tab2, font=("Consolas", 12), width=50, height=18, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground="#00ff00")
    copybook.pack(pady=5)

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

    def load_config():
        global save_file
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding="UTF-8") as f:
                path = f.read().strip()
            if os.path.exists(path):
                save_file = path
                load_saved_text()

    def load_saved_text():
        global save_file
        if save_file and os.path.exists(save_file):
            with open(save_file, "r", encoding="utf-8") as f:
                content = f.read()
            copybook.delete(1.0, END)
            copybook.insert(1.0, content)

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

    load_config()
    load_saved_text()


    return tab2,copybook