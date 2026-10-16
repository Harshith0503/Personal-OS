from PyQt6.QtCore import QObject, pyqtSignal


class ProcessManager(QObject):
    processes_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.processes = {}

    def start(self, app_id, window):
        self.processes[app_id] = window
        self.processes_changed.emit()

    def stop(self, app_id):
        if app_id in self.processes:
            del self.processes[app_id]
            self.processes_changed.emit()

    def get(self, app_id):
        return self.processes.get(app_id)

    def all(self):
        return self.processes.items()

    def is_running(self, app_id):
        return app_id in self.processes