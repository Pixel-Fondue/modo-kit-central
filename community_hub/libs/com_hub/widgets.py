# python
try:
    from PySide2.QtCore import Qt, QTimer, QUrl
    from PySide2.QtGui import QCursor, QPixmap, QColor, QFont, QDesktopServices
    from PySide2.QtWidgets import (QLabel, QDesktopWidget, QMainWindow, QApplication, QTabWidget,
                                   QPushButton, QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                                   QHBoxLayout, QPlainTextEdit, QSpacerItem)
except ImportError:
    from PySide.QtCore import Qt, QTimer, QUrl
    from PySide.QtGui import (QPixmap, QLabel, QDesktopWidget, QMainWindow, QCursor, QColor,
                              QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget,
                              QListWidget, QListWidgetItem, QHBoxLayout, QPlainTextEdit,
                              QSpacerItem, QDesktopServices)

from com_hub.prefs import KEYS
from com_hub.prefs import authors, Text


class KitWidget(QWidget):
    def __init__(self, name, info):
        """Class to display the kit information in the main UI.

        Args:
            name (str): The name of the kit.
            info (dict): The information about the kit.
        """
        super(KitWidget, self).__init__()

        self.lbl_title = QLabel(name)
        self.lbl_version = QLabel(info.get("version"))
        self.author = info.get("author")
        self.lbl_author = QLabel("Author: {}".format(info.get("author")))
        self.description = QLabel(info.get("description"))
        self.btn_link = QPushButton("View")
        self.btn_help = QPushButton("Help")
        self.url_view = QUrl(info.get("url"))
        self.url_help = QUrl(info.get("help"))

        self.build_ui()

    def build_ui(self):
        """Builds the UI"""
        base_layout = QVBoxLayout()
        base_layout.setContentsMargins(0, 2, 0, 0)
        self.setLayout(base_layout)
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(self.lbl_version)

        self.description.setWordWrap(True)
        self.description.setObjectName("description")

        # Setup Author link
        author_data = authors.get(self.author)
        if author_data:
            self.lbl_author.setText(Text.author.format(author_data.get("profile"), self.author))
            self.lbl_author.setOpenExternalLinks(True)

        # Create the layout to hold the interactive buttons
        interactive_layout = QHBoxLayout()
        interactive_layout.addWidget(self.btn_link)
        interactive_layout.addWidget(self.btn_help)

        # Link urls
        self.btn_link.clicked.connect(lambda: QDesktopServices.openUrl(self.url_view))
        self.btn_help.clicked.connect(lambda: QDesktopServices.openUrl(self.url_help))

        # Add all elements to the base layout.
        base_layout.addLayout(header_layout)
        base_layout.addWidget(self.lbl_author)
        base_layout.addWidget(self.description)
        base_layout.addLayout(interactive_layout)


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
        self.btn_link = QPushButton("Open")
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
        self.btn_link = QPushButton("Open")
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


# Map to get the correct widget class based on the incoming data.
widget_map = {
    KEYS.kits: KitWidget,
    KEYS.videos: VideoWidget,
    KEYS.social: SocialWidget
}

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    data = {"author": "Shawn Frueh",
            "version": "2.0",
            "description": "The Python Mesh Operator, PyMop, allows you to edit the code of a mesh operator live from within MODO!",
            "url": "https://shawnfrueh.gumroad.com/l/pyMop",
            "help": "https://community.foundry.com/discuss/topic/139479/kit-the-python-mesh-operator"
            }
    kit_widget = KitWidget(name="pyMop", info=data)
    kit_widget.show()

    sys.exit(app.exec_())
