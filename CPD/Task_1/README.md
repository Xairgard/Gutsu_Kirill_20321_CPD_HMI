## Задание
1. Графический интерфейс:
   - Основное окно со списком активных процессов.
   - Возможность обновления списка процессов.
   - Информационная панель, отображающая общие ресурсы системы (использование ЦП, памяти и т. д.).

2. Список процессов:
   - Отображение PID (идентификатор процесса).
   - Отображение имени процесса.
   - Отображение использования ЦП и памяти конкретным процессом.
   - Возможность завершения выбранного процесса.
   - Возможность отсортировать список процессов по различным параметрам (например, использование ЦП, памяти).

3. Информационная панель. 
Обновление в реальном времени (matplotlib. FigureCanvasTkAgg):
   - Графическое представление загрузки ЦП.
   - Графическое представление использования оперативной памяти.
   - Графическое представление использования дискового пространства.
   - Отображение загруженности сети (загрузка/выгрузка).

4.:
   - Поиск процессов по имени.
   - Возможность просмотра дополнительной информации о процессе (например, путь к исполняемому файлу, время запуска).
   - Возможность изменения приоритета процесса.

5. Настройки и предпочтения:
   - Возможность выбора интервала обновления информации (например, каждые 2 секунды, 5 секунд и т. д.).

6. Безопасность и стабильность:
   - Информирование пользователя о потенциально опасных действиях (например, предупреждение при попытке завершить какой-либо процесс (напр. важный системный процесс)).

## Листинг
```Py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import datetime  # Добавлен импорт для форматирования времени

class ProcessManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Диспетчер задач")
        self.geometry("1000x600")

        # Treeview для отображения списка процессов
        self.process_tree = ttk.Treeview(self, columns=("PID", "Name", "CPU", "Memory"), show="headings")
        self.process_tree.heading("PID", text="PID", command=lambda: self.sort_column("PID", False))
        self.process_tree.heading("Name", text="Name", command=lambda: self.sort_column("Name", False))
        self.process_tree.heading("CPU", text="CPU (%)", command=lambda: self.sort_column("CPU", False))
        self.process_tree.heading("Memory", text="Memory (MB)", command=lambda: self.sort_column("Memory", False))

        self.process_tree.column("PID", width=50)
        self.process_tree.column("Name", width=200)
        self.process_tree.column("CPU", width=80)
        self.process_tree.column("Memory", width=80)

        self.process_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar для списка процессов
        process_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.process_tree.yview)
        process_scrollbar.grid(row=0, column=1, sticky="ns")
        self.process_tree.configure(yscrollcommand=process_scrollbar.set)

        # Кнопка обновления списка процессов
        refresh_button = ttk.Button(self, text="Обновить процессы", command=self.refresh_processes)
        refresh_button.grid(row=1, column=0, pady=10)

        # Кнопка завершения выбранного процесса
        kill_button = ttk.Button(self, text="Завершить процесс", command=self.kill_selected_process)
        kill_button.grid(row=1, column=1, pady=10)

        # Информационная панель
        self.info_label = tk.Label(self, text="")
        self.info_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Выбор интервала обновления
        self.update_interval_label = tk.Label(self, text="Интервал обновления:")
        self.update_interval_label.grid(row=3, column=0, pady=10)

        self.update_interval_values = [1, 2, 5, 10, 30]  # Возможные значения интервала в секундах
        self.update_interval_var = tk.StringVar(value=self.update_interval_values[0])
        self.update_interval_combobox = ttk.Combobox(self, values=self.update_interval_values, textvariable=self.update_interval_var)
        self.update_interval_combobox.grid(row=3, column=1, pady=10)
        self.update_interval_combobox.bind("<<ComboboxSelected>>", self.update_interval_changed)

        # Поле ввода для поиска процессов по имени
        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(row=4, column=0, pady=10, padx=10, sticky="ew")
        self.search_entry.insert(0, "")

        # Кнопка выполнения поиска
        search_button = ttk.Button(self, text="Поиск", command=self.search_process)
        search_button.grid(row=4, column=1, pady=10)

        # Графики для информационной панели
        self.fig, self.ax = plt.subplots(2, 2, figsize=(8, 6))
        self.fig.subplots_adjust(hspace=0.5)  # Увеличиваем расстояние между графиками
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=3, padx=10, pady=10)

        # Переменные для графиков
        self.cpu_data = []
        self.memory_data = []
        self.disk_data = []
        self.network_data = []

        # Интервал обновления информации в миллисекундах
        self.update_interval = 1000  # Значение по умолчанию

        # Запуск обновления информации
        self.after(0, self.update_info)

        # Задаем вес столбцов и строк
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Обновляем список процессов
        self.refresh_processes()

    def refresh_processes(self):
        # Очищаем Treeview перед обновлением
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        # Получаем список активных процессов
        processes = psutil.process_iter()
        for process in processes:
            try:
                process_info = process.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_info'])
                self.process_tree.insert("", tk.END, values=(
                    process_info['pid'],
                    process_info['name'],
                    f"{process_info['cpu_percent']:.2f}",
                    f"{process_info['memory_info'].rss / (1024 ** 2):.2f}"
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Обновляем информационную панель
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        self.info_label.config(text=f"Использование CPU: {cpu_usage:.2f}% | Использование памяти: {memory_usage:.2f}%")

    def kill_selected_process(self):
        selected_items = self.process_tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Процесс не выбран. Выберите процесс.")
            return

        selected_pid = int(self.process_tree.item(selected_items[0], 'values')[0])

        try:
            process = psutil.Process(selected_pid)
            process.terminate()
            messagebox.showinfo("Информация", f"Процесс {selected_pid} успешно завершен.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.TimeoutExpired):
            messagebox.showerror("Ошибка", f"Невозможно завершить процесс {selected_pid}.")

    def sort_column(self, col, reverse):
        # Определение типа данных для сортировки
        data_type = int if col == 'PID' else float if col in ['CPU', 'Memory'] else str

        items = [(data_type(self.process_tree.set(k, col)), k) for k in self.process_tree.get_children('')]
        items.sort(reverse=reverse)

        for index, (val, k) in enumerate(items):
            self.process_tree.move(k, '', index)

        self.process_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def update_info(self):
        # Обновление списка процессов
        self.refresh_processes()

        # Обновление графиков
        self.update_plots()

        # Повторное выполнение через указанный интервал
        self.after(self.update_interval, self.update_info)

    def update_plots(self):
        # Обновление данных для графиков
        self.cpu_data.append(psutil.cpu_percent())
        self.memory_data.append(psutil.virtual_memory().percent)
        self.disk_data.append(psutil.disk_usage('/').percent)
        self.network_data.append(psutil.net_io_counters().bytes_recv / 1024 / 1024)

        # Отображение данных на графиках
        self.plot_graph(self.ax[0, 0], self.cpu_data, 'Использование CPU', 'Время', 'Проценты')
        self.plot_graph(self.ax[0, 1], self.memory_data, 'Использование памяти', 'Время', 'Проценты')
        self.plot_graph(self.ax[1, 0], self.disk_data, 'Использование диска', 'Время', 'Проценты')
        self.plot_graph(self.ax[1, 1], self.network_data, 'Использование сети', 'Время', 'MB/s')

        # Обновление отображения
        self.canvas.draw()

    def plot_graph(self, ax, data, title, xlabel, ylabel):
        ax.clear()
        ax.plot(np.arange(len(data)), data, label=title)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()

    def update_interval_changed(self, event):
        # Обработка изменения интервала обновления
        selected_interval = int(self.update_interval_var.get())
        self.update_interval = selected_interval * 1000  # Переводим в миллисекунды

    def search_process(self):
        # Получаем имя процесса из поля ввода
        process_name = self.search_entry.get()

        # Очищаем Treeview перед поиском
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        # Ищем процессы по имени
        processes = psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info'])
        for process in processes:
            try:
                if process_name.lower() in process.info['name'].lower():
                    self.process_tree.insert("", tk.END, values=(
                        process.info['pid'],
                        process.info['name'],
                        f"{process.info['cpu_percent']:.2f}",
                        f"{process.info['memory_info'].rss / (1024 ** 2):.2f}"
                    ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def show_process_info(self):
        selected_items = self.process_tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Процесс не выбран. Выберите процесс.")
            return

        selected_pid = int(self.process_tree.item(selected_items[0], 'values')[0])

        try:
            process = psutil.Process(selected_pid)
            process_info = f"ID процесса: {selected_pid}\n"
            process_info += f"Имя: {process.name()}\n"
            process_info += f"Путь: {process.exe()}\n"
            process_info += f"Время создания: {self.format_time(process.create_time())}"

            messagebox.showinfo("Информация о процессе", process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.TimeoutExpired):
            messagebox.showerror("Ошибка", f"Невозможно получить информацию о процессе {selected_pid}.")

    def format_time(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    app = ProcessManagerApp()
    app.mainloop()

```

## Скриншот

![alt text](https://github.com/Xairgard/Gutsu_Kirill_20321_CPD_HMI/blob/main/CPD/Task_1/Image1.png)

## Пояснение

1. Создается окно приложения, содержащее виджет Treeview для отображения списка процессов с информацией о PID, имени, использовании CPU и памяти.
2. Метод `refresh_processes` обновляет Treeview, отображая текущие активные процессы с использованием библиотеки psutil.
3. Метод `kill_selected_process` завершает выбранный процесс с использованием библиотеки psutil.
4. Реализована сортировка данных в Treeview по различным столбцам (PID, Name, CPU, Memory) с возможностью изменения порядка сортировки.
5. В верхней части приложения представлена информационная панель с текущим использованием CPU и памяти.
6. Интегрированы графики для отображения использования CPU, памяти, дискового пространства и сети в реальном времени с использованием библиотеки Matplotlib.
7. Добавлена возможность выбора интервала обновления данных, например, каждые 1, 2, 5 секунд.
8. Добавлен функционал поиска процессов по имени с обновлением Treeview.
9. Реализована возможность просмотра дополнительной информации о выбранном процессе, такой как путь к исполняемому файлу и время запуска.
10. Пока не включено в код, но предусмотрено для будущих модификаций.
11. Некоторые проверки добавлены для обработки исключений, таких как отсутствие процесса или отказ в доступе.
12. Добавлены комментарии на русском языке, обеспечивающие понимание функций и блоков кода. Код структурирован в виде класса для легкости понимания и поддержки.
