"""
Тесты для генератора учебного календаря
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from datetime import date
from main import UniversityCalendar


class TestUniversityCalendar(unittest.TestCase):
    
    def test_2026_year(self):
        """Тест для учебного года 2026-2027"""
        cal = UniversityCalendar(2026)
        weeks = cal.generate(4)
        
        # Проверяем первую неделю (должна быть 31.08.2026 - 06.09.2026)
        self.assertEqual(weeks[0].number, 1)
        self.assertEqual(weeks[0].start_date, date(2026, 8, 31))
        self.assertEqual(weeks[0].end_date, date(2026, 9, 6))
        self.assertEqual(weeks[0].parity, "*")  # Первая неделя нечётная
    
    def test_2024_year_sunday(self):
        """Тест для 2024 года (1 сентября - воскресенье)"""
        cal = UniversityCalendar(2024)
        weeks = cal.generate(4)
        
        # Проверяем, что первая неделя начинается 2 сентября
        self.assertEqual(weeks[0].start_date, date(2024, 9, 2))
        self.assertEqual(weeks[0].end_date, date(2024, 9, 8))
    
    def test_parity_alternation(self):
        """Тест чередования четности недель"""
        cal = UniversityCalendar(2025)
        weeks = cal.generate(10)
        
        # Проверяем чередование
        parities = [w.parity for w in weeks]
        expected = ["*", "**", "*", "**", "*", "**", "*", "**", "*", "**"]
        self.assertEqual(parities, expected)
    
    def test_contains_sept_1(self):
        """Тест определения недели с 1 сентября"""
        cal = UniversityCalendar(2025)
        weeks = cal.generate(52)
        
        # Находим неделю, содержащую 1 сентября 2025
        week_with_sept_1 = None
        for week in weeks:
            if week.contains_sept_1:
                week_with_sept_1 = week
                break
        
        self.assertIsNotNone(week_with_sept_1)
        self.assertTrue(date(2025, 9, 1) >= week_with_sept_1.start_date)
        self.assertTrue(date(2025, 9, 1) <= week_with_sept_1.end_date)


if __name__ == '__main__':
    unittest.main()