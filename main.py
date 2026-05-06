import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# --- НАЧАЛЬНЫЕ ДАННЫЕ ---
# Список предопределенных задач. Каждая задача — это словарь.
PREDEFINED_TASKS = [
    {"name": "Прочитать статью", "category": "учёба"},
    {"name": "Сделать зарядку", "category": "спорт"},
    {"name": "Написать отчёт", "category": "работа"},
    {"name": "Посмотреть лекцию", "category": "учёба"},
    {"name": "Пробежка", "category": "спорт"},
    {"name": "Составить план", "category": "работа"},
]

# Имя файла для сохранения истории
HISTORY_FILE = "tasks.json"


class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        # Загружаем историю из файла при запуске
        self.history = self.load_history()

        # --- ВИДЖЕТЫ ИНТЕРФЕЙСА ---

        # Текущая задача
        self.task_label = tk.Label(root, text="Ваша задача:", font=("Arial", 14))
        self.task_label.pack(pady=10)

        self.task_display = tk.Label(root, text="", font=("Arial", 16, "bold"), wraplength=350)
        self.task_display.pack(pady=5)

        # Кнопка генерации
        self.generate_btn = tk.Button(root, text="Сгенерировать задачу", font=("Arial", 12), command=self.generate_task)
        self.generate_btn.pack(pady=10)

        # фильтр по категории
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)

        self.category_var = tk.StringVar(value="все")
        categories = ["все"] + sorted(list({task["category"] for task in PREDEFINED_TASKS}))

        self.category_menu = tk.OptionMenu(filter_frame, self.category_var, *categories,
                                           command=self.filter_history)
        self.category_menu.config(width=10)
        self.category_menu.pack(side=tk.LEFT, padx=5)
        # история задач
        history_frame = tk.Frame(root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.history_label = tk.Label(history_frame, text="История:")
        self.history_label.pack(anchor="w")
        self.history_listbox = tk.Listbox(history_frame, width=50, height=10, font=("Arial", 10))
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
        # добавление новой задачи
        add_frame = tk.Frame(root)
        add_frame.pack(pady=10)
        self.new_task_entry = tk.Entry(add_frame, width=30, font=("Arial", 12))
        self.new_task_entry.pack(side=tk.LEFT, padx=5)
        self.category_new_var = tk.StringVar(value="другое")
        self.category_new_menu = tk.OptionMenu(add_frame, self.category_new_var, "другое", "учёба", "спорт", "работа")
        self.category_new_menu.config(width=10)
        self.category_new_menu.pack(side=tk.LEFT, padx=5)
        self.add_task_btn = tk.Button(add_frame, text="Добавить задачу", font=("Arial", 12), command=self.add_task)
        self.add_task_btn.pack(side=tk.LEFT, padx=5)

    # логика приложения

    def generate_task(self):
        """Генерирует случайную задачу из предопределенного списка."""
        if not PREDEFINED_TASKS:
            messagebox.showwarning("Нет задач", "Список предопределенных задач пуст. Добавьте новые задачи.")
            return
        task = random.choice(PREDEFINED_TASKS)
        # добавляем в историю (копируем словарь, чтобы не было ссылок)
        self.history.append(task.copy())
        # сохраняем историю на диск
        self.save_history()
        # обновляем отображение истории и текущей задачи
        self.update_history_display()
        self.task_display.config(text=task["name"])
    def add_task(self):
        """Добавляет новую задачу в список предопределенных."""
        name = self.new_task_entry.get().strip()
        # проверка на пустую строку (валидация ввода)
        if not name:
            messagebox.showerror("Ошибка ввода", "Поле задачи не может быть пустым.")
            return
        category = self.category_new_var.get()
        # добавляем в список и в историю сразу
        new_task = {"name": name, "category": category}
        PREDEFINED_TASKS.append(new_task.copy())
        # очищаем поле ввода
        self.new_task_entry.delete(0, tk.END)
        # добавляем в историю и сохраняем
        self.history.append(new_task.copy())
        self.save_history()
        # обновляем интерфейс
        self.update_history_display()
    def filter_history(self, value):
        """Фильтрует отображение истории по выбранной категории."""
        self.update_history_display(category=value)
    def update_history_display(self, category=None):
        """Обновляет виджет Listbox с историей задач."""
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            # Если фильтр не задан или категория совпадает с фильтром
            if category is None or category == "все" or task["category"] == category:
                display_text = f"{task['name']} ({task['category']})"
                self.history_listbox.insert(tk.END, display_text)
    def save_history(self):
        """Сохраняет историю задач в файл JSON."""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")
    def load_history(self):
        """Загружает историю задач из файла JSON."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить историю: {e}")
                return []
        return []
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()