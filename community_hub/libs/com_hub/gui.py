try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout)
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import (QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout)

# Kit imports
from com_hub.prefs import Text, KEYS, CSS
from com_hub.utils import load_resource
from com_hub.gui_utils import build_tab


class CommunityHub(QMainWindow):

    def __init__(self):
        super(CommunityHub, self).__init__(None)
        self.setWindowTitle(Text.title)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.resize(450, 300)
        self.authors = load_resource(KEYS.authors)
        self.build_ui()

        # Display the UI
        self.show()

    def build_ui(self):
        base_widget = QWidget(self)
        base_layout = QVBoxLayout(base_widget)
        base_layout.setContentsMargins(2, 2, 2, 2)
        base_widget.setLayout(base_layout)

        # Generate Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tab_close)
        self.tabs.setObjectName("Tabs")
        base_layout.addWidget(self.tabs)

        for tab_type in (KEYS.videos, KEYS.kits, KEYS.social):
            tab = build_tab(tab_type)
            self.tabs.addTab(tab, tab_type)

        self.setCentralWidget(base_widget)
        self.setStyleSheet(CSS)

    def closeEvent(self, event):
        """ PySide method: Handle closing the UI"""
        self.close()
        event.accept()

    def tab_close(self, index):
        """Handle closing Author tabs."""
        if index > 2:
            # Ge the widget attached to the tab
            tab_widget = self.tabs.widget(index)
            # Remove tab from tab widget
            self.tabs.removeTab(index)
            # Destroy widget as it's no longer needed.
            del tab_widget


if __name__ == "__main__":
    """Used to test this UI outside of Modo"""
    import sys

    app = QApplication(sys.argv)

    window = CommunityHub()

    sys.exit(app.exec_())
