try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QCloseEvent, QPixmap
    from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTabBar, QLabel
except ImportError:
    # Fallback to PySide2 if PySide6 is not available
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QCloseEvent, QPixmap
    from PySide2.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTabBar, QLabel

# Kit imports
from .prefs import Text, KEYS, DATA, Paths
from .widgets import KitsTab


class KitCentralWindow(QMainWindow):
    """The core window for Modo Kit Central."""

    def __init__(self) -> None:
        """Initialization of the Kit Central Window."""
        super(KitCentralWindow, self).__init__(None)
        # Build the UI
        self._build_window()
        self._build_ui()
        self._build_tabs()
        # Display the UI
        self.show()

    def _build_window(self) -> None:
        """Sets up the main window properties."""
        self.setStyleSheet(DATA.CSS)
        self.setWindowTitle(Text.title)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setFixedWidth(512)
        self.resize(512, 364)

    def _build_ui(self) -> None:
        """Builds the UI for the Kit Central."""
        self.base_widget = QWidget(self)
        self.base_layout = QVBoxLayout(self.base_widget)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(6)
        self.base_widget.setLayout(self.base_layout)
        self.base_layout.addWidget(self._ui_banner())
        self.setCentralWidget(self.base_widget)

    def _ui_banner(self) -> QLabel:
        """Sets up the banner for the kits tab."""
        self.banner = QLabel()
        self.banner.setPixmap(QPixmap(Paths.IMAGES / "banner.png"))
        self.banner.setAlignment(Qt.AlignLeft)
        return self.banner

    def _build_tabs(self) -> None:
        """Builds the tabs for Modo Kit Central."""
        # Generate Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tab_close)
        self.tabs.setObjectName("Tabs")
        self.base_layout.addWidget(self.tabs)
        # Add the core tab
        self.tab_kits = KitsTab()
        self.tabs.addTab(self.tab_kits, KEYS.KITS)
        # Remove the close button from these core tab
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)
        # Remove close button on macOS
        self.tabs.tabBar().setTabButton(0, QTabBar.LeftSide, None)

    def closeEvent(self, event: QCloseEvent) -> None:
        """PySide method: Handle closing the UI

        Args:
            event: The close event from the Window.
        """
        self.close()
        event.accept()

    def tab_close(self, index: int) -> None:
        """Handle closing extra tabs.

        Args:
            index: The index of the tab to close.
        """
        if index == 0:
            # Core tab, don't close.
            return
        # Ge the widget attached to the tab
        tab_widget = self.tabs.widget(index)
        if tab_widget is not None:
            # Remove tab from tab widget
            self.tabs.removeTab(index)
            # Destroy widget as it's no longer needed.
            tab_widget.deleteLater()
