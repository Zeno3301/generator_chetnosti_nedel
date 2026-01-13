@echo off
chcp 65001 >nul
echo ========================================
echo    СБОРКА EXE (без автоматического запуска)
echo ========================================
echo.

echo 1. Очистка старых файлов...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del *.spec 2>nul
echo [OK] Очистка завершена

echo.
echo 2. Проверка зависимостей...
python --version >nul
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    pause
    exit /b 1
)

REM Исправляем проверку tkinter (без Unicode символов)
python -c "import tkinter; print('tkinter доступен')" >nul
if errorlevel 1 (
    echo [ОШИБКА] tkinter не найден!
    pause
    exit /b 1
)
echo [OK] tkinter доступен

echo.
echo 3. Проверка исходного кода...
if not exist run_gui.py (
    echo [ОШИБКА] run_gui.py не найден!
    pause
    exit /b 1
)
if not exist src\gui_app.py (
    echo [ОШИБКА] gui_app.py не найден!
    pause
    exit /b 1
)
echo [OK] Исходный код найден

echo.
echo 4. Сборка EXE (с полным tkinter)...
echo    Пожалуйста, подождите...
echo.

set "APP_NAME=Генератор четности недель"

REM Сборка с полным tkinter
pyinstaller --clean ^
            --windowed ^
            --noconsole ^
            --name "%APP_NAME%" ^
            --add-data "src;src" ^
            --collect-all tkinter ^
            run_gui.py

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Сборка не удалась!
    echo.
    echo Возможные причины:
    echo 1. Антивирус блокирует PyInstaller
    echo 2. Недостаточно места на диске
    echo 3. Ошибка в коде Python
    pause
    exit /b 1
)

echo.
echo [OK] Сборка завершена успешно!
echo.

REM 5. Проверяем результат (БЕЗ запуска!)
set "EXE_PATH=dist\%APP_NAME%\%APP_NAME%.exe"

if exist "%EXE_PATH%" (
    echo [OK] EXE файл создан:
    echo    %EXE_PATH%
    echo.
    
    for %%I in ("%EXE_PATH%") do (
        set /a size_kb=%%~zI / 1024
        set /a size_mb=size_kb / 1024
        echo Информация:
        echo    Размер: %%size_kb%% KB (%%size_mb%% MB)
        echo    Дата: %%~tI
    )
    
    echo.
    echo Содержимое папки:
    dir "dist\%APP_NAME%" /B
    
    echo.
    echo ВНИМАНИЕ: Проверьте антивирус!
    echo    Если EXE не запускается - добавьте папку в исключения.
    
) else (
    echo [ОШИБКА] EXE файл не найден!
    echo.
    echo Проверьте папку dist:
    dir dist /B /S
)

echo.
echo 6. Создаю полезные скрипты...
echo.

REM Создаем run_app.bat для удобного запуска из корня
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo echo Запуск %APP_NAME%...
    echo echo.
    echo "%%~dp0dist\%APP_NAME%\%APP_NAME%.exe"
) > "run_app.bat"

echo [OK] Создан run_app.bat - запускает программу из этой папки

REM Создаем run_debug.bat в папке с EXE
if exist "dist\%APP_NAME%" (
    (
        echo @echo off
        echo chcp 65001 ^>nul
        echo echo ========================================
        echo echo    %APP_NAME%
        echo echo ========================================
        echo echo.
        echo echo Папка: %%~dp0
        echo echo Дата: %%date%% %%time%%
        echo echo.
        echo echo Нажмите любую клавишу для запуска...
        echo pause ^>nul
        echo echo.
        echo echo ЗАПУСКАЮ ПРОГРАММУ...
        echo echo.
        echo "%%~dp0%APP_NAME%.exe"
        echo echo.
        echo echo Программа завершилась. Код: %%ERRORLEVEL%%
        echo pause
    ) > "dist\%APP_NAME%\run_debug.bat"
    
    echo [OK] Создан run_debug.bat в папке с EXE
)

echo.
echo ========================================
echo    ИНСТРУКЦИЯ ПО ТЕСТИРОВАНИЮ
echo ========================================
echo.
echo Теперь программа НЕ запустится автоматически!
echo.
echo Чтобы протестировать:
echo.
echo Способ 1: Запустите run_app.bat (из этой папки)
echo Способ 2: Перейдите в папку и запустите вручную:
echo           cd "dist\%APP_NAME%"
echo           "%APP_NAME%.exe"
echo Способ 3: Используйте run_debug.bat для отладки:
echo           cd "dist\%APP_NAME%"
echo           run_debug.bat
echo.
echo Проверьте все функции:
echo - Экспорт в CSV
echo - Информация о неделях (двойной клик)
echo - Информация о годе
echo.
pause