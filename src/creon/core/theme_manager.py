from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication
from typing import Dict

class ThemeManager:
    """Управление темами приложения (Dark/Light)"""
    
    DARK_THEME = {
        "bg_primary": "#1e293b",
        "bg_secondary": "#334155",
        "bg_table": "#0f172a",
        "text_primary": "#f1f5f9",
        "text_secondary": "#94a3b8",
        "accent": "#3b82f6",
        "accent_dark": "#1e40af",
        "success": "#22c55e",
        "warning": "#eab308",
        "danger": "#ef4444",
        "border": "#475569",
        "hover": "#475569",
        "title": "#f1f5f9"
    }
    
    LIGHT_THEME = {
        # Фон
        "bg_primary": "#FFFFFF",
        "bg_secondary": "#F8FAFC",
        
        # Таблица - чередование строк
        "bg_table": "#F6F2EC",
        "bg_table_alt": "#D6C1A6",
        
        # Текст
        "text_primary": "#1e293b",
        "text_secondary": "#64748b",
        "title": "#1A1A1A",
        
        # Акценты
        "accent": "#3b82f6",
        "accent_dark": "#1e40af",
        "success": "#22c55e",
        "warning": "#eab308",
        "danger": "#ef4444",
        "border": "#e2e8f0",
        "hover": "#e2e8f0",
        
        # Кнопки (Light Mode)
        "btn_add_category": "#22AB74",
        "btn_add_category_hover": "#1A8A5C",
        
        "btn_theme": "#FFDD45",
        "btn_theme_hover": "#E6C43D",
        
        "btn_storage": "#A63040",
        "btn_storage_hover": "#8A2835",
    }
    
    def __init__(self):
        self.current_theme = "dark"
        self.colors = self.DARK_THEME.copy()
    
    def set_theme(self, theme: str):
        """Установка темы"""
        if theme == "light":
            self.current_theme = "light"
            self.colors = self.LIGHT_THEME.copy()
        else:
            self.current_theme = "dark"
            self.colors = self.DARK_THEME.copy()
    
    def get_stylesheet(self) -> str:
        """Получение полного QSS стилей"""
        c = self.colors
        
        return f"""
        /* Global Styles */
        QWidget {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
            font-family: 'Sans Serif';
            font-size: 14px;
        }}
        
        /* Main Window */
        QMainWindow {{
            background-color: {c['bg_primary']};
        }}
        
        /* Header */
        QLabel#appTitle {{
            font-family: 'Sans Serif';
            font-size: 32px;
            font-weight: bold;
            color: {c['title']};
            padding: 10px;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {c['bg_secondary']};
            color: {c['text_primary']};
            padding: 5px;
            border-bottom: 1px solid {c['border']};
        }}
        
        QMenuBar::item {{
            padding: 5px 15px;
            background: transparent;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {c['hover']};
        }}
        
        QMenu {{
            background-color: {c['bg_secondary']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            padding: 5px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {c['hover']};
        }}
        
        /* Buttons - Base Style */
        QPushButton {{
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            min-width: 100px;
            font-size: 13px;
        }}
        
        QPushButton:hover {{
            opacity: 0.9;
        }}
        
        QPushButton:pressed {{
            opacity: 0.8;
        }}
        
        /* Button - Add Category */
        QPushButton#btnAddCategory {{
            background-color: {c.get('btn_add_category', c['success'])};
        }}
        
        QPushButton#btnAddCategory:hover {{
            background-color: {c.get('btn_add_category_hover', c['success'])};
        }}
        
        /* Button - Theme Toggle */
        QPushButton#btnTheme {{
            background-color: {c.get('btn_theme', c['warning'])};
            color: #1e293b;
        }}
        
        QPushButton#btnTheme:hover {{
            background-color: {c.get('btn_theme_hover', c['warning'])};
        }}
        
        /* Button - Storage Path */
        QPushButton#btnStorage {{
            background-color: {c.get('btn_storage', c['danger'])};
        }}
        
        QPushButton#btnStorage:hover {{
            background-color: {c.get('btn_storage_hover', c['danger'])};
        }}
        
        /* Table */
        QTableWidget {{
            background-color: {c['bg_table']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            gridline-color: {c['border']};
            color: {c['text_primary']};
            alternate-background-color: {c.get('bg_table_alt', c['bg_table'])};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {c['accent']};
            color: white;
        }}
        
        QTableWidget::item:hover {{
            background-color: {c['hover']};
        }}
        
        QHeaderView::section {{
            background-color: {c['bg_secondary']};
            color: {c['text_primary']};
            padding: 10px;
            border: 1px solid {c['border']};
            font-weight: bold;
        }}
        
        /* Input Fields */
        QLineEdit {{
            background-color: {c['bg_secondary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px;
            color: {c['text_primary']};
            selection-background-color: {c['accent']};
        }}
        
        QLineEdit:focus {{
            border: 2px solid {c['accent']};
        }}
        
        /* SpinBox for numbers */
        QSpinBox {{
            background-color: {c['bg_secondary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px;
            color: {c['text_primary']};
        }}
        
        QSpinBox:focus {{
            border: 2px solid {c['accent']};
        }}
        
        /* Scrollbar */
        QScrollBar:vertical {{
            background-color: {c['bg_secondary']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {c['border']};
            border-radius: 6px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {c['hover']};
        }}
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {c['bg_secondary']};
            color: {c['text_secondary']};
            border-top: 1px solid {c['border']};
        }}
        
        /* Dialog */
        QMessageBox {{
            background-color: {c['bg_primary']};
        }}
        
        /* Tool Tip */
        QToolTip {{
            background-color: {c['bg_secondary']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            padding: 5px;
        }}
        
        /* Labels */
        QLabel#fundsValue, QLabel#remainingValue {{
            font-weight: bold;
        }}
        """
    
    def toggle_theme(self) -> str:
        """Переключение темы"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme(new_theme)
        return new_theme