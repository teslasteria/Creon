from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import (
    QPropertyAnimation,
    pyqtProperty,
    QEasingCurve,
    Qt,
)  # <-- Добавь Qt
from PyQt6.QtGui import QFont


class AnimatedLabel(QLabel):
    """Label с анимацией изменения чисел"""

    def __init__(self, initial_value: float = 0.0, parent=None):
        super().__init__(parent)
        self._value = initial_value
        self.setFont(QFont("Roboto", 32, QFont.Weight.Bold))
        self.setStyleSheet("color: #00d9ff;")
        self.update_text()

    @pyqtProperty(float)
    def value(self):
        return self._value

    @value.setter
    def value(self, val: float):
        self._value = val
        self.update_text()

    def update_text(self):
        """Обновляет текст с форматированием валюты"""
        self.setText(f"${self._value:,.2f}")

    def animate_to(self, target_value: float, duration: int = 500):
        """Плавная анимация к целевому значению"""
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(duration)
        self.animation.setStartValue(self._value)
        self.animation.setEndValue(target_value)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.start()

    def set_positive_style(self):
        self.setStyleSheet("color: #00ff88;")

    def set_negative_style(self):
        self.setStyleSheet("color: #ff4757;")

    def set_neutral_style(self):
        self.setStyleSheet("color: #00d9ff;")


class BalanceCard(QFrame):
    """Карточка с балансом"""

    def __init__(self, title: str, initial_value: float = 0.0, parent=None):
        super().__init__(parent)
        self.setObjectName("balance_card")
        self.setFixedSize(250, 150)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Title
        self.title_label = QLabel(title)
        self.title_label.setObjectName("balance_title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Value
        self.value_label = AnimatedLabel(initial_value)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)

        layout.addStretch()

    def update_value(self, new_value: float):
        """Обновляет значение с анимацией"""
        self.value_label.animate_to(new_value)

        # Меняем цвет в зависимости от значения
        if new_value > 0:
            self.value_label.set_positive_style()
        elif new_value < 0:
            self.value_label.set_negative_style()
        else:
            self.value_label.set_neutral_style()
