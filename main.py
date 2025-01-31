
from tkinter.ttk import Notebook
import ttkbootstrap as ttk
from Main_tab1 import create_main_tab
from Spam_tab2 import create_spam_tab
from Prices_tab3 import create_prices_tab, load_prices
from utils2 import on_close
# Инициализация основного окна
window = ttk.Window(themename="darkly")
window.title("SCTrade - Аукцион")
window.geometry("500x600+750+300")
window.iconbitmap('images/ico.ico')
window.configure(bg="#1e1e1e")

# Создание вкладок
notebook = Notebook(window)
notebook.pack(expand=True, fill="both", padx=10, pady=10)


tab2, copybook = create_spam_tab(notebook)
tab1 = create_main_tab(notebook, window, copybook)
tab3 = create_prices_tab(notebook, window)

# Добавление вкладок в Notebook
notebook.insert(0,tab1, text='Главная')
notebook.add(tab2, text='Спам')
notebook.add(tab3, text='Цены')

notebook.select(tab1)
# Загрузка конфигурации и данных
load_prices()

# Закрытие приложения с сохранением данных
window.protocol("WM_DELETE_WINDOW", lambda: on_close(copybook, window))

window.mainloop()
