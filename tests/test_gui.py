"""
Тесты графического интерфейса Creon
"""

import pytest
from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt, QDate
import sys
from pathlib import Path

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from creon.views.main_window import MainWindow
from creon.core.theme_manager import ThemeManager
from creon.models.finance import MonthData, Category


@pytest.fixture
def app(qtbot):
    """Фикстура для создания приложения"""
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def main_window(qtbot, app):
    """Фикстура для создания главного окна"""
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


class TestAppLaunch:
    """Тесты запуска приложения"""

    def test_app_launch(self, main_window):
        """Проверка запуска приложения"""
        assert main_window is not None
        assert main_window.isVisible()
        assert main_window.windowTitle() == "Creon - Finance Tracker"

    def test_table_initialized(self, main_window):
        """Проверка инициализации таблицы"""
        assert main_window.table is not None
        assert main_window.table.columnCount() == 4
        assert main_window.table.rowCount() > 0  # Есть категории по умолчанию


class TestThemeToggle:
    """Тесты переключения тем"""

    def test_theme_toggle(self, qtbot, main_window):
        """Проверка переключения темы"""
        initial_theme = main_window.theme_manager.current_theme

        # Кликаем кнопку смены темы
        qtbot.mouseClick(main_window.btn_theme, Qt.MouseButton.LeftButton)

        # Проверяем, что тема изменилась
        new_theme = main_window.theme_manager.current_theme
        assert new_theme != initial_theme

    def test_theme_persistence(self, main_window):
        """Проверка сохранения темы"""
        from creon.core.config import config

        # Тема должна сохраняться в конфиге
        assert config.theme == main_window.theme_manager.current_theme


class TestCloseEvent:
    """Тесты события закрытия"""

    def test_close_with_unsaved_changes(self, qtbot, main_window, monkeypatch):
        """Проверка диалога при закрытии с несохранёнными изменениями"""
        # Устанавливаем флаг несохранённых изменений
        main_window.has_unsaved_changes = True

        # Эмулируем ответ "Cancel" на диалог
        def mock_question(*args, **kwargs):
            return QMessageBox.StandardButton.Cancel

        monkeypatch.setattr(QMessageBox, "question", mock_question)

        # Пытаемся закрыть окно
        from PyQt6.QtGui import QCloseEvent

        event = QCloseEvent()
        main_window.closeEvent(event)

        # Окно не должно закрыться
        assert event.isAccepted() == False

    def test_close_with_save(self, qtbot, main_window, monkeypatch, tmp_path):
        """Проверка сохранения при закрытии"""
        main_window.has_unsaved_changes = True

        # Эмулируем ответ "Save"
        def mock_question(*args, **kwargs):
            return QMessageBox.StandardButton.Save

        monkeypatch.setattr(QMessageBox, "question", mock_question)

        # Меняем путь сохранения на временный
        main_window.storage.storage_path = tmp_path

        # Закрываем окно
        from PyQt6.QtGui import QCloseEvent

        event = QCloseEvent()
        main_window.closeEvent(event)

        # Проверяем, что файл создан
        assert event.isAccepted() == True


class TestDataOperations:
    """Тесты операций с данными"""

    def test_add_category(self, qtbot, main_window):
        """Проверка добавления категории"""
        initial_count = main_window.table.rowCount()

        # Кликаем кнопку добавления
        qtbot.mouseClick(main_window.btn_add_category, Qt.MouseButton.LeftButton)

        # Проверяем, что строка добавлена
        assert main_window.table.rowCount() == initial_count + 1

    def test_balance_calculation(self, main_window):
        """Проверка расчёта баланса"""
        if main_window.current_data:
            # Устанавливаем тестовые значения
            main_window.current_data.total_funds = 1000.0
            main_window.current_data.categories[0].actual = 100.0

            main_window._update_balance_display()

            # Проверяем, что остаток рассчитан верно
            expected_remaining = 900.0
            assert main_window.current_data.remaining == expected_remaining

    def test_storage_path_change(self, qtbot, main_window, tmp_path, monkeypatch):
        """Проверка изменения пути хранения"""

        # Эмулируем выбор директории
        def mock_getExistingDirectory(*args, **kwargs):
            return str(tmp_path)

        monkeypatch.setattr(
            "PyQt6.QtWidgets.QFileDialog.getExistingDirectory",
            mock_getExistingDirectory,
        )

        # Кликаем кнопку выбора пути
        qtbot.mouseClick(main_window.btn_storage, Qt.MouseButton.LeftButton)

        # Проверяем, что путь изменился
        assert main_window.storage.storage_path == tmp_path


class TestMonthData:
    """Тесты моделей данных"""

    def test_month_data_creation(self):
        """Проверка создания данных месяца"""
        data = MonthData(2024, 10)
        assert data.year == 2024
        assert data.month == 10
        assert data.month_name == "october"
        assert data.filename == "october_2024.json"

    def test_category_operations(self):
        """Проверка операций с категориями"""
        data = MonthData(2024, 10)
        data.add_category("Test", 100.0, 50.0)

        assert len(data.categories) == 1
        assert data.categories[0].name == "Test"
        assert data.categories[0].difference == 50.0

    def test_month_serialization(self):
        """Проверка сериализации месяца"""
        data = MonthData(2024, 10)
        data.total_funds = 1000.0
        data.add_category("Rent", 500.0, 450.0)

        # Сериализация
        data_dict = data.to_dict()

        # Десериализация
        restored = MonthData.from_dict(data_dict)

        assert restored.year == data.year
        assert restored.month == data.month
        assert restored.total_funds == data.total_funds
        assert len(restored.categories) == len(data.categories)
