import json
from pathlib import Path
from typing import Optional
from creon.core.config import get_file_path, get_current_month_info, DEFAULT_CATEGORIES
from creon.models.finance import FinanceData, Category


class StorageManager:
    def __init__(self):
        self.current_path: Optional[Path] = None

    def get_current_month_data(self) -> FinanceData:
        """
        Загружает данные для текущего месяца.
        Если файла нет, создает новый шаблон с дефолтными категориями.
        """
        month, year = get_current_month_info()
        self.current_path = get_file_path(month, year)

        if self.current_path.exists():
            return self.load_data(self.current_path)
        else:
            # Создаем новый файл с пустыми данными и дефолтными категориями
            new_data = FinanceData(
                month=month,
                year=year,
                total_funds=0.0,
                categories=[
                    Category(name=c["name"], display_name=c["display_name"])
                    for c in DEFAULT_CATEGORIES
                ],
            )
            self.save_data(new_data)
            return new_data

    def load_data(self, path: Path) -> FinanceData:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return FinanceData.from_dict(data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading data: {e}")
            # В случае ошибки возвращаем пустую структуру для текущего месяца
            month, year = get_current_month_info()
            return FinanceData(month=month, year=year)

    def save_data(self, data: FinanceData) -> bool:
        """Сохраняет данные в файл, соответствующий месяцу и году объекта data."""
        path = get_file_path(data.month, data.year)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data.to_dict(), f, indent=4)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False

    def delete_month_data(self, month: str, year: int) -> bool:
        """Удаляет файл конкретного месяца."""
        path = get_file_path(month, year)
        if path.exists():
            path.unlink()
            return True
        return False

    def load_specific_month(self, month: str, year: int) -> FinanceData:
        """Загружает данные для конкретного месяца (для меню Load)."""
        path = get_file_path(month, year)
        if path.exists():
            self.current_path = path
            return self.load_data(path)
        else:
            raise FileNotFoundError(f"No data found for {month} {year}")
