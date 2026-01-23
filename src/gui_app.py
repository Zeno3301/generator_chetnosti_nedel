"""
Графический интерфейс для генератора учебного календаря
Версия: 2.5 (компактный интерфейс)
"""

import tkinter as tk
from tkinter import ttk
import datetime
from datetime import timedelta
import csv
import os
import locale


class AcademicCalendarGUI:
    """Главное окно приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("NEFU Генератор четности недель")
        
        # Устанавливаем локаль для русского языка
        try:
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')
            except:
                pass
        
        self.setup_styles()
        
        self.calendar_data = []
        
        # Автоматическое определение текущего учебного года
        self.current_year = self.get_current_academic_year()
        
        self.create_widgets()
        
        # Автоматическая генерация при запуске
        self.auto_generate_on_startup()
        
        # Фиксируем размер окна
        self.root.geometry("750x750")
    
    def get_current_academic_year(self):
        """Определяет текущий учебный год"""
        today = datetime.date.today()
        
        if today.month >= 9:  # Сентябрь-Декабрь
            return today.year
        else:  # Январь-Август
            return today.year - 1
    
    def auto_generate_on_startup(self):
        """Автоматически генерирует календарь при запуске программы"""
        self.year_var.set(str(self.current_year))
        self.generate_calendar()
    
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.accent_color = "#1e3a8a"
        self.today_bg = "#e6f0ff"
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ВЕРХНЯЯ ПАНЕЛЬ - ЗАГОЛОВОК
        header_frame = tk.Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            header_frame,
            text="ГЕНЕРАТОР ЧЕТНОСТИ НЕДЕЛЬ",
            font=("Arial", 18, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Северо-Восточный федеральный университет",
            font=("Arial", 10),
            fg="#64748b",
            bg=self.bg_color
        )
        subtitle_label.pack()
        
        # ОСНОВНОЙ КОНТЕНТ (две колонки)
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # ЛЕВАЯ КОЛОНКА - основные элементы
        left_frame = tk.Frame(content_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # ПАНЕЛЬ УПРАВЛЕНИЯ ГЕНЕРАЦИЕЙ
        control_frame = tk.LabelFrame(
            left_frame,
            text="УЧЕБНЫЙ ГОД",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            padx=12,
            pady=12
        )
        control_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Год
        year_label = tk.Label(
            control_frame,
            text="Учебный год:",
            font=("Arial", 10),
            bg=self.bg_color
        )
        year_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 8))
        
        self.year_var = tk.StringVar(value=str(self.current_year))
        year_spinbox = tk.Spinbox(
            control_frame, 
            from_=2000, 
            to=2100, 
            textvariable=self.year_var,
            width=12,
            font=("Arial", 10),
            justify=tk.CENTER,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        year_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Количество недель
        weeks_label = tk.Label(
            control_frame,
            text="Кол-во недель:",
            font=("Arial", 10),
            bg=self.bg_color
        )
        weeks_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 8))
        
        self.weeks_var = tk.StringVar(value="52")
        weeks_spinbox = tk.Spinbox(
            control_frame, 
            from_=1, 
            to=100, 
            textvariable=self.weeks_var,
            width=8,
            font=("Arial", 10),
            justify=tk.CENTER,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        weeks_spinbox.grid(row=0, column=3, sticky=tk.W)
        
        # Кнопка генерации
        generate_btn = tk.Button(
            control_frame,
            text="СГЕНЕРИРОВАТЬ",
            command=self.generate_calendar,
            width=15,
            font=("Arial", 10, "bold"),
            bg=self.accent_color,
            fg="white",
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            activebackground="#2563eb",
            activeforeground="white"
        )
        generate_btn.grid(row=0, column=4, padx=(20, 0))
        
        # БОЛЬШОЙ ОТОБРАЖАТЕЛЬ ТЕКУЩЕЙ НЕДЕЛИ (компактный)
        today_display_frame = tk.Frame(left_frame, bg=self.today_bg, relief=tk.RIDGE, borderwidth=2)
        today_display_frame.pack(fill=tk.X, pady=(0, 12))
        
        today_title_label = tk.Label(
            today_display_frame,
            text="СЕГОДНЯ",
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            pady=6
        )
        today_title_label.pack(fill=tk.X)
        
        self.today_info_text = tk.StringVar(value="Загрузка...")
        today_label = tk.Label(
            today_display_frame,
            textvariable=self.today_info_text,
            font=("Arial", 20, "bold"),
            bg=self.today_bg,
            fg=self.accent_color,
            pady=15
        )
        today_label.pack(fill=tk.X)
        
        # ИНФОРМАЦИЯ О ГОДЕ (компактная)
        year_info_frame = tk.Frame(left_frame, bg="#f8fafc", relief=tk.SUNKEN, borderwidth=1)
        year_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = tk.StringVar(value="Выберите год и нажмите 'СГЕНЕРИРОВАТЬ'")
        info_label = tk.Label(
            year_info_frame,
            textvariable=self.info_text,
            wraplength=500,
            font=("Arial", 9),
            bg="#f8fafc",
            fg="#1e293b",
            justify=tk.LEFT,
            padx=8,
            pady=8
        )
        info_label.pack(fill=tk.X)
        
        # ТАБЛИЦА С НЕДЕЛЯМИ (компактная)
        table_label = tk.Label(
            left_frame,
            text="СГЕНЕРИРОВАННЫЙ КАЛЕНДАРЬ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        table_label.pack(anchor=tk.W, pady=(0, 5))
        
        table_frame = tk.Frame(left_frame, bg=self.bg_color)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_table(table_frame)
        
        # ПРАВАЯ КОЛОНКА - кнопки действий (вертикально)
        right_frame = tk.Frame(content_frame, bg=self.bg_color, width=180)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)  # Фиксируем ширину
        
        # Кнопки действий (вертикальный стек)
        buttons_frame = tk.Frame(right_frame, bg=self.bg_color)
        buttons_frame.pack(fill=tk.Y, expand=True, pady=(10, 0))
        
        # Кнопка экспорта
        export_btn = tk.Button(
            buttons_frame,
            text="ЭКСПОРТ В CSV",
            command=self.export_to_csv,
            width=18,
            height=2,
            bg="#10b981",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            activebackground="#34d399",
            activeforeground="white"
        )
        export_btn.pack(pady=(0, 10))
        
        # Кнопка очистки
        clear_btn = tk.Button(
            buttons_frame,
            text="ОЧИСТИТЬ",
            command=self.clear_output,
            width=18,
            height=2,
            bg="#ef4444",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            activebackground="#f87171",
            activeforeground="white"
        )
        clear_btn.pack(pady=(0, 10))
        
        # Кнопка "О программе"
        about_btn = tk.Button(
            buttons_frame,
            text="О ПРОГРАММЕ",
            command=self.show_about_info,
            width=18,
            height=2,
            bg="#8b5cf6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2",
            activebackground="#a78bfa",
            activeforeground="white"
        )
        about_btn.pack()
        
        # Заполнитель для выравнивания
        spacer_frame = tk.Frame(buttons_frame, bg=self.bg_color, height=20)
        spacer_frame.pack(fill=tk.Y, expand=True)
        
        # СТАТУС БАР внизу окна
        status_frame = tk.Frame(self.root, bg="#1e293b", height=22)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg="#1e293b",
            fg="white",
            font=("Arial", 9),
            anchor=tk.W,
            padx=10
        )
        status_bar.pack(fill=tk.X)
    
    def create_table(self, parent):
        """Создание компактной таблицы для отображения календаря"""
        
        style = ttk.Style()
        style.configure("Treeview.Heading", 
                       font=("Arial", 9, "bold"),
                       background=self.accent_color,
                       foreground="white")
        style.configure("Treeview", 
                       font=("Arial", 9),
                       rowheight=22,
                       background="white",
                       fieldbackground="white")
        
        columns = ("week", "start", "end", "parity")
        
        self.tree = ttk.Treeview(
            parent, 
            columns=columns, 
            show="headings",
            height=10,  # Уменьшили высоту
            style="Treeview"
        )
        
        self.tree.heading("week", text="№ недели")
        self.tree.heading("start", text="Начало недели")
        self.tree.heading("end", text="Конец недели")
        self.tree.heading("parity", text="Четность")
        
        self.tree.column("week", width=70, anchor=tk.CENTER, minwidth=70)
        self.tree.column("start", width=100, anchor=tk.CENTER, minwidth=100)
        self.tree.column("end", width=100, anchor=tk.CENTER, minwidth=100)
        self.tree.column("parity", width=80, anchor=tk.CENTER, minwidth=80)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def analyze_year_structure(self, year):
        """Анализирует структуру учебного года и возвращает детали"""
        sept_1 = datetime.date(year, 9, 1)
        weekdays = ["понедельник", "вторник", "среда", 
                   "четверг", "пятница", "суббота", "воскресенье"]
        
        if sept_1.weekday() == 6:  # Воскресенье
            first_monday = sept_1 + timedelta(days=1)
            start_date = first_monday
            week_type = "special"
            first_week_parity = "ЧЁТНАЯ"
        else:
            first_monday = sept_1 - timedelta(days=sept_1.weekday())
            start_date = first_monday
            week_type = "normal"
            first_week_parity = "НЕЧЁТНАЯ"
        
        return {
            'year': year,
            'sept_1': sept_1,
            'sept_1_weekday_name': weekdays[sept_1.weekday()],
            'start_date': start_date,
            'week_type': week_type,
            'first_week_parity': first_week_parity
        }
    
    def generate_academic_calendar(self, start_year, total_weeks=52):
        """Генерирует учебный календарь с правильной четностью"""
        weeks = []
        
        try:
            start_year = int(start_year)
            sept_1 = datetime.date(start_year, 9, 1)
            
            if sept_1.weekday() == 6:  # Воскресенье
                first_monday = sept_1 + timedelta(days=1)
                current_date = first_monday
                current_parity = "чётная"
            else:
                first_monday = sept_1 - timedelta(days=sept_1.weekday())
                current_date = first_monday
                current_parity = "нечётная"
            
            for week_num in range(1, total_weeks + 1):
                start_week = current_date
                end_week = current_date + timedelta(days=6)
                
                parity = current_parity
                
                today = datetime.date.today()
                is_current = start_week <= today <= end_week
                contains_sept_1 = start_week <= sept_1 <= end_week
                
                weeks.append({
                    'week_num': week_num,
                    'start_date': start_week,
                    'end_date': end_week,
                    'parity': parity,
                    'is_current': is_current,
                    'contains_sept_1': contains_sept_1
                })
                
                current_date += timedelta(days=7)
                
                # Меняем четность для следующей недели
                current_parity = "чётная" if current_parity == "нечётная" else "нечётная"
                
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка генерации календаря:\n{str(e)}")
            
        return weeks
    
    def generate_calendar(self):
        """Обработчик кнопки генерации"""
        try:
            year = int(self.year_var.get())
            weeks_count = int(self.weeks_var.get())
            
            self.status_var.set("Генерация календаря...")
            self.root.update()
            
            self.calendar_data = self.generate_academic_calendar(year, weeks_count)
            
            self.update_year_info(year)
            self.update_today_info()
            
            # Очищаем таблицу
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Заполняем таблицу
            for week in self.calendar_data:
                tags = ()
                if week['is_current']:
                    tags = ('current',)
                
                self.tree.insert("", tk.END,
                    values=(
                        week['week_num'],
                        week['start_date'].strftime("%d.%m.%Y"),
                        week['end_date'].strftime("%d.%m.%Y"),
                        week['parity'].upper()
                    ),
                    tags=tags
                )
            
            # Настраиваем теги для выделения
            self.tree.tag_configure('current', background='#ffeb3b')
            
            # Статистика
            odd_weeks = sum(1 for w in self.calendar_data if w['parity'] == "нечётная")
            even_weeks = len(self.calendar_data) - odd_weeks
            
            self.status_var.set(
                f"✓ Сгенерировано {len(self.calendar_data)} недель "
                f"({odd_weeks} нечётных, {even_weeks} чётных)"
            )
            
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")
            self.status_var.set("Ошибка ввода данных")
    
    def update_year_info(self, year):
        """Обновляет информацию о выбранном годе"""
        analysis = self.analyze_year_structure(year)
        
        info = (f"📅 Учебный год {year}-{year+1}")
        
        if analysis['week_type'] == 'special':
            info += " | ⚠️ Особый год: 1 сентября - воскресенье"
        
        self.info_text.set(info)
    
    def update_today_info(self):
        """Обновляет информацию о сегодняшнем дне"""
        today = datetime.date.today()
        
        # Форматируем дату на русском языке
        try:
            # Пробуем получить русское название месяца
            month_names = ["января", "февраля", "марта", "апреля", "мая", "июня",
                          "июля", "августа", "сентября", "октября", "ноября", "декабря"]
            today_str = f"{today.day} {month_names[today.month - 1]} {today.year} года"
        except:
            # Если не получилось, используем числовой формат
            today_str = today.strftime("%d.%m.%Y")
        
        current_week = None
        week_num = None
        parity = None
        
        if self.calendar_data:
            for week in self.calendar_data:
                if week['start_date'] <= today <= week['end_date']:
                    current_week = week
                    week_num = week['week_num']
                    parity = week['parity']
                    break
        
        if current_week:
            parity_display = "ЧЁТНАЯ" if parity == "чётная" else "НЕЧЁТНАЯ"
            self.today_info_text.set(f"{today_str}\nНеделя {week_num}\n{parity_display}")
        else:
            if self.calendar_data:
                self.today_info_text.set(f"{today_str}\n\n(дата вне диапазона календаря)")
            else:
                self.today_info_text.set(f"{today_str}\n\nСгенерируйте календарь")
    
    def show_about_info(self):
        """Показывает информацию о программе"""
        
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("450x350")
        about_window.resizable(False, False)
        about_window.configure(bg="#f8fafc")
        
        about_window.transient(self.root)
        about_window.grab_set()
        
        header_frame = tk.Frame(about_window, bg="#1e3a8a")
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="NEFU Academic Calendar Generator",
            font=("Arial", 12, "bold"),
            bg="#1e3a8a",
            fg="white",
            pady=10
        )
        title_label.pack()
        
        content_frame = tk.Frame(about_window, bg="#f8fafc", padx=20, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = """Версия: 1.1.0

Назначение:
Генерация четности недель учебного года
Отображение четности сегодняшнего дня

Особенности:
• Автоматическое определение учебного года
• Генерация календаря с правильной четностью
• Экспорт в CSV для Excel
• Компактный интерфейс

Контакты:
dev: Zeno
GitHub: https://github.com/Zeno3301/Academic-calendar
Email: aa.rozhin@svfu.ru
Якутск 2025 г.
"""
        
        text_widget = tk.Text(
            content_frame,
            wrap=tk.WORD,
            font=("Arial", 9),
            bg="white",
            fg="#1e293b",
            relief=tk.FLAT,
            borderwidth=1,
            height=12,
            padx=10,
            pady=10
        )
        text_widget.insert(tk.INSERT, info_text)
        text_widget.configure(state='disabled')
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        close_frame = tk.Frame(about_window, bg="#f8fafc")
        close_frame.pack(fill=tk.X, pady=10)
        
        close_btn = tk.Button(
            close_frame,
            text="Закрыть",
            command=about_window.destroy,
            width=10,
            bg="#64748b",
            fg="white",
            font=("Arial", 9),
            relief=tk.RAISED,
            cursor="hand2"
        )
        close_btn.pack()
        
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenwidth() // 2) - (height // 2)
        about_window.geometry(f'{width}x{height}+{x}+{y}')
    
    def export_to_csv(self):
        """Экспорт календаря в CSV файл"""
        if not self.calendar_data:
            tk.messagebox.showwarning("Нет данных", "Сначала сгенерируйте календарь")
            return
        
        try:
            year = int(self.year_var.get())
            next_year = year + 1
            
            # Простой диалог сохранения
            filename = tk.filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV файлы", "*.csv")],
                initialfile=f"четность_недель_{year}_{next_year}.csv",
                title="Сохранить календарь"
            )
            
            if not filename:
                return
            
            # Простое сохранение файла
            with open(filename, 'w', encoding='utf-8') as f:
                # Заголовок
                f.write(f"Учебный календарь четности недель НЕФУ\n")
                f.write(f"Год: {year}-{next_year}\n")
                f.write(f"Дата экспорта: {datetime.date.today().strftime('%d.%m.%Y')}\n\n")
                
                # Данные
                f.write("Номер недели;Начало недели;Конец недели;Четность\n")
                
                for week in self.calendar_data:
                    parity = "НЕЧЁТНАЯ" if week['parity'] == "нечётная" else "ЧЁТНАЯ"
                    f.write(f"{week['week_num']};"
                           f"{week['start_date'].strftime('%d.%m.%Y')};"
                           f"{week['end_date'].strftime('%d.%m.%Y')};"
                           f"{parity}\n")
            
            file_basename = os.path.basename(filename)
            self.status_var.set(f"✓ Экспортировано: {file_basename}")
            
            # Упрощенное сообщение
            tk.messagebox.showinfo(
                "Экспорт завершен",
                f"Календарь экспортирован в файл:\n{file_basename}"
            )
            
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Некорректное значение года")
            self.status_var.set("Ошибка: некорректный год")
        except Exception as e:
            tk.messagebox.showerror("Ошибка экспорта", f"Не удалось сохранить файл")
            self.status_var.set("Ошибка экспорта")
    
    def clear_output(self):
        """Очистка результатов"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.calendar_data = []
        
        self.info_text.set("Сгенерируйте календарь")
        self.today_info_text.set("Очищено\n\nСгенерируйте календарь")
        self.status_var.set("Очищено")


def main():
    """Запуск GUI приложения"""
    root = tk.Tk()
    
    # Устанавливаем размер окна
    root.geometry("900x550")
    root.minsize(850, 500)
    
    # Пробуем установить иконку
    try:
        # Для Windows
        root.iconbitmap(default='icon.ico')
    except:
        try:
            # Для других систем или если нет файла
            pass
        except:
            pass
    
    app = AcademicCalendarGUI(root)
    
    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()