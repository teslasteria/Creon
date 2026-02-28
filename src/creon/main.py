"""
Точка входа приложения Creon
"""
import sys
import faulthandler
import traceback
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Включаем отладчик сегментации faults
faulthandler.enable()
# faulthandler.register(signal.SIGSEGV)

from creon.views.main_window import MainWindow
from creon.core.config import config


def exception_hook(exctype, value, tb):
    """Перехват исключений для отладки"""
    print('\n'.join(traceback.format_exception(exctype, value, tb)))
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = exception_hook


def main():
    """Основная функция запуска"""
    
    print("=" * 50)
    print("Creon Finance Tracker - Debug Mode")
    print("=" * 50)
    
    try:
        # Настройка High DPI
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        print("[1/5] Creating QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName("Creon")
        app.setOrganizationName("CreonFinance")
        
        print("[2/5] Loading configuration...")
        print(f"   Storage path: {config.storage_path}")
        print(f"   Theme: {config.theme}")
        
        print("[3/5] Creating MainWindow...")
        window = MainWindow()
        
        print("[4/5] Showing window...")
        window.show()
        
        print("[5/5] Starting event loop...")
        print("=" * 50)
        print("Application running. Press Ctrl+C to exit.")
        print("=" * 50)
        
        exit_code = app.exec()
        
        print(f"Application exited with code: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()