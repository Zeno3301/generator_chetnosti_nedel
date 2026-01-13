#!/usr/bin/env python3
"""
Точка входа для EXE - специальная версия для PyInstaller
"""

import sys
import os
import traceback

def main():
    """Основная функция"""
    try:
        # Добавляем папку src в путь импорта
        if getattr(sys, 'frozen', False):
            # Если запущено как EXE
            application_path = sys._MEIPASS
        else:
            # Если запущено как скрипт
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        src_path = os.path.join(application_path, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Импортируем и запускаем
        from gui_app import main as gui_main
        gui_main()
        
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        
        # Пауза для просмотра ошибки
        if sys.platform == 'win32':
            os.system('pause')

if __name__ == "__main__":
    main()