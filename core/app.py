from desktop.desktop import DesktopWindow
from desktop.window_manager import WindowManager
from core.logger import Logger
from core.settings import Settings
from core.theme_manager import ThemeManager
from core.plugin_manager import PluginManager
from core.service_registry import ServiceRegistry
from core.app_registry import AppRegistry
from core.process_manager import ProcessManager
from apps.files.explorer import FileExplorer
from apps.settings.settings import SettingsApp


class HarshOSApp:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.logger.info("Initializing HarshOS...")
        self.settings = Settings()
        self.logger.info("Settings loaded.")
        self.theme = ThemeManager(self.settings)
        self.logger.info(
            f"Themes loaded: {self.theme.current_theme()}"
        )
        self.plugin_manager = PluginManager(self.logger)
        self.plugin_manager.discover_plugins()
        self.window_manager = WindowManager(self.logger)
        self.registry = AppRegistry()
        self.process_manager = ProcessManager()
        self.running_apps = {}
        self.registry.register(
            app_id="files",
            name="Files",
            icon="📁",
            window_class=FileExplorer
        )
        self.registry.register(
            app_id="settings",
            name="Settings",
            icon="⚙",
            window_class=SettingsApp
        )
        ServiceRegistry.register("logger", self.logger)
        ServiceRegistry.register("settings", self.settings)
        ServiceRegistry.register("theme", self.theme)
        ServiceRegistry.register("plugin_manager", self.plugin_manager)
        ServiceRegistry.register("window_manager", self.window_manager)
        ServiceRegistry.register("process_manager", self.process_manager)
        self.window = DesktopWindow(self)
        self.window_manager.register(self.window)
        self.logger.info("Desktop initialized.")

    def start(self):
        self.logger.info("Starting HarshOS...")
        self.window.show()