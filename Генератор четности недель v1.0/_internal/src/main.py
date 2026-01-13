#!/usr/bin/env python3
"""
Генератор учебного календаря для университета
Версия: 3.0 (упрощенная, без каникул)
"""

import datetime
from datetime import timedelta
import csv
import os
import sys
import argparse
from typing import List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class AcademicWeek:
    """Учебная неделя"""
    number: int
    start_date: datetime.date
    end_date: datetime.date
    parity: str  # "*" (нечётная) или "**" (чётная)
    is_current: bool = False
    contains_sept_1: bool = False


class UniversityCalendar:
    """Генератор календаря для университета"""
    
    def __init__(self, academic_year: int):
        """
        Инициализация
        
        Args:
            academic_year: Год начала учебного года (напр., 2026)
        """
        self.academic_year = academic_year
        self.weeks: List[AcademicWeek] = []
        self.today = datetime.date.today()
        
    def find_first_academic_week(self) -> Tuple[datetime.date, str]:
        """
        Находит первую учебную неделю по правилам ГОСТ
        
        Returns:
            (дата_начала, примечание)
        """
        sept_1 = datetime.date(self.academic_year, 9, 1)
        
        # День недели 1 сентября
        weekday_names = ["понедельник", "вторник", "среда", 
                        "четверг", "пятница", "суббота", "воскресенье"]
        weekday_name = weekday_names[sept_1.weekday()]
        
        # Определяем начало первой недели
        if sept_1.weekday() == 6:  # Воскресенье
            start_date = sept_1 + timedelta(days=1)  # Понедельник 2 сентября
            note = f"1 сентября - воскресенье, уч. год начинается 2 сентября"
        else:
            start_date = sept_1 - timedelta(days=sept_1.weekday())
            note = f"1 сентября - {weekday_name}"
        
        return start_date, note
    
    def generate(self, total_weeks: int = 52) -> List[AcademicWeek]:
        """
        Генерирует календарь

        Args:
            total_weeks: Общее количество недель

        Returns:
            Список учебных недель
        """
        self.weeks.clear()

        # Определяем первую неделю
        start_date, first_week_note = self.find_first_academic_week()

        # ⭐ ИСПРАВЛЕНИЕ: Определяем правильную четность первой недели
        sept_1 = datetime.date(self.academic_year, 9, 1)

        # Если 1 сентября - воскресенье, то уч. год начинается со 2 сентября
        # и первая неделя должна быть чётной
        if sept_1.weekday() == 6:  # Воскресенье
            first_week_parity = "**"  # Чётная
        else:
            first_week_parity = "*"  # Нечётная

        # Генерируем недели
        current_parity = first_week_parity

        for week_num in range(1, total_weeks + 1):
            end_date = start_date + timedelta(days=6)
            # Используем текущую четность
            parity = current_parity
            # Проверяем, текущая ли это неделя
            is_current = start_date <= self.today <= end_date
            # Проверяем, содержит ли неделя 1 сентября
            contains_sept_1 = start_date <= sept_1 <= end_date
            week = AcademicWeek(
                number=week_num,
                start_date=start_date,
                end_date=end_date,
                parity=parity,
                is_current=is_current,
                contains_sept_1=contains_sept_1
            )

            self.weeks.append(week)
            start_date += timedelta(days=7)

            # Меняем четность для следующей недели
            current_parity = "**" if current_parity == "*" else "*"
    
        return self.weeks
    
    def print_table(self, show_notes: bool = False) -> None:
        """Вывод таблицы в консоль"""
        
        print("\n" + "="*70)
        print(f"УЧЕБНЫЙ КАЛЕНДАРЬ {self.academic_year}-{self.academic_year + 1}")
        print("="*70)
        
        if show_notes:
            print("Легенда: [*] - нечётная неделя, [**] - чётная неделя, [●] - текущая неделя")
            print("-"*70)
        
        # Заголовок
        header = f"{'Неделя':<8} {'Начало':<12} {'Конец':<12} {'Четность':<10}"
        if show_notes:
            header += " Примечание"
        print(header)
        print("-"*70)
        
        # Данные
        for week in self.weeks:
            start_str = week.start_date.strftime("%d.%m.%Y")
            end_str = week.end_date.strftime("%d.%m.%Y")
            
            # Форматируем номер недели с маркером текущей
            week_num_str = f"{week.number}"
            if week.is_current:
                week_num_str = f"{week.number}●"
            
            row = f"{week_num_str:<8} {start_str:<12} {end_str:<12} {week.parity:<10}"
            
            if show_notes:
                notes = []
                if week.contains_sept_1:
                    notes.append("Начало учебного года")
                if week.is_current:
                    notes.append("Текущая")
                notes_str = ", ".join(notes)
                row += f" {notes_str}"
            
            print(row)
    
    def export_csv(self, filename: str = None) -> str:
        """
        Экспорт в CSV
        
        Returns:
            Путь к созданному файлу
        """
        if not filename:
            filename = f"university_calendar_{self.academic_year}_{self.academic_year+1}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            
            # Заголовок
            writer.writerow([
                'Номер недели',
                'Начало недели',
                'Конец недели', 
                'Четность',
                'Текущая неделя',
                'Содержит 1 сентября'
            ])
            
            # Данные
            for week in self.weeks:
                writer.writerow([
                    week.number,
                    week.start_date.strftime("%d.%m.%Y"),
                    week.end_date.strftime("%d.%m.%Y"),
                    week.parity,
                    'Да' if week.is_current else 'Нет',
                    'Да' if week.contains_sept_1 else 'Нет'
                ])
        
        return os.path.abspath(filename)
    
    def get_current_week(self) -> Optional[AcademicWeek]:
        """Получить текущую неделю"""
        for week in self.weeks:
            if week.is_current:
                return week
        return None
    
    def get_statistics(self) -> dict:
        """Статистика по календарю"""
        if not self.weeks:
            return {}
        
        total = len(self.weeks)
        odd = sum(1 for w in self.weeks if w.parity == "*")
        even = total - odd
        current = self.get_current_week()
        
        return {
            'total_weeks': total,
            'odd_weeks': odd,
            'even_weeks': even,
            'start_date': self.weeks[0].start_date,
            'end_date': self.weeks[-1].end_date,
            'current_week': current.number if current else None
        }


def analyze_year(year: int) -> None:
    """Анализ структуры учебного года"""
    
    print(f"\n{'='*60}")
    print(f"АНАЛИЗ УЧЕБНОГО ГОДА {year}-{year+1}")
    print(f"{'='*60}")
    
    sept_1 = datetime.date(year, 9, 1)
    weekdays = ["понедельник", "вторник", "среда", 
                "четверг", "пятница", "суббота", "воскресенье"]
    
    weekday_num = sept_1.weekday()
    weekday_name = weekdays[weekday_num]
    
    print(f"📅 1 сентября {year} года: {weekday_name}")
    
    if weekday_num == 6:  # Воскресенье
        start_date = sept_1 + timedelta(days=1)
        print("⚠️  1 сентября - воскресенье")
        print(f"✅ Учебный год начинается: {start_date.strftime('%d.%m.%Y')}")
        print(f"✅ Первая учебная неделя: {start_date.strftime('%d.%m.%Y')} - "
              f"{(start_date + timedelta(days=6)).strftime('%d.%m.%Y')}")
    else:
        start_date = sept_1 - timedelta(days=weekday_num)
        print(f"✅ Первая учебная неделя: {start_date.strftime('%d.%m.%Y')} - "
              f"{(start_date + timedelta(days=6)).strftime('%d.%m.%Y')}")
    
    # Предыдущие и следующие годы для сравнения
    print(f"\nСравнение с соседними годами:")
    for y in [year-1, year, year+1]:
        s1 = datetime.date(y, 9, 1)
        wd_name = weekdays[s1.weekday()]
        marker = "←" if y == year else ""
        print(f"  {y}-{y+1}: 1 сентября - {wd_name} {marker}")


def validate_year(year: int) -> bool:
    """Проверка корректности года"""
    current_year = datetime.date.today().year
    return 2000 <= year <= current_year + 20


def main():
    """Точка входа в программу"""
    
    parser = argparse.ArgumentParser(
        description='Генератор учебного календаря для университета',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s                    # Текущий учебный год
  %(prog)s -y 2026           # Конкретный год
  %(prog)s -y 2026 -d        # Подробный вывод
  %(prog)s -y 2026 -e        # Экспорт в CSV
  %(prog)s -y 2026 -a        # Анализ года
  %(prog)s -y 2026 -s        # Статистика
        """
    )
    
    parser.add_argument('-y', '--year', type=int,
                       help='Год начала учебного года (напр., 2026)')
    parser.add_argument('-d', '--detailed', action='store_true',
                       help='Подробный вывод с примечаниями')
    parser.add_argument('-e', '--export', action='store_true',
                       help='Экспорт в CSV файл')
    parser.add_argument('-a', '--analyze', action='store_true',
                       help='Анализ структуры учебного года')
    parser.add_argument('-s', '--stats', action='store_true',
                       help='Показать статистику')
    parser.add_argument('-w', '--weeks', type=int, default=52,
                       help='Количество недель (по умолчанию: 52)')
    
    args = parser.parse_args()
    
    # Определяем год
    if args.year:
        if not validate_year(args.year):
            current_year = datetime.date.today().year
            print(f"❌ Год должен быть между 2000 и {current_year + 20}")
            sys.exit(1)
        year = args.year
    else:
        today = datetime.date.today()
        year = today.year if today.month >= 9 else today.year - 1
    
    print(f"\n🎓 УНИВЕРСИТЕТСКИЙ КАЛЕНДАРЬ")
    print(f"{'='*50}")
    
    # Анализ года если запрошен
    if args.analyze:
        analyze_year(year)
        return
    
    # Создаем календарь
    calendar = UniversityCalendar(year)
    calendar.generate(args.weeks)
    
    # Выводим информацию о первой неделе
    first_week = calendar.weeks[0] if calendar.weeks else None
    if first_week:
        print(f"📅 Учебный год: {year}-{year+1}")
        print(f"📍 Первая неделя: {first_week.start_date.strftime('%d.%m.%Y')} - "
              f"{first_week.end_date.strftime('%d.%m.%Y')} ({first_week.parity})")
    
    # Выводим таблицу
    calendar.print_table(show_notes=args.detailed)
    
    # Текущая неделя
    current_week = calendar.get_current_week()
    if current_week:
        print(f"\n📌 ТЕКУЩАЯ НЕДЕЛЯ: №{current_week.number} "
              f"({current_week.parity}) "
              f"{current_week.start_date.strftime('%d.%m.%Y')} - "
              f"{current_week.end_date.strftime('%d.%m.%Y')}")
    
    # Статистика
    if args.stats:
        stats = calendar.get_statistics()
        print(f"\n{'='*50}")
        print(f"СТАТИСТИКА")
        print(f"{'='*50}")
        print(f"Всего недель: {stats['total_weeks']}")
        print(f"Нечётных: {stats['odd_weeks']}")
        print(f"Чётных: {stats['even_weeks']}")
        print(f"Начало: {stats['start_date'].strftime('%d.%m.%Y')}")
        print(f"Окончание: {stats['end_date'].strftime('%d.%m.%Y')}")
        if stats['current_week']:
            print(f"Текущая неделя: №{stats['current_week']}")
    
    # Экспорт
    if args.export:
        filepath = calendar.export_csv()
        print(f"\n💾 Экспортировано в: {filepath}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)