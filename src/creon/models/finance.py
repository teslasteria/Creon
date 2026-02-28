"""
Модели данных для финансового учёта
"""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json


class Category:
    """Категория расходов"""

    def __init__(self, name: str, planned: float = 0.0, actual: float = 0.0):
        self.name = name
        self.planned = planned
        self.actual = actual

    def to_dict(self) -> Dict:
        return {"name": self.name, "planned": self.planned, "actual": self.actual}

    @classmethod
    def from_dict(cls, data: Dict) -> "Category":
        return cls(
            name=data.get("name", "Unknown"),
            planned=float(data.get("planned", 0)),
            actual=float(data.get("actual", 0)),
        )

    @property
    def difference(self) -> float:
        """Разница между планируемым и фактическим"""
        return self.planned - self.actual


class MonthData:
    """Данные за месяц"""

    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month
        self.categories: List[Category] = []
        self.total_funds: float = 0.0
        self.created_at: str = datetime.now().isoformat()
        self.updated_at: str = datetime.now().isoformat()

    @property
    def month_name(self) -> str:
        """Название месяца на английском"""
        months = [
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
        ]
        return months[self.month - 1]

    @property
    def filename(self) -> str:
        """Имя файла для сохранения"""
        return f"{self.month_name}_{self.year}.json"

    @property
    def total_planned(self) -> float:
        """Общий планируемый бюджет"""
        return sum(cat.planned for cat in self.categories)

    @property
    def total_actual(self) -> float:
        """Общий фактический бюджет"""
        return sum(cat.actual for cat in self.categories)

    @property
    def remaining(self) -> float:
        """Остаток средств после всех трат"""
        return self.total_funds - self.total_actual

    def add_category(self, name: str, planned: float = 0.0, actual: float = 0.0):
        """Добавление категории"""
        self.categories.append(Category(name, planned, actual))
        self.updated_at = datetime.now().isoformat()

    def remove_category(self, name: str):
        """Удаление категории"""
        self.categories = [c for c in self.categories if c.name != name]
        self.updated_at = datetime.now().isoformat()

    def update_category(
        self, name: str, planned: Optional[float] = None, actual: Optional[float] = None
    ):
        """Обновление категории"""
        for cat in self.categories:
            if cat.name == name:
                if planned is not None:
                    cat.planned = planned
                if actual is not None:
                    cat.actual = actual
                break
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "year": self.year,
            "month": self.month,
            "total_funds": self.total_funds,
            "categories": [cat.to_dict() for cat in self.categories],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "MonthData":
        instance = cls(data.get("year", 2024), data.get("month", 1))
        instance.total_funds = float(data.get("total_funds", 0))
        instance.categories = [
            Category.from_dict(cat) for cat in data.get("categories", [])
        ]
        instance.created_at = data.get("created_at", datetime.now().isoformat())
        instance.updated_at = data.get("updated_at", datetime.now().isoformat())
        return instance


class FinanceStorage:
    """Управление хранением финансовых данных"""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def get_file_path(self, year: int, month: int) -> Path:
        """Получение пути к файлу месяца"""
        month_names = [
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
        ]
        filename = f"{month_names[month - 1]}_{year}.json"
        return self.storage_path / filename

    def save_month(self, data: MonthData):
        """Сохранение данных месяца"""
        file_path = self.get_file_path(data.year, data.month)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data.to_dict(), f, indent=2, ensure_ascii=False)

    def load_month(self, year: int, month: int) -> Optional[MonthData]:
        """Загрузка данных месяца"""
        file_path = self.get_file_path(year, month)
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return MonthData.from_dict(data)

    def delete_month(self, year: int, month: int) -> bool:
        """Удаление файла месяца"""
        file_path = self.get_file_path(year, month)
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def list_months(self) -> List[str]:
        """Список доступных месяцев"""
        files = list(self.storage_path.glob("*.json"))
        return [f.stem for f in files]
