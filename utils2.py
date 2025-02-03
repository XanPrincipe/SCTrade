import subprocess
import os
from tkinter import filedialog as fd

PRIMARY_COLOR = "#1C1C1C"  # Тёмный фон
SECONDARY_COLOR = "#2A2A2A"  # Для второстепенных элементов
ACCENT_COLOR = "#DE9E07"  # Оранжевый акцент
TEXT_COLOR = "#FFFFFF"  # Белый текст
ENTRY_BG = "#333333"  # Цвет фона для полей ввода
HIGHLIGHT_COLOR = "#00FF00"  # Подсветка (зеленая)

def update_sum(entries, comboboxes, prices, prices_dict, result_label):
    try:
        # Получаем цены, связанные с выбранными элементами
        selected_prices = [prices.get(cb.get(), 0) for cb in comboboxes]

        # Получаем количества из полей ввода
        quantities = [int(entry.get()) if entry.get() else 0 for entry in entries]

        # Считаем общую сумму
        total = sum(prices_dict.get(price, 0) * qty for price, qty in zip(selected_prices, quantities))

        # Обновляем текст метки с результатом
        result_label.config(text=f"{total:,}".replace(',', ' '))
    except ValueError:
        result_label.config(text="Ошибка ввода!")
    except KeyError:
        result_label.config(text="Ошибка выбора!")

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
def open_window_calculator():
    subprocess.run('calc.exe')

def load_data_from_file(file_path):
    data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    data[key] = float(value)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except ValueError:
        print(f"Ошибка обработки данных в файле {file_path}. Проверьте формат.")
    return data

def save_data_to_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for key, value in data.items():
                file.write(f"{key}:{value}\n")
    except IOError:
        print(f"Ошибка записи в файл {file_path}.")


def on_close(copybook, window):
    global save_file
    if save_file:  # Проверяем, был ли ранее выбран файл
        save_text(copybook)  # Сохраняем только если уже есть файл
    window.destroy()

save_file = None

def save_text(copybook):
    global save_file  # Указываем, что используем глобальную переменную
    if not save_file:  # Если save_file еще не задан
        save_file = fd.askopenfilename(  # Открывается диалог сохранения
            title='Сохранить как',
            defaultextension='.txt',
            filetypes=[('Текстовые файлы', '*.txt'), ("Все файлы", "*.*")]
        )
    if save_file:  # Если файл был выбран
        content = copybook.get(1.0, "end-1c")  # Получаем содержимое
        with open(save_file, 'w', encoding="UTF-8") as f:
            f.write(content)
