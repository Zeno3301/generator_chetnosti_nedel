#!/usr/bin/env python3
"""
Точка входа для EXE-версии
"""

import sys
import os

# Добавляем папку src в путь
if getattr(sys, 'frozen', False):
    # Если запущено как EXE
    base_path = sys._MEIPASS
else:
    # Если запущено как скрипт
    base_path = os.path.dirname(__file__)

src_path = os.path.join(base_path, 'src')
sys.path.insert(0, src_path)

# Запускаем приложение
from gui_app import main
main()