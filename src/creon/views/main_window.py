"""
Главное окно приложения Creon
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QMenuBar,
    QMenu, QStatusBar, QFileDialog, QMessageBox,
    QSpinBox, QPushButton, QHeaderView, QFrame
)
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt, QDate

from creon.core.theme_manager import ThemeManager
from creon.core.config import config, DEFAULT_CATEGORIES
from creon.models.finance import MonthData, FinanceStorage
from creon.views.styles import setup_fonts


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        
        # Инициализация
        self.theme_manager = ThemeManager()
        self.theme_manager.set_theme(config.theme)
        
        # Регистрация шрифтов (отключена)
        setup_fonts()
        
        # Хранилище данных
        self.storage = FinanceStorage(config.storage_path)
        
        # Текущие данные месяца
        self.current_data: MonthData = None
        self.has_unsaved_changes = False
        
        # Флаг для блокировки рекурсивных обновлений
        self._updating_table = False
        
        # Настройка UI
        self._setup_ui()
        self._setup_menu()
        self._apply_theme()
        
        # Загрузка текущего месяца
        self._load_current_month()
        
        # Настройка окна
        self.setWindowTitle("Creon - Finance Tracker")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title_label = QLabel("Creon")
        title_label.setObjectName("appTitle")  # ← Убедиться, что есть
        title_label.setFont(QFont("Sans Serif", 32, QFont.Weight.Bold))
        main_layout.addWidget(title_label)
        
        # Панель с балансом
        balance_frame = self._create_balance_panel()
        main_layout.addWidget(balance_frame)
        
        # Таблица категорий - БЕЗ КАСТОМНЫХ ДЕЛЕГАТОВ
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Category", "Planned Budget", "Actual Budget", "Difference"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # Разрешаем редактирование только числовых колонок
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        
        # ⚠️ НЕ используем setItemDelegate - это вызывает segfault!
        
        # Сигналы
        self.table.cellChanged.connect(self._on_cell_changed)
        
        main_layout.addWidget(self.table, stretch=1)
        
        # Кнопки управления
        buttons_layout = self._create_buttons_panel()
        main_layout.addLayout(buttons_layout)
        
        # Статус бар
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
    
    def _create_balance_panel(self) -> QFrame:
        """Создание панели с балансом"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(30)
        
        # Total Funds
        funds_label = QLabel("Total Funds:")
        funds_label.setFont(QFont("Sans Serif", 14, QFont.Weight.Bold))
        
        self.funds_value = QLabel("$0.00")
        self.funds_value.setFont(QFont("Sans Serif", 18, QFont.Weight.Bold))
        self.funds_value.setObjectName("fundsValue")
        
        # Remaining
        remaining_label = QLabel("Remaining After Expenses:")
        remaining_label.setFont(QFont("Sans Serif", 14, QFont.Weight.Bold))
        
        self.remaining_value = QLabel("$0.00")
        self.remaining_value.setFont(QFont("Sans Serif", 18, QFont.Weight.Bold))
        self.remaining_value.setObjectName("remainingValue")
        
        # Input для Total Funds
        self.funds_input = QSpinBox()
        self.funds_input.setRange(0, 10000000)
        self.funds_input.setPrefix("$ ")
        self.funds_input.setFont(QFont("Sans Serif", 14))
        self.funds_input.valueChanged.connect(self._on_funds_changed)
        
        layout.addWidget(funds_label)
        layout.addWidget(self.funds_input)
        layout.addSpacing(50)
        layout.addWidget(remaining_label)
        layout.addWidget(self.remaining_value)
        layout.addStretch()
        
        return frame
    
    def _create_buttons_panel(self) -> QHBoxLayout:
        """Создание панели кнопок"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Add Category
        self.btn_add_category = QPushButton("+ Add Category")
        self.btn_add_category.setObjectName("btnAddCategory")  # ← ДОБАВИТЬ
        self.btn_add_category.clicked.connect(self._add_category)
        layout.addWidget(self.btn_add_category)
        
        # Theme Toggle
        self.btn_theme = QPushButton("🌙 Dark Mode")
        self.btn_theme.setObjectName("btnTheme")  # ← ДОБАВИТЬ
        self.btn_theme.clicked.connect(self._toggle_theme)
        layout.addWidget(self.btn_theme)
        
        # Set Storage Path
        self.btn_storage = QPushButton("📁 Storage Path")
        self.btn_storage.setObjectName("btnStorage")  # ← ДОБАВИТЬ
        self.btn_storage.clicked.connect(self._set_storage_path)
        layout.addWidget(self.btn_storage)
        
        layout.addStretch()
        
        return layout
    
    def _setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        load_action = QAction("Load Data", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self._load_data)
        file_menu.addAction(load_action)
        
        save_action = QAction("Save Data", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_data)
        file_menu.addAction(save_action)
        
        delete_action = QAction("Delete Month", self)
        delete_action.setShortcut("Ctrl+D")
        delete_action.triggered.connect(self._delete_month)
        file_menu.addAction(delete_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings Menu
        settings_menu = menubar.addMenu("Settings")
        
        theme_action = QAction("Toggle Theme", self)
        theme_action.setShortcut("Ctrl+T")
        theme_action.triggered.connect(self._toggle_theme)
        settings_menu.addAction(theme_action)
        
        path_action = QAction("Set Storage Path", self)
        path_action.triggered.connect(self._set_storage_path)
        settings_menu.addAction(path_action)
    
    def _apply_theme(self):
        """Применение текущей темы"""
        try:
            stylesheet = self.theme_manager.get_stylesheet()
            self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"Warning: Error applying theme: {e}")
        
        if self.theme_manager.current_theme == "dark":
            self.btn_theme.setText("🌙 Dark Mode")
        else:
            self.btn_theme.setText("☀️ Light Mode")
    
    def _load_current_month(self):
        """Загрузка данных текущего месяца"""
        today = QDate.currentDate()
        year = today.year()
        month = today.month()
        
        self.current_data = self.storage.load_month(year, month)
        
        if self.current_data is None:
            self.current_data = MonthData(year, month)
            for cat_name in DEFAULT_CATEGORIES:
                self.current_data.add_category(cat_name)
        
        self._refresh_table()
        self._update_balance_display()
        self.statusBar.showMessage(f"Loaded: {self.current_data.month_name}_{year}")
    
    def _refresh_table(self):
        """Обновление таблицы"""
        if not self.current_data:
            return
        
        self._updating_table = True
        self.table.blockSignals(True)
        
        try:
            self.table.setRowCount(len(self.current_data.categories))
            
            for row, category in enumerate(self.current_data.categories):
                # Category Name
                name_item = QTableWidgetItem(category.name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 0, name_item)
                
                # Planned Budget
                planned_item = QTableWidgetItem(f"{category.planned:.2f}")
                planned_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, 1, planned_item)
                
                # Actual Budget
                actual_item = QTableWidgetItem(f"{category.actual:.2f}")
                actual_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, 2, actual_item)
                
                # Difference
                diff = category.difference
                diff_item = QTableWidgetItem(f"{diff:.2f}")
                diff_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                
                # Цвет в зависимости от разницы
                if diff > 0:
                    diff_item.setForeground(Qt.GlobalColor.darkGreen)
                elif diff < 0:
                    diff_item.setForeground(Qt.GlobalColor.red)
                
                self.table.setItem(row, 3, diff_item)
                
                # ← Чередование цветов строк (если нужно программно)
                # QSS делает это автоматически через alternate-background-color
        except Exception as e:
            print(f"Error refreshing table: {e}")
        finally:
            self.table.blockSignals(False)
            self._updating_table = False
    
    def _update_balance_display(self):
        """Обновление отображения баланса"""
        if not self.current_data:
            return
        
        try:
            self.funds_value.setText(f"${self.current_data.total_funds:,.2f}")
            self.remaining_value.setText(f"${self.current_data.remaining:,.2f}")
            
            if self.current_data.remaining >= 0:
                self.remaining_value.setStyleSheet("color: #22c55e;")
            else:
                self.remaining_value.setStyleSheet("color: #ef4444;")
        except Exception as e:
            print(f"Error updating balance: {e}")
    
    def _on_cell_changed(self, row: int, column: int):
        """Обработка изменения ячейки таблицы"""
        if self._updating_table:
            return
        
        if not self.current_data or row >= len(self.current_data.categories):
            return
        
        item = self.table.item(row, column)
        if item is None:
            return
        
        category = self.current_data.categories[row]
        
        try:
            if column == 1:  # Planned
                text = item.text().strip()
                value = float(text) if text else 0.0
                self.current_data.update_category(category.name, planned=value)
            elif column == 2:  # Actual
                text = item.text().strip()
                value = float(text) if text else 0.0
                self.current_data.update_category(category.name, actual=value)
            else:
                return
            
            self.has_unsaved_changes = True
            self._update_balance_display()
            self.statusBar.showMessage("Unsaved changes")
            
        except ValueError as e:
            print(f"Invalid value entered: {e}")
        except Exception as e:
            print(f"Error in cellChanged: {e}")
    
    def _on_funds_changed(self, value: int):
        """Изменение общих средств"""
        if self.current_data:
            self.current_data.total_funds = float(value)
            self.has_unsaved_changes = True
            self._update_balance_display()
            self.statusBar.showMessage("Unsaved changes")
    
    def _add_category(self):
        """Добавление новой категории"""
        if not self.current_data:
            return
        
        base_name = "New Category"
        counter = 1
        name = base_name
        
        existing_names = {cat.name for cat in self.current_data.categories}
        while name in existing_names:
            counter += 1
            name = f"{base_name} {counter}"
        
        self.current_data.add_category(name)
        self.has_unsaved_changes = True
        self._refresh_table()
        self.statusBar.showMessage(f"Added category: {name}")
    
    def _toggle_theme(self):
        """Переключение темы"""
        self.theme_manager.toggle_theme()
        config.theme = self.theme_manager.current_theme
        self._apply_theme()
        self.statusBar.showMessage(f"Theme switched to {self.theme_manager.current_theme}")
    
    def _set_storage_path(self):
        """Установка пути к хранилищу"""
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Storage Directory",
            str(config.storage_path)
        )
        
        if path:
            config.storage_path = path
            self.storage = FinanceStorage(config.storage_path)
            self.statusBar.showMessage(f"Storage path: {path}")
    
    def _load_data(self):
        """Загрузка данных"""
        self._load_current_month()
        self.has_unsaved_changes = False
        self.statusBar.showMessage("Data loaded")
    
    def _save_data(self):
        """Сохранение данных"""
        if self.current_data:
            try:
                self.storage.save_month(self.current_data)
                self.has_unsaved_changes = False
                self.statusBar.showMessage(f"Saved: {self.current_data.filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {e}")
    
    def _delete_month(self):
        """Удаление данных месяца"""
        if not self.current_data:
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Month",
            f"Are you sure you want to delete {self.current_data.filename}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.storage.delete_month(self.current_data.year, self.current_data.month):
                self.statusBar.showMessage("Month deleted")
                self._load_current_month()
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        if self.has_unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Save Changes",
                "You have unsaved changes. Do you want to save them?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self._save_data()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()