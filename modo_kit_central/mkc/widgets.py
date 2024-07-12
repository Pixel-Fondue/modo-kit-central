import sqlite3

from PySide6.QtGui import QCursor, QDesktopServices, QPixmap, QIcon, QMouseEvent
from PySide6.QtCore import Qt, QUrl, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation
from PySide6.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QToolButton, QScrollArea, QPlainTextEdit, QSizePolicy,
    QFrame, QTabWidget, QLineEdit
)

from .prefs import KEYS, Text, Paths
from .prefs import DATA, KitData, AuthorData
from .utils import load_avatar
from .database import search_kits, get_kits, get_author


class KitWidget(QWidget):
    """Class to display the information of a given kit."""

    def __init__(self, kit_data: KitData) -> None:
        """Class to display the kit information in the main UI.

        Args:
            kit_data: The kit data from the database.
        """
        super(KitWidget, self).__init__()
        self.data = kit_data
        self.lbl_author = QLabel(f"Author: {self.data.author}")
        self.description = QPlainTextEdit(self.data.description)
        self.description.setReadOnly(True)
        self.description.setMaximumHeight(120)
        self.description.setMinimumHeight(20)
        self.btn_link = Button("View")
        self.btn_help = Button("Help")
        self.url_view = QUrl(self.data.url)
        self.url_help = QUrl(self.data.help)

        self.build_ui()

    def build_ui(self) -> None:
        """Builds the UI"""
        base_layout = QVBoxLayout()
        base_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(base_layout)

        self.description.setObjectName("description")

        self.lbl_author.setText(
            Text.author.format(self.data.author, self.data.author))
        self.lbl_author.mousePressEvent = self.open_author

        # Create the layout to hold the interactive buttons
        interactive_layout = QHBoxLayout()
        interactive_layout.setContentsMargins(0, 0, 0, 0)
        interactive_layout.addWidget(self.btn_link)
        interactive_layout.addWidget(self.btn_help)

        # Link urls
        self.btn_link.clicked.connect(lambda: QDesktopServices.openUrl(self.url_view))
        self.btn_help.clicked.connect(lambda: QDesktopServices.openUrl(self.url_help))

        # Add all elements to the base layout.
        base_layout.addWidget(self.description)
        base_layout.addLayout(interactive_layout)
        base_layout.addWidget(self.lbl_author)

    def open_author(self, event: QMouseEvent) -> None:
        """Opens the author tab when the author's name is clicked.

        Args:
            event: The mouse click event.
        """
        # Get the tab widget
        tab_widget: QTabWidget = DATA.mkc_window.tabs
        # Find if Author is already a tab
        author_widget = tab_widget.findChild(QScrollArea, self.data.author)
        if not author_widget:
            author_data = get_author(self.data.author)
            # Create new avatar tab
            author_widget = AuthorTab(author_data)
            tab_widget.addTab(author_widget, self.data.author)
        # Set the tab as active
        tab_widget.setCurrentIndex(tab_widget.indexOf(author_widget))


class AuthorTab(QScrollArea):
    def __init__(self, author_data: AuthorData, parent: QWidget = None) -> None:
        """Scroll area that populates with incoming author information.

        Args:
            author_data: Data for the given author.
            parent: Widget to set as parent.
        """
        super(AuthorTab, self).__init__(parent)
        self.data = author_data
        self.setObjectName(self.data.name)
        self.base_widget = QWidget()
        self.base_layout = QVBoxLayout()
        self.base_layout.setAlignment(Qt.AlignCenter)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setAlignment(Qt.AlignTop)

        self.base_widget.setLayout(self.base_layout)
        self.setWidgetResizable(True)
        self.setWidget(self.base_widget)

        # Load avatar if it exists.
        self.avatar = load_avatar(self.data.avatar)
        avatar_lbl = QLabel("test")
        avatar_lbl.setFixedSize(120, 100)
        # Load and scale avatar.
        avatar_pix = QPixmap(self.avatar).scaledToHeight(100)
        avatar_lbl.setPixmap(avatar_pix)
        self.base_layout.addWidget(avatar_lbl, alignment=Qt.AlignCenter)

        author_lbl = QLabel(self.data.name)
        self.base_layout.addWidget(author_lbl, alignment=Qt.AlignCenter)
        # TODO: Display all author kits from author view.
        # Display all links
        for text, url in self.data.links.items():
            link_lbl = QLabel()
            link_lbl.setText(Text.lbl_link.format(text=text, link=url))
            link_lbl.setOpenExternalLinks(True)
            self.base_layout.addWidget(link_lbl)


class KitTab(QScrollArea):
    """Class to display the kits in the main UI."""

    def __init__(self, parent: QWidget = None) -> None:
        """Scroll area that populates with incoming kit information.

        Args:
            parent: Widget to set as parent.
        """
        super(KitTab, self).__init__(parent)
        self.kits: list[FoldContainer] = []
        self.base_widget = QWidget()
        self.base_layout = QVBoxLayout()
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setAlignment(Qt.AlignTop)

        self.base_widget.setLayout(self.base_layout)
        self.setWidgetResizable(True)
        self.setWidget(self.base_widget)
        self.search_bar = KitSearchBar(self)
        self.base_layout.addWidget(self.search_bar)
        self.add_kits()

    def add_kits(self) -> None:
        """Iterate over the kit database table and add the kits to the UI."""
        for kit in get_kits():
            # Generate a collapsable container
            kit_data = KitData(*kit)
            kit_container = FoldContainer(name=kit_data.name, version=kit_data.version)
            kit_container.set_content(KitWidget(kit_data))
            self.kits.append(kit_container)
            self.base_layout.addWidget(kit_container)


class Button(QPushButton):

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


class FoldContainer(QWidget):

    def __init__(self, name: str = "test", version: str = None, parent: QWidget = None) -> None:
        """Class to create a collapsable container for the kit widgets.

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
        button_text = "{} ({})".format(name, version) if version else name
        self.toggle_button = QToolButton(text=button_text, checkable=True, checked=False)
        self.toggle_animation = QParallelAnimationGroup(self)
        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content = None
        self.build_ui()

    def build_ui(self) -> None:
        """Builds the UI"""
        self.toggle_button.setStyleSheet(DATA.CSS)
        self.toggle_button.setFixedHeight(17)
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
        # Initialize all added animations with the same values.
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(self.anim_length)
            animation.setStartValue(self.collapsed_height)
            animation.setEndValue(self.collapsed_height + height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(self.anim_length)
        content_animation.setStartValue(0)
        content_animation.setEndValue(height)


class KitSearchBar(QWidget):
    def __init__(self, kit_tab: KitTab, parent: QWidget = None):
        """Initialization of the search bar for the kits tab.

        Args:
            kit_tab: Widget to search children for.
            parent: Parent to attach widget to.
        """
        super(KitSearchBar, self).__init__(parent)
        self.kit_tab = kit_tab
        self.base_layout = QHBoxLayout()
        self.setLayout(self.base_layout)
        self.search_txt = QLineEdit()
        # Build the UI
        self.build_ui()

    def build_ui(self) -> None:
        """Builds the UI"""
        self.search_txt.setPlaceholderText("Search")
        self.base_layout.addWidget(self.search_txt)
        # Connect search bar to search function.
        self.search_txt.textChanged.connect(self.search)

    def search(self, text: str) -> None:
        """Handles searching the widgets and disabling the ones that do not match.

        Args:
            text: The search text.
        """
        # Get id of all matching kits
        kit_ids = search_kits(text)

        for kit_id, kit in enumerate(self.kit_tab.kits):
            if kit_id in kit_ids:
                kit.setVisible(True)
            else:
                kit.setVisible(False)


# Map to get the correct widget class based on the incoming data.
widget_map = {
    KEYS.KITS: KitWidget
}

widget_tabs = {
    KEYS.KITS: KitTab
}
