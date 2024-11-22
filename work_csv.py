import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Button, Entry, Frame, Listbox, Scrollbar, END # графічний інтефейс
from tkinter.font import Font
from tkinter import messagebox

history = []  # список який буде служии історією запитів
df = None  # порожній фрейм для збереження великих данних
full_data = None  # обєданні данні


# завантаження csv
def load_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        try:
            global df, full_data
            # зчитування csv частинами для великих файлів
            df = pd.read_csv(filepath, chunksize=500000, encoding='utf-8')
            full_data = pd.concat(df, ignore_index=True)
            history.append(f"файл завантажено: {filepath}, {len(full_data)} записів")
            update_history()
            label_info['text'] = f"файл із {len(full_data)} записів завантажено!"
        except Exception as e:
            messagebox.showerror("помилка", f"не вдалося завантажити файл: {e}")

# оновлення історії запитів
def update_history():
    history_listbox.delete(0, END)
    for entry in history:
        history_listbox.insert(END, entry)


# вивід статистики
def show_statistics(column):
    if column in full_data.columns:
        try:
            # спроба перевірити даннні для числового формату
            col_data = pd.to_numeric(full_data[column], errors='coerce')
            
            # перевірка чи є хоча б одне число в колонці
            if col_data.isnull().all():
                label_result['text'] = f"у колонці {column} немає числових значень!"
                return

            # обчислення статистики
            mean_val = col_data.mean()
            min_val = col_data.min()
            max_val = col_data.max()

            label_result['text'] = f"{column}:\nсереднє: {mean_val}\nмінімум: {min_val}\nмаксимум: {max_val}"
            history.append(f"статистика для {column}: середнє={mean_val}, мін={min_val}, макс={max_val}")
            update_history()
        except Exception as e:
            label_result['text'] = f"Помилка при обчисленні статистики: {e}"
    else:
        label_result['text'] = "Стовпець не знайдено!"


# фільтрація данних
def filter_data(column, condition, value):
    if column in full_data.columns:
        try:
            # тут досить легкі умови, якщо користувач ввів у фільтр Більше то буде шукати числа > за якесь число
            # якщо Менше то < за якесь число# якщо Менше то < за якесь число
            # якщо Дорівнює то = за якесь число, в іншому випадку якщо не більше не менше і не дорівнює то виводиммо не правильна умова
            # ні? тоді не правильне значення, а якщо указаного тсовпця вообще нема то стовпець не знайденно
            # якщо люданна все зробила правильно то напише відповідь (вона буде різна порівнянно з іншими місяцями або стовпцями)
            value = float(value)
            if condition == "Більше":
                filtered = full_data[full_data[column] > value]
            elif condition == "Менше":
                filtered = full_data[full_data[column] < value]
            elif condition == "Дорівнює":
                filtered = full_data[full_data[column] == value]
            else:
                label_result['text'] = "неправильна умова!"
                return
            label_result['text'] = f"фільтровано: {len(filtered)} записів"
            history.append(f"фільтрація: {column} {condition} {value}, {len(filtered)} записів")
            update_history()
            filtered.to_csv("filtered_data.csv", index=False)
        except ValueError:
            label_result['text'] = "неправильне значення!"
    else:
        label_result['text'] = "стовпець не знайдено!"


# візуал для гіпсограми, тут досить я багато чого написав, але тут по суті більшість коду для візуалу і росписувати це буде самогупством бо його прям нереально довго писать
def visualize_data(column, chart_type="гістограма"):
    if column in full_data.columns:
        # застусування темної теми
        plt.style.use('dark_background')
        
        plt.figure(figsize=(10, 6))
        if chart_type.lower() == "гістограма":
            plt.hist(full_data[column].dropna(), bins=50, alpha=0.7, color='cyan', edgecolor='white')
            plt.title(f"гістограма для {column}", fontsize=16, color="white")
        elif chart_type.lower() == "лінійний графік":
            plt.plot(full_data[column].dropna(), alpha=0.7, color='lightgreen')
            plt.title(f"лінійний графік для {column}", fontsize=16, color="white")
        elif chart_type.lower() == "boxplot":
            plt.boxplot(full_data[column].dropna(), vert=False, patch_artist=True,
                        boxprops=dict(facecolor="purple", color="white"),
                        whiskerprops=dict(color="white"),
                        capprops=dict(color="white"),
                        medianprops=dict(color="yellow"))
            plt.title(f"вoxplot для {column}", fontsize=16, color="white")
        else:
            label_result['text'] = "невідомий тип діаграми!"
            return

        plt.xlabel(column, fontsize=14, color="white")
        plt.ylabel("частота", fontsize=14, color="white")
        plt.grid(visible=True, linestyle='--', alpha=0.5, color='gray')
        plt.show()

        history.append(f"візуалізація {chart_type} для {column}")
        update_history()
    else:
        label_result['text'] = "стовпець не знайдено!"


# графіка
win = Tk() # вікнно
win.title("X_PYTHON") # назва вікна
win.geometry("900x700")  # саме вікно

# кольри для темного режиму
bg_color = "#1E1E1E"  # темний фон
fg_color = "#D4D4D4"  # світлий текст
button_color = "#3C3C3C"  # темно-сірі кнопки
button_fg_color = "#FFFFFF"  # білий текст на кнопках
entry_bg_color = "#2D2D2D"  # темний фон для полів вводу
entry_fg_color = "#D4D4D4"  # світлий текст для полів вводу
highlight_color = "#007ACC"  # синій акцент

# шрифти
title_font = Font(family="Helvetica", size=16, weight="bold")
label_font = Font(family="Arial", size=12)
entry_font = Font(family="Arial", size=12)

# заголовок
label_title = Label(win, text="аналіз даних CSV", font=title_font, fg=fg_color, bg=bg_color, padx=10, pady=10)
label_title.pack(fill="x")

# рамка
frame_main = Frame(win, bg=bg_color, padx=10, pady=10)
frame_main.pack(fill="both", expand=True)

# інформація
label_info = Label(frame_main, text="завантажте файл для аналізу", font=label_font, bg=bg_color, fg=fg_color)
label_info.pack(pady=5)

button_load = Button(frame_main, text="завантажити CSV", command=load_csv, bg=button_color, fg=button_fg_color,
                     font=label_font, activebackground=highlight_color, activeforeground=fg_color)
button_load.pack(pady=10)

# введення назви стовпця (текст)
frame_input = Frame(frame_main, bg=bg_color)
frame_input.pack(pady=10)

entry_column = Entry(frame_input, width=20, font=entry_font, bg=entry_bg_color, fg=entry_fg_color, insertbackground=fg_color)
entry_column.grid(row=0, column=0, padx=5)
entry_column.insert(0, "Назва стовпця")

button_stats = Button(frame_input, text="статистика", command=lambda: show_statistics(entry_column.get()),
                      bg=button_color, fg=button_fg_color, font=label_font, activebackground=highlight_color,
                      activeforeground=fg_color)
button_stats.grid(row=0, column=1, padx=5)

button_visual = Button(frame_input, text="гістограма", command=lambda: visualize_data(entry_column.get(), "гістограма"),
                       bg=button_color, fg=button_fg_color, font=label_font, activebackground=highlight_color,
                       activeforeground=fg_color)
button_visual.grid(row=0, column=2, padx=5)

# фільтрація
frame_filter = Frame(frame_main, bg=bg_color)
frame_filter.pack(pady=10)

entry_condition = Entry(frame_filter, width=10, font=entry_font, bg=entry_bg_color, fg=entry_fg_color,
                        insertbackground=fg_color)
entry_condition.grid(row=0, column=0, padx=5)
entry_condition.insert(0, "умова")

entry_value = Entry(frame_filter, width=10, font=entry_font, bg=entry_bg_color, fg=entry_fg_color, insertbackground=fg_color)
entry_value.grid(row=0, column=1, padx=5)
entry_value.insert(0, "значення")

button_filter = Button(frame_filter, text="фільтрувати",
                       command=lambda: filter_data(entry_column.get(), entry_condition.get(), entry_value.get()),
                       bg=button_color, fg=button_fg_color, font=label_font, activebackground=highlight_color,
                       activeforeground=fg_color)
button_filter.grid(row=0, column=2, padx=5)

# історія запитів
frame_history = Frame(frame_main, bg=bg_color)
frame_history.pack(pady=10, fill="both", expand=True)

label_history = Label(frame_history, text="історія запитів", font=label_font, bg=bg_color, fg=fg_color)
label_history.pack()

scrollbar = Scrollbar(frame_history, bg=bg_color)
scrollbar.pack(side="right", fill="y")

history_listbox = Listbox(frame_history, font=entry_font, yscrollcommand=scrollbar.set, bg=entry_bg_color,
                          fg=entry_fg_color, highlightbackground=highlight_color, selectbackground=highlight_color)
history_listbox.pack(fill="both", expand=True)
scrollbar.config(command=history_listbox.yview)

# результат
label_result = Label(frame_main, text="", font=label_font, bg=bg_color, fg=fg_color)
label_result.pack(pady=10)

win.mainloop()