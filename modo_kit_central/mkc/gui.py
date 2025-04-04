"""The main window for Modo Kit Central."""
from typing import Union, Type

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
from .prefs import Text, KEYS, DATA, Paths, TabRequest
from .widgets.tabs import tab_map, TAB, KitsTab
from .widgets.core import Banner


class KitCentralWindow(QMainWindow):
    """The core window for Modo Kit Central."""

    def __init__(self) -> None:
        """Initialization of the Kit Central Window."""
        super(KitCentralWindow, self).__init__(None)
        # Build the UI
        self._build_window()
        self._build_ui()
        self._build_tabs()
        self._connect_ui()
        # Display the UI
        self.show()

    def _build_window(self) -> None:
        """Sets up the main window properties."""
        self.setStyleSheet(DATA.CSS)
        self.setWindowTitle(Text.title)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.icon = QPixmap(Paths.ICON.as_posix())
        self.setWindowIcon(self.icon)
        self.setFixedWidth(512)
        self.resize(512, 400)

    def _build_ui(self) -> None:
        """Builds the UI for the Kit Central."""
        self.base_widget = QWidget(self)
        self.base_layout = QVBoxLayout(self.base_widget)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)
        self.base_widget.setLayout(self.base_layout)
        self.banner = Banner(Paths.BANNER_MKC)
        self.banner.setContentsMargins(0, 0, 0, 0)
        self.base_layout.addWidget(self.banner)
        self.setCentralWidget(self.base_widget)

    def _build_tabs(self) -> None:
        """Builds the tabs for Modo Kit Central."""
        # Generate Tabs
        self.tabs = QTabWidget()
        self.tab_bar = self.tabs.tabBar()
        self.tabs.setTabsClosable(True)
        self.tabs.setObjectName("Tabs")
        self.base_layout.addWidget(self.tabs)

        # Add the core tab
        self.tab_kits = self.load_tab(TabRequest(KEYS.KITS, closeable=False))
        # Add the help tab
        self.tab_help = self.load_tab(TabRequest(KEYS.INFO, closeable=False))

    def _connect_ui(self) -> None:
        """Connects the UI elements to their respective slots."""
        # Connect the tab bar to the close event.
        self.tab_bar.tabCloseRequested.connect(self._tab_close)
        # Connect the author request to the load tab function.
        self.tab_kits.author_request.connect(self.load_tab)

    def _tab_close(self, index: int) -> None:
        """Handle closing extra tabs.

        Args:
            index: The index of the tab to close.
        """
        if index in (0, 1):
            # Core tabs, don't close.
            return

        # Ge the widget attached to the tab
        tab_widget = self.tabs.widget(index)
        if tab_widget is not None:
            # Remove tab from tab widget
            self.tabs.removeTab(index)
            # Destroy widget as it's no longer needed.
            tab_widget.deleteLater()

    def load_tab(self, tab_request: TabRequest) -> Union[TAB, None]:
        """Open a new tab in the Kit Central main layout.

        Args:
            tab_request: The request to open a new tab.

        Returns:
            QWidget: The new tab widget if it was created, otherwise None.
        """
        # Get the intended tab name and check to see if it exists.
        tab_name = tab_request.name if tab_request.name else tab_request.type
        tab = self.tabs.findChild(QWidget, tab_name)
        # If the tab exists, get the index of the tab, else set it to -1.
        tab_index = self.tabs.indexOf(tab) if tab else -1

        if tab_index != -1:
            # The tab already exists, so just show it.
            self.tabs.setCurrentIndex(tab_index)
            return self.tabs.widget(tab_index)

        # Looks like we need to create a new tab. Let's grab it from the tab map.
        tab_class: Type[TAB] = tab_map.get(tab_request.type)
        if not tab_class:
            return None

        # Initialize the tab with the request data if it exists.
        new_tab = tab_class(**tab_request.kwargs) if tab_request.kwargs else tab_class()
        # Add the new tab to the tab bar and get the index.
        new_tab_index = self.tabs.addTab(new_tab, tab_name)

        if tab_request.show:
            # If the tab is requested to be shown, set it to the current index.
            self.tabs.setCurrentIndex(new_tab_index)
        if not tab_request.closeable:
            # If the tab is not closeable, set the close button to None.
            self.tab_bar.setTabButton(new_tab_index, QTabBar.RightSide, None)
            self.tab_bar.setTabButton(new_tab_index, QTabBar.LeftSide, None)

        return new_tab

    def closeEvent(self, event: QCloseEvent) -> None:
        """PySide method: Handle closing the UI

        Args:
            event: The close event from the Window.
        """
        self.close()
        event.accept()
