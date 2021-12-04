# python
try:
    from PySide2.QtCore import Qt, QUrl, QParallelAnimationGroup, QPropertyAnimation, \
        QAbstractAnimation
    from PySide2.QtGui import QCursor, QDesktopServices, QPixmap
    from PySide2.QtWidgets import (QLabel, QApplication, QWidget, QVBoxLayout, QPushButton,
                                   QHBoxLayout, QToolButton, QScrollArea, QPlainTextEdit,
                                   QSizePolicy, QFrame, QTabWidget, QLineEdit)
except ImportError:
    from PySide.QtCore import Qt, QUrl, QParallelAnimationGroup, QPropertyAnimation, \
        QAbstractAnimation
    from PySide.QtGui import (QLabel, QCursor, QApplication, QWidget, QVBoxLayout, QPushButton,
                              QHBoxLayout, QDesktopServices, QToolButton, QScrollArea, QSizePolicy,
                              QFrame, QPixmap, QTabWidget, QPlainTextEdit, QLineEdit)

from com_hub.prefs import KEYS, authors, Text, CSS_FOLD
from com_hub.utils import load_avatar


class AuthorTab(QScrollArea):
    def __init__(self, name, author_data, parent=None):
        """Scroll area that populates with incoming author information.

        Args:
            name (str): Name of the author.
            author_data (dict): Data for the given author.
            parent (QWidget): Widget to set as parent.
        """
        super(AuthorTab, self).__init__(parent)
        self.author_data = author_data
        self.name = name
        self.setObjectName(name)
        self.base_widget = QWidget()
        self.base_layout = QVBoxLayout()
        self.base_layout.setAlignment(Qt.AlignCenter)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setAlignment(Qt.AlignTop)

        self.base_widget.setLayout(self.base_layout)
        self.setWidgetResizable(True)
        self.setWidget(self.base_widget)

        # Load avatar if it exists.
        self.avatar = load_avatar(author_data.get('avatar'))
        avatar_lbl = QLabel("test")
        avatar_lbl.setFixedSize(64, 64)
        # Load and scale avatar.
        avatar_pix = QPixmap(self.avatar).scaledToHeight(64)
        avatar_lbl.setPixmap(avatar_pix)
        self.base_layout.addWidget(avatar_lbl, alignment=Qt.AlignCenter)

        author_lbl = QLabel(name)
        self.base_layout.addWidget(author_lbl, alignment=Qt.AlignCenter)

        for text, url in author_data.get('links').items():
            link_lbl = QLabel()
            link_lbl.setText(Text.lbl_link.format(text=text, link=url))
            link_lbl.setOpenExternalLinks(True)
            self.base_layout.addWidget(link_lbl)


class KitTab(QScrollArea):
    def __init__(self, kit_data, parent=None):
        """Scroll area that populates with incoming kit information.

        Args:
            kit_data (dict): Data for each kit to add.
            parent (QWidget): Widget to set as parent.
        """
        super(KitTab, self).__init__(parent)
        self.kit_data = kit_data
        self.base_widget = QWidget()
        self.base_layout = QVBoxLayout()
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setAlignment(Qt.AlignTop)

        self.base_widget.setLayout(self.base_layout)
        self.setWidgetResizable(True)
        self.setWidget(self.base_widget)
        self.search_bar = SearchBar(self)
        self.base_layout.addWidget(self.search_bar)
        self.add_kits()

    def add_kits(self):
        """Adds all kits listed in the kits data. data from kits.json"""
        for kit_name, kit_info in sorted(self.kit_data.items()):
            # Generate a collapsable container
            container = FoldContainer(name=kit_name, version=kit_info.get('version', "N/A"))
            # Add kit widget to container
            container.set_content(KitWidget(kit_info))
            # Add container to the scroll-area
            self.base_layout.addWidget(container)


class KitWidget(QWidget):
    def __init__(self, info):
        """Class to display the kit information in the main UI.

        Args:
            info (dict): The information about the kit.
        """
        super(KitWidget, self).__init__()
        self.search = info.get('search', [])
        self.author = info.get('author')
        self.author_data = authors.get(self.author)
        self.lbl_author = QLabel("Author: {}".format(info.get('author')))
        self.description = QPlainTextEdit(info.get('description'))
        self.description.setReadOnly(True)
        self.description.setMaximumHeight(120)
        self.description.setMinimumHeight(20)
        self.btn_link = Button("View")
        self.btn_help = Button("Help")
        self.url_view = QUrl(info.get('url'))
        self.url_help = QUrl(info.get('help'))

        self.build_ui()

    def build_ui(self):
        """Builds the UI"""
        base_layout = QVBoxLayout()
        base_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(base_layout)

        self.description.setObjectName("description")

        # Setup Author link
        if self.author_data:
            self.lbl_author.setText(
                Text.author.format(self.author_data.get("profile"), self.author))
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

    def open_author(self, event):
        # Get the tab widget
        tab_widget = self.window().findChild(QTabWidget, "Tabs")  # type: QTabWidget
        # Find if Author is already a tab
        author_widget = tab_widget.findChild(QScrollArea, self.author)
        if not author_widget:
            # Create new avatar tab
            author_widget = AuthorTab(self.author, self.author_data)
            tab_widget.addTab(author_widget, self.author)
        # Set the tab as active
        tab_widget.setCurrentIndex(tab_widget.indexOf(author_widget))


class VideoWidget(QWidget):

    def __init__(self, title, info):
        """Class to display the video information in the main UI.

        Args:
            title (str): The name of the video.
            info (dict): The description of the video.
        """
        super(VideoWidget, self).__init__()

        self.lbl_title = QLabel(title)
        self.description = QLabel(info.get("description"))
        self.btn_link = Button("Open")
        self.url_view = QUrl(info.get("url"))

        self.build_ui()

    def build_ui(self):
        """Builds the UI"""
        base_layout = QVBoxLayout()
        base_layout.setContentsMargins(0, 2, 0, 0)
        self.setLayout(base_layout)

        self.description.setWordWrap(True)
        self.description.setObjectName("description")

        # Link urls
        self.btn_link.clicked.connect(lambda: QDesktopServices.openUrl(self.url_view))

        # Add all elements to the base layout.
        base_layout.addWidget(self.lbl_title)
        base_layout.addWidget(self.description)
        base_layout.addWidget(self.btn_link)


class SocialWidget(QWidget):

    def __init__(self, title, info):
        """Class to display the social media information in the main UI.

        Args:
            title (str): The name of the social media site.
            info (dict): The information about the site..
        """
        super(SocialWidget, self).__init__()

        self.lbl_title = QLabel(title)
        self.description = QLabel(info.get("description"))
        self.btn_link = Button("Open")
        self.url_view = QUrl(info.get("url"))

        self.build_ui()

    def build_ui(self):
        """Builds the UI"""
        base_layout = QHBoxLayout()
        base_layout.setContentsMargins(0, 2, 0, 0)
        self.setLayout(base_layout)

        self.description.setWordWrap(True)
        self.description.setObjectName("description")

        # Link urls
        self.btn_link.clicked.connect(lambda: QDesktopServices.openUrl(self.url_view))

        # Add all elements to the base layout.
        base_layout.addWidget(self.lbl_title)
        base_layout.addWidget(self.description)
        base_layout.addWidget(self.btn_link)


class Button(QPushButton):

    def __init__(self, text="Button", icon=None):
        """Inherited Pushbutton class to format all buttons alike.

        Args:
            text (str): The text to display on the button.
            icon (QIcon): The icon to display on the button.
        """
        super(Button, self).__init__(text)
        # Add icon if given one.
        if icon:
            self.setIcon(icon)
        # Enable the pointer mouse.
        self.setCursor(QCursor(Qt.PointingHandCursor))


class FoldContainer(QWidget):

    def __init__(self, name="test", version=0, parent=None):
        super(FoldContainer, self).__init__(parent)
        self.setObjectName(name)
        self.anim_length = 200
        self.forward = QAbstractAnimation.Forward
        self.reverse = QAbstractAnimation.Backward
        self.toggle_button = QToolButton(
            text="{} ({})".format(name, version),
            checkable=True, checked=False
        )
        self.toggle_animation = QParallelAnimationGroup(self)
        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content = None
        self.build_ui()

    def build_ui(self):
        self.toggle_button.setStyleSheet(CSS_FOLD)
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

    def on_pressed(self):
        """Enable animation when user selects the bar."""
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        self.toggle_animation.setDirection(self.forward if not checked else self.reverse)
        self.toggle_animation.start()

    def set_content(self, content):
        """Sets a widget as the containers displayable content.

        Args:
            content (QWidget): The widget to set as the core content.
        """
        self.content = content
        # Create new layout
        lay = QVBoxLayout()
        # Add content to layout
        lay.addWidget(self.content)
        # Set layout as the main content layout
        self.content_area.setLayout(lay)
        # Calculate the height of the widget when closed.
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        # Get the current height of the new layout with added content
        content_height = lay.sizeHint().height()
        # Initialize all added animations with the same values.
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(self.anim_length)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(self.anim_length)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


class SearchBar(QWidget):
    def __init__(self, search_tab, parent=None):
        """Initialization of the search bar.

        Args:
            search_tab (QWidget): Widget to search children for.
            parent (QWidget): Parent to attach widget to.
        """
        super(SearchBar, self).__init__(parent)
        self.search_tab = search_tab
        self.base_layout = QHBoxLayout()
        self.setLayout(self.base_layout)
        self.search_txt = QLineEdit()
        # Build the UI
        self.build_ui()

    def build_ui(self):
        self.search_txt.setPlaceholderText("Search")
        # search_btn = Button("search")
        # search_btn.setFixedWidth(75)
        self.base_layout.addWidget(self.search_txt)
        # self.base_layout.addWidget(search_btn)
        # Connect search bar to search function.
        self.search_txt.textChanged.connect(self.search)

    def search(self, text):
        """Handles searching the widgets and disabling the ones that do not match.

        Args:
            text (str): The search text.
        """
        search_text = text.lower()
        # Find all Fold containers
        for child in self.search_tab.findChildren(FoldContainer):  # type: FoldContainer
            # Adjust the visibility based on the search.
            match_terms = any(s for s in child.content.search if search_text in s)
            match_author = search_text in child.content.author.lower()
            match_name = search_text in child.objectName().lower()
            child.setVisible(any((match_terms, match_author, match_name)))


# Map to get the correct widget class based on the incoming data.
widget_map = {
    KEYS.kits: KitWidget,
    KEYS.videos: VideoWidget,
    KEYS.social: SocialWidget
}

if __name__ == "__main__":
    """Used to test this UI outside of Modo"""
    import sys

    app = QApplication(sys.argv)
    base = QWidget()
    base.show()

    sys.exit(app.exec_())
