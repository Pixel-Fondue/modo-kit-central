try:
    from PySide.QtCore import Qt, QTimer
    from PySide.QtGui import (QPixmap, QLabel, QDesktopWidget, QMainWindow, QCursor, QColor,
                              QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget,
                              QListWidget, QListWidgetItem)
except (ImportError, ModuleNotFoundError):
    from PySide2.QtCore import Qt, QTimer
    from PySide2.QtGui import QCursor, QPixmap, QColor
    from PySide2.QtWidgets import (QLabel, QDesktopWidget, QMainWindow, QApplication, QTabWidget,
                                   QPushButton, QWidget, QVBoxLayout, QListWidget, QListWidgetItem)
# Kit imports
from com_hub.prefs import Text, KEYS, CSS
from com_hub.utils import load_resource
from com_hub.widgets import widget_map


class CommunityHub(QMainWindow):

    def __init__(self):
        super(CommunityHub, self).__init__(None)
        self.setWindowTitle(Text.title)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.build_ui()

        # Display the UI
        self.show()

    def build_ui(self):
        base_widget = QWidget(self)
        base_layout = QVBoxLayout(base_widget)
        base_layout.setContentsMargins(2, 2, 2, 2)
        base_widget.setLayout(base_layout)

        # Generate Tabs
        tabs = QTabWidget()
        base_layout.addWidget(tabs)

        tab_video = self.build_tab(KEYS.videos)
        tabs.addTab(tab_video, KEYS.videos)
        tab_kits = self.build_tab(KEYS.kits)
        tabs.addTab(tab_kits, KEYS.kits)

        self.setCentralWidget(base_widget)
        self.setStyleSheet(CSS)

    def build_tab(self, tab_type):
        # Get tab resource
        tab_data = load_resource(tab_type)
        if not tab_data:
            return

        widget_class = widget_map.get(tab_type)
        print(widget_class)
        tab_list = QListWidget()

        for name, info in tab_data.items():
            print(name)
            # Create QList widget for item
            item = QListWidgetItem()
            # Create Widget for info
            widget = widget_class(name, info)
            # Add the QListWidgetItem to the QListView
            tab_list.addItem(item)
            # Set the widget to the QListWidgetItem
            tab_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())
            print(widget)
        return tab_list

    def closeEvent(self, event):
        """ PySide method: Handle closing the UI"""
        self.close()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = CommunityHub()

    sys.exit(app.exec_())
