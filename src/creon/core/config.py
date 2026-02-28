"""
Конфигурация приложения Creon
"""

from pathlib import Path
from typing import Dict, List
import json

# Базовые категории расходов
DEFAULT_CATEGORIES: List[str] = [
    "Rent",
    "Utilities",
    "Groceries",
    "Transport",
    "Entertainment",
    "Health",
    "Education",
    "Savings",
    "Personal Care",
    "Subscriptions",
    "Other",
]

# Пути
BASE_DIR = Path(__file__).parent.parent.parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
FONTS_DIR = RESOURCES_DIR / "fonts"

# Настройки по умолчанию
DEFAULT_CONFIG: Dict = {
    "storage_path": str(BASE_DIR / "data"),
    "theme": "dark",
    "language": "en",
}


class Config:
    """Управление конфигурацией приложения"""

    def __init__(self):
        self.config_file = BASE_DIR / "creon_config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Загрузка конфигурации из файла"""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        """Сохранение конфигурации в файл"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None):
        """Получение значения конфигурации"""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """Установка значения конфигурации"""
        self.config[key] = value
        self.save_config()

    @property
    def storage_path(self) -> Path:
        """Путь к хранилищу данных"""
        return Path(self.config.get("storage_path", str(BASE_DIR / "data")))

    @storage_path.setter
    def storage_path(self, path: Path):
        self.config["storage_path"] = str(path)
        self.save_config()

    @property
    def theme(self) -> str:
        """Текущая тема"""
        return self.config.get("theme", "dark")

    @theme.setter
    def theme(self, theme: str):
        self.config["theme"] = theme
        self.save_config()


# Глобальный экземпляр конфигурации
config = Config()
