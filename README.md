# Creon

> Modern cross-platform finance tracker built with Python & PyQt6.

![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey.svg)

---

## ✨ Features

- **Monthly tracking**: Auto-save to `{month}_{year}.json` format
- **Budget categories**: Pre-defined + custom categories with planned/actual columns
- **Real-time calculations**: Instant balance updates as you type
- **Dark/Light themes**: Toggle between color schemes
- **Custom storage path**: Choose where to store your data
- **Safe exit**: Prompt to save unsaved changes
- **Clean UI**: Modern design with smooth interactions

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.13 |
| GUI | PyQt6 |
| Package Manager | Poetry |
| Data Storage | JSON |
| Testing | pytest, pytest-qt |

---

## 📦 Installation

### Prerequisites
- Python 3.13+
- [Poetry](https://python-poetry.org/docs/#installation)

### Steps

```bash
# 1. Clone repository
git clone git@github.com:teslasteria/Creon.git
cd Creon

# 2. Install dependencies
poetry install

# 3. Run application
poetry run creon
# Or: poetry run python -m creon.main
```

### Optional: Download fonts (for Inter/Roboto support)
```bash
mkdir -p resources/fonts
# Download Inter: https://github.com/rsms/inter/releases
# Download Roboto: https://fonts.google.com/specimen/Roboto
# Place .ttf files in resources/fonts/
```

---

## 🚀 Usage

### First Launch
1. Application auto-loads current month's data
2. Default categories are created if no file exists
3. Set your **Total Funds** in the top panel

### Managing Data
| Action | Method |
|--------|--------|
| Edit budget | Double-click table cell |
| Add category | Click "+ Add Category" |
| Save data | `File → Save` or `Ctrl+S` |
| Load month | `File → Load` or `Ctrl+O` |
| Delete month | `File → Delete Month` |
| Change theme | `Settings → Toggle Theme` or `Ctrl+T` |
| Set storage path | `Settings → Set Storage Path` |

### Data Format
```
data/
├── january_2025.json
├── february_2025.json
└── ...

# File structure:
{
  "year": 2025,
  "month": 1,
  "total_funds": 1000.0,
  "categories": [
    {"name": "Rent", "planned": 500.0, "actual": 450.0},
    ...
  ]
}
```

---

## ⚙️ Configuration

Config file: `creon_config.json` (auto-created)

```json
{
  "storage_path": "/path/to/data",
  "theme": "dark",
  "language": "en"
}
```

| Key | Values | Default |
|-----|--------|---------|
| `storage_path` | Any writable directory | `./data` |
| `theme` | `dark`, `light` | `dark` |
| `language` | `en` | `en` |

---

## 📁 Project Structure

```
Creon/
├── src/creon/
│   ├── main.py              # Entry point
│   ├── core/
│   │   ├── config.py        # App configuration
│   │   ├── storage.py       # JSON file operations
│   │   └── theme_manager.py # Theme handling
│   ├── models/
│   │   └── finance.py       # Data models
│   └── views/
│       ├── main_window.py   # Main UI
│       └── styles.py        # UI utilities
├── resources/fonts/         # Optional custom fonts
├── data/                    # User financial data (gitignored)
├── tests/                   # pytest tests
├── pyproject.toml           # Poetry configuration
└── README.md
```

---

## 🧪 Testing

```bash
# Run all tests
poetry run pytest tests/ -v

# Run with coverage
poetry run pytest tests/ --cov=creon

# Format code
poetry run black src/ tests/
```

---

## 🔧 Development

```bash
# Activate virtual environment
poetry shell

# Add new dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name

# Update dependencies
poetry update
```

---

## ⚠️ Notes

- **Data files** (`data/*.json`, `creon_config.json`) are excluded from Git by default
- **Fonts are optional**: Application falls back to system fonts if custom fonts are missing
- **Cross-platform**: Tested on Linux and Windows

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

> **Creon** — Track your finances. Simple. Fast. Private.