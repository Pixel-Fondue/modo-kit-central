"""Core widgets for Modo Kit Central."""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tabs import KitsTab

try:
    from PySide6.QtGui import QCursor, QDesktopServices, QMouseEvent
    from PySide6.QtGui import QPixmap, QIcon
    from PySide6.QtCore import Qt, QUrl, Signal
    from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation
    from PySide6.QtWidgets import (
        QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QToolButton, QScrollArea,
        QPlainTextEdit, QSizePolicy, QFrame, QTabWidget, QLineEdit
    )
except ImportError:
    # Fallback to PySide2 if PySide6 is not available
    from PySide2.QtGui import QCursor, QDesktopServices, QMouseEvent
    from PySide2.QtGui import QPixmap, QIcon
    from PySide2.QtCore import Qt, QUrl, Signal
    from PySide2.QtCore import QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation
    from PySide2.QtWidgets import (
        QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QToolButton, QScrollArea,
        QPlainTextEdit, QSizePolicy, QFrame, QTabWidget, QLineEdit
    )

from ..prefs import Text, DATA, KitData, KitInfo, KitAction
from ..files import Paths
from ..database import search_kits
from ..update import update_kit


class Button(QPushButton):
    """Class to format all buttons alike."""

    def __init__(self, text: str = "Button", icon: QIcon = None) -> None:
        """Inherited Pushbutton class to format all buttons alike.

        Args:
            text: The text to display on the button.
            icon: The icon to display on the button.
        """
        super(Button, self).__init__(text)
        # Add icon if given one.
        if icon:
            self.setIcon(icon)
        # Enable the pointer mouse.
        self.setCursor(QCursor(Qt.PointingHandCursor))


class Banner(QLabel):
    """Class to display a banner image."""

    def __init__(self, image: Path, parent: QWidget = None) -> None:
        """Banner class to display a Kit banner.

        Args:
            image: The image to display as the banner.
            parent: The parent widget.
        """
        super(Banner, self).__init__(parent)
        self.setAlignment(Qt.AlignLeft)
        self.setContentsMargins(0, 0, 0, 0)
        self.setPixmap(QPixmap(image.as_posix()))
        # Remove padding for pixmap
        self.setScaledContents(True)


class FoldContainer(QWidget):
    """Class to create a collapsable container for the kit widgets."""

    def __init__(self, name: str = "test", version: str = None, parent: QWidget = None) -> None:
        """Initialization of the FoldContainer class.

        Args:
            name: The name of the container.
            version: The version of the kit.
            parent: The parent widget.
        """
        super(FoldContainer, self).__init__(parent)
        self.setObjectName(name)
        self.layout = QVBoxLayout()
        self.anim_length = 200
        self.collapsed_height = 0
        self.forward = QAbstractAnimation.Forward
        self.reverse = QAbstractAnimation.Backward
        button_text = f"{name} v{version}" if version else name
        self.toggle_button = QToolButton(text=button_text, checkable=True, checked=False)
        self.toggle_animation = QParallelAnimationGroup(self)
        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Builds the UI"""
        self.setContentsMargins(0, 0, 0, 0)
        self.toggle_button.setFixedHeight(20)
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        # Enable the pointer mouse.
        self.toggle_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_button.pressed.connect(self.on_pressed)

        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setFrameShape(QFrame.NoFrame)

        container_layout = QVBoxLayout(self)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.toggle_button)
        container_layout.addWidget(self.content_area)
        # Add animations for smooth opening
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, b"maximumHeight"))

    def on_pressed(self) -> None:
        """Enable animation when user selects the bar."""
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        self.toggle_animation.setDirection(self.forward if not checked else self.reverse)
        self.toggle_animation.start()

    def expand(self, value: int) -> None:
        """Expands the content to fit more stuff.

        Args:
            value: The height value to expand the content by.
        """
        content_height = self.layout.sizeHint().height() + value
        # Initialize all added animations with the same values.
        self.animation_setup(content_height)
        self.toggle_animation.start()

    def set_content(self, content: QWidget) -> None:
        """Sets a widget as the containers displayable content.

        Args:
            content: The widget to set as the core content.
        """
        self.content = content
        # Add content to layout
        self.layout.addWidget(self.content)
        # Set layout as the main content layout
        self.content_area.setLayout(self.layout)
        # Calculate the height of the widget when closed.
        self.collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        # Get the current height of the new layout with added content
        content_height = self.layout.sizeHint().height()
        self.animation_setup(content_height)

    def animation_setup(self, height: int) -> None:
        """Sets up the animations for the container for a smooth open/close.

        Args:
            height: The height to animate to.
        """
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(self.anim_length)
            animation.setStartValue(self.collapsed_height)
            animation.setEndValue(self.collapsed_height + height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(self.anim_length)
        content_animation.setStartValue(0)
        content_animation.setEndValue(height)


class KitWidget(QWidget):
    """Class to display the information of a given kit."""
    author_clicked = Signal(str)

    def __init__(self, kit_data: KitData, show_author: bool = True) -> None:
        """Class to display the kit information in the main UI.

        Args:
            kit_data: The kit data from the database.
            show_author: Whether to show the author information. Default is True.
        """
        super(KitWidget, self).__init__()
        self.kit_data = kit_data
        self.show_author = show_author
        self.install_action = KitAction.NONE
        self._build_ui()
        self._connect_ui()

    def _build_ui(self) -> None:
        """Builds the UI for the kit widget."""
        self.setContentsMargins(0, 0, 0, 0)
        self.base_layout = QVBoxLayout()
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.base_layout)
        self.lbl_author = QLabel(f"Author: {self.kit_data.author}")

        self.description = QPlainTextEdit(self.kit_data.description)
        self.description.setObjectName("description")
        self.description.setReadOnly(True)
        self.description.setMaximumHeight(120)
        self.description.setMinimumHeight(40)

        self.btn_link = Button("View")
        self.url_view = QUrl(self.kit_data.url)

        self.btn_install = Button("Install")

        self.btn_help = Button("Help")
        self.url_help = QUrl(self.kit_data.help)

        # Create the layout to hold the interactive buttons
        self.interactive_layout = QHBoxLayout()
        self.interactive_layout.setContentsMargins(0, 0, 0, 0)
        self.interactive_layout.addWidget(self.btn_link)
        self.interactive_layout.addWidget(self.btn_install)
        self.interactive_layout.addWidget(self.btn_help)

        # Check if banner is available and add it to the widget.
        self._add_banner()
        # Add all elements to the base layout.
        self.base_layout.addWidget(self.description)
        self.base_layout.addLayout(self.interactive_layout)

        # Add author information if needed.
        if self.show_author:
            self.base_layout.addWidget(self.lbl_author)
            self.lbl_author.setText(
                Text.author.format(self.kit_data.author, self.kit_data.author))
            self.lbl_author.mousePressEvent = self._emit_author

        # Check if the kit is installable.
        if self.kit_data.installable:
            self._add_action_button()

    def _add_action_button(self) -> None:
        """Adds the action button."""
        installed_kit = DATA.modo_kits.get(self.kit_data.name, False)
        if not installed_kit:
            self.install_action = KitAction.INSTALL
            self.btn_install.setText("Install")
        elif installed_kit and installed_kit.version != self.kit_data.version:
            self.install_action = KitAction.UPDATE
            self.btn_install.setText(
                f"Update! v{installed_kit.version} -> {self.kit_data.version}"
            )
            self.btn_install.setProperty('update', True)
        else:
            # The kit is already installed, show option to uninstall.
            self.install_action = KitAction.UNINSTALL
            self.btn_install.setText("Uninstall")
            self.btn_install.setDisabled(True)

    def _add_banner(self) -> None:
        """Adds a banner to the widget if it exists."""
        banner_image = Paths.BANNERS / f"{self.kit_data.name}.png"
        if banner_image.exists():
            self.banner = Banner(image=banner_image)
            self.base_layout.addWidget(self.banner)

    def _connect_ui(self) -> None:
        """Connects the UI elements to their respective functions."""
        self.btn_link.clicked.connect(lambda: QDesktopServices.openUrl(self.url_view))
        self.btn_help.clicked.connect(lambda: QDesktopServices.openUrl(self.url_help))
        self.btn_install.clicked.connect(self._handle_action)

    def _emit_author(self, event: QMouseEvent) -> None:
        """Emits the author clicked signal when the author label is clicked.

        Args:
            event: The mouse click event.
        """
        self.author_clicked.emit(self.kit_data.author)

    def _handle_action(self) -> None:
        """Handles the installable button."""
        print(self.install_action.value)
        update_kit(self.kit_data)


class KitInfoWidget(QWidget):
    """Class to display information about an installed kit that is not in the database."""

    def __init__(self, kit_info: KitInfo) -> None:
        """Initialization of the kit info widget.

        Args:
            kit_info: Information about an installed kit.
        """
        super(KitInfoWidget, self).__init__()
        self.kit_info = kit_info
        self._build_ui()

    def _build_ui(self) -> None:
        """Builds the UI for the kit info widget."""
        self.base_layout = QVBoxLayout()
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.base_layout)

        # Display kit name and status
        status = "Enabled" if self.kit_info.enabled else "Disabled"
        self.name_label = QLabel(f"{self.kit_info.name} ({status})")
        self.name_label.setObjectName("kit-name")

        # Display version
        self.version_label = QLabel(f"Version: {self.kit_info.version}")

        # Display path
        self.path_label = QLabel(f"Path: {self.kit_info.path}")
        self.path_label.setWordWrap(True)

        # Add widgets to layout
        self.base_layout.addWidget(self.name_label)
        self.base_layout.addWidget(self.version_label)
        self.base_layout.addWidget(self.path_label)


class KitSearchBar(QWidget):
    """Custom search bar for the kits tab."""

    def __init__(self, kit_tab: 'KitsTab', parent: QWidget = None):
        """Initialization of the search bar for the kits tab.

        Args:
            kit_tab: Widget to search children for.
            parent: Parent to attach widget to.
        """
        super(KitSearchBar, self).__init__(parent)
        self.kit_tab = kit_tab
        # Build the UI
        self._build_ui()

    def _build_ui(self) -> None:
        """Builds the UI for the search bar."""
        self.base_layout = QHBoxLayout()
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.base_layout)
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("kit_search")
        self.search_bar.setPlaceholderText("Search...")
        # Set placeholder property for css.
        self.search_bar.setProperty("placeholder", True)
        self.base_layout.addWidget(self.search_bar)
        # Connect search bar to search function.
        self.search_bar.textChanged.connect(self.search)

    def search(self, text: str) -> None:
        """Handles searching the widgets and disabling the ones that do not match.

        Note:
            If there seems to be a performance issue,
            consider using a QSortFilterProxyModel here.

        Args:
            text: The search text.
        """
        show_placeholder = not bool(text)
        self.search_bar.setProperty("placeholder", show_placeholder)
        # Refresh the style to show/hide the placeholder.
        self.search_bar.style().polish(self.search_bar)
        # Get id of all matching kits
        kit_ids = search_kits(text)
        # Iterate over all kits and set visibility based on search.
        for kit_id, kit in enumerate(self.kit_tab.kits):
            if kit_id in kit_ids:
                kit.setVisible(True)
            else:
                kit.setVisible(False)

        # Iterate over all local kits that are not in the database.
        search_terms = [s.strip().lower() for s in text.split(",")]

        for kit in self.kit_tab.local_kits:
            if any(term in kit.content.kit_info.name.lower() for term in search_terms):
                kit.setVisible(True)
            else:
                kit.setVisible(False)
