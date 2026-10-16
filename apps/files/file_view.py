from pathlib import Path

from PyQt6.QtCore import (
    Qt,
    QDir,
    pyqtSignal
)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QMenu,
    QInputDialog,
    QMessageBox
)


class FileView(QWidget):
    path_changed = pyqtSignal(str)
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.history = []
        self.history_index = -1
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(
            self.model.index(QDir.homePath())
        )
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        self.tree.setSortingEnabled(True)
        self.tree.setAnimated(True)
        layout.addWidget(self.tree)
        self.tree.doubleClicked.connect(
            self.item_double_clicked
        )
        self.tree.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.tree.customContextMenuRequested.connect(
            self.show_context_menu
        )
        self.open_path(QDir.homePath())

    def current_path(self):
        return self.model.filePath(
            self.tree.rootIndex()
        )

    def open_path(self, path):
        path = str(Path(path))
        index = self.model.index(path)
        if not index.isValid():
            return
        self.tree.setRootIndex(index)
        self.path_changed.emit(path)
        if (
            self.history_index == -1
            or self.history[self.history_index] != path
        ):
            self.history = self.history[:self.history_index + 1]
            self.history.append(path)
            self.history_index += 1

    def go_back(self):
        if self.history_index <= 0:
            return
        self.history_index -= 1
        index = self.model.index(
            self.history[self.history_index]
        )
        self.tree.setRootIndex(index)

    def go_forward(self):
        if self.history_index >= len(self.history) - 1:
            return
        self.history_index += 1
        index = self.model.index(
            self.history[self.history_index]
        )
        self.tree.setRootIndex(index)

    def go_up(self):
        current = Path(self.current_path())
        if current.parent != current:
            self.open_path(current.parent)

    def refresh(self):
        self.open_path(
            self.current_path()
        )

    def item_double_clicked(self, index):
        if self.model.isDir(index):
            self.open_path(
                self.model.filePath(index)
            )

    def show_context_menu(self, pos):
        index = self.tree.indexAt(pos)
        menu = QMenu(self)
        open_action = menu.addAction("Open")
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        new_folder_action = menu.addAction("New Folder")
        menu.addSeparator()
        refresh_action = menu.addAction("Refresh")
        action = menu.exec(
            self.tree.viewport().mapToGlobal(pos)
        )
        if action == open_action:
            if index.isValid():
                self.item_double_clicked(index)
        elif action == rename_action:
            self.rename_item(index)
        elif action == delete_action:
            self.delete_item(index)
        elif action == new_folder_action:
            self.create_folder()
        elif action == refresh_action:
            self.refresh()

    def rename_item(self, index):
        if not index.isValid():
            return
        old_path = Path(
            self.model.filePath(index)
        )
        new_name, ok = QInputDialog.getText(
            self,
            "Rename",
            "New name:",
            text=old_path.name
        )
        if not ok or not new_name.strip():
            return
        new_path = old_path.parent / new_name
        try:
            old_path.rename(new_path)
            self.refresh()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Rename Failed",
                str(e)
            )

    def delete_item(self, index):
        if not index.isValid():
            return
        path = Path(
            self.model.filePath(index)
        )
        reply = QMessageBox.question(
            self,
            "Delete",
            f"Delete '{path.name}'?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        try:
            if path.is_dir():
                path.rmdir()
            else:
                path.unlink()
            self.refresh()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Delete Failed",
                str(e)
            )

    def create_folder(self):
        current = Path(
            self.current_path()
        )
        name, ok = QInputDialog.getText(
            self,
            "New Folder",
            "Folder name:"
        )
        if not ok or not name.strip():
            return
        try:
            (current / name).mkdir()
            self.refresh()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )