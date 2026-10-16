from pathlib import Path


# ==========================
# Application Information
# ==========================

APP_NAME = "HarshOS"
APP_VERSION = "0.1.0"
ORGANIZATION = "Harshith Tech"

# ==========================
# Project Paths
# ==========================

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
THEMES_DIR = ROOT_DIR / "themes"
PLUGINS_DIR = ROOT_DIR / "plugins"
DATABASE_DIR = ROOT_DIR / "database"
LOGS_DIR = ROOT_DIR / "logs"


# Create required folders automatically
for folder in (
    THEMES_DIR,
    PLUGINS_DIR,
    DATABASE_DIR,
    LOGS_DIR,
):
    folder.mkdir(parents=True, exist_ok=True)


# ==========================
# Database
# ==========================

DATABASE_FILE = DATABASE_DIR / "harshos.db"

# ==========================
# Window
# ==========================

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850
MIN_WINDOW_WIDTH = 1000
MIN_WINDOW_HEIGHT = 650

# ==========================
# Theme
# ==========================

DEFAULT_THEME = "dark"

# ==========================
# Logging
# ==========================

LOG_FILE = LOGS_DIR / "harshos.log"

# ==========================
# Fonts
# ==========================

DEFAULT_FONT = "Segoe UI"
DEFAULT_FONT_SIZE = 10

# ==========================
# AI
# ==========================

DEFAULT_LLM = "llama3"

# ==========================
# Application
# ==========================

FPS = 60