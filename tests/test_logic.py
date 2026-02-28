# test_logic.py
from creon.core.storage import StorageManager
from creon.core.config import DATA_DIR

print(f"Data will be stored in: {DATA_DIR}")

manager = StorageManager()
data = manager.get_current_month_data()

print(f"Loaded month: {data.month} {data.year}")
print(f"Categories count: {len(data.categories)}")
print(f"Initial Remaining: {data.calculate_remaining()}")

# Тест изменения
data.total_funds = 1000.0
data.categories[0].actual = 200.0  # Rent
print(f"New Remaining: {data.calculate_remaining()}")

# Тест сохранения
if manager.save_data(data):
    print("Data saved successfully!")
