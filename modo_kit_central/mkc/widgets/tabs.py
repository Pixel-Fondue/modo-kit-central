"""MKC core tab widgets."""
from typing import List, Dict, Type, TypeVar

try:
    from PySide6.QtGui import QPixmap
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtWidgets import (
        QLabel, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QStyle
    )
except ImportError:
    # Fallback to PySide2 if PySide6 is not available
    from PySide2.QtGui import QPixmap
    from PySide2.QtCore import Qt, QThread, Signal
    from PySide2.QtWidgets import (
        QLabel, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QStyle
    )

from ..prefs import Text, AuthorData, KEYS, TabRequest, DATA
from ..files import Paths
from ..database import get_kits, get_author_kits, get_author
from ..github import DatabaseWorker, AvatarWorker
from .core import FoldContainer, KitSearchBar, KitWidget, KitInfoWidget


class KitsTab(QWidget):
    """Class to display the kits in the main UI."""
    author_request = Signal(TabRequest)

    def __init__(self, parent: QWidget = None) -> None:
        """Scroll area that populates with incoming kit information.

        Args:
            parent: Widget to set as parent.
        """
        super(KitsTab, self).__init__(parent)
        self.kits: List[FoldContainer] = []
        self.local_kits: List[FoldContainer] = []
        self._build_ui()
        self._sync_database()

    def _build_ui(self) -> None:
        """Sets up the UI for the kit tab."""
        self.setContentsMargins(4, 4, 4, 4)
        # Search
        self.search_bar = KitSearchBar(self)
        # Base layout for the tab
        self.base_widget = QWidget()
        self.base_layout = QVBoxLayout()
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setAlignment(Qt.AlignTop)
        self.base_layout.addWidget(self.search_bar)
        self.base_widget.setLayout(self.base_layout)
        # Scroll area for kits
        self.kits_widget = QWidget()
        self.kits_scroll = QScrollArea()
        self.kits_scroll.setContentsMargins(0, 0, 0, 0)
        self.kits_scroll.setWidget(self.kits_widget)
        self.kits_scroll.setWidgetResizable(True)
        self.kits_layout = QVBoxLayout()
        self.kits_layout.setContentsMargins(0, 0, 0, 0)
        self.kits_layout.setAlignment(Qt.AlignTop)
        self.kits_scroll.setWidget(self.kits_widget)
        self.kits_widget.setLayout(self.kits_layout)
        # Add Kits to the base layout
        self.base_layout.addWidget(self.kits_scroll)
        # Set the base layout as the main layout
        self.setLayout(self.base_layout)

    def _sync_database(self) -> None:
        """Spawns a thread to handle pulling the latest kit database."""
        self.thread = QThread()
        self.worker = DatabaseWorker()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.on_finished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def _add_kits(self) -> None:
        """Iterate over the kits database table and add the kits to the UI."""
        # Get copy of installed kits.
        installed_kits = DATA.modo_kits.copy()
        database_kits = get_kits()

        for kit_name, kit_data in database_kits.items():
            # Generate a collapsable container.
            kit_container = FoldContainer(name=kit_data.label, version=kit_data.version)
            kit_widget = KitWidget(kit_data)
            kit_container.set_content(kit_widget)
            # Get the author data for the kit,
            author_data = {'author_data': get_author(kit_data.author)}
            author_request = TabRequest(type=KEYS.AUTHORS, name=kit_data.author, show=True, kwargs=author_data)
            # Link the author request signal to the kit widget
            kit_widget.author_clicked.connect(lambda author: self.author_request.emit(author_request))
            self.kits.append(kit_container)
            self.kits_layout.addWidget(kit_container)
            # If the kit is installed, remove it from the installed kits list.
            if kit_name in installed_kits:
                del installed_kits[kit_name]

        # Add the installed kits that are not in the database.
        for kit_name, kit_info in installed_kits.items():
            kit_container = FoldContainer(name=kit_name, version=kit_info.version)
            kit_info_widget = KitInfoWidget(kit_info)
            kit_container.set_content(kit_info_widget)
            self.local_kits.append(kit_container)
            self.kits_layout.addWidget(kit_container)

    def on_finished(self) -> None:
        """Handles the completion of the database worker."""
        self.thread.quit()
        self.thread.wait()
        self._add_kits()

    def on_error(self, error: str) -> None:
        """Handles the error from the database worker.

        Args:
            error: The error raised by the worker.
        """
        print(f"Error: {error}")
        self.thread.quit()
        self.thread.wait()


class AuthorTab(QScrollArea):
    """Class to display the author information in the main UI."""

    def __init__(self, author_data: AuthorData, parent: QWidget = None) -> None:
        """Scroll area that populates with incoming author information.

        Args:
            author_data: Data for the given author.
            parent: Widget to set as parent.
        """
        super(AuthorTab, self).__init__(parent)
        self.data = author_data
        self.setObjectName(self.data.name)
        self.avatar_pix: QPixmap = None
        self._build_ui()
        self._add_links()
        self._add_kits()
        self._sync_avatar()

    def _build_ui(self) -> None:
        """Builds the UI for the author tab."""
        self.base_widget = QWidget()
        self.base_layout = QVBoxLayout()
        self.base_layout.setAlignment(Qt.AlignCenter)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setAlignment(Qt.AlignTop)

        self.base_widget.setLayout(self.base_layout)
        self.setWidgetResizable(True)
        self.setWidget(self.base_widget)

        # Load avatar if it exists.
        self.avatar = Paths.AVATAR
        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(120, 100)
        self.avatar_pix = QPixmap(self.avatar.as_posix())
        # Load avatar image into the label.
        self._add_avatar()
        self.base_layout.addWidget(self.avatar_lbl, alignment=Qt.AlignCenter)
        # Add author name
        self.author_lbl = QLabel(self.data.name)
        self.base_layout.addWidget(self.author_lbl, alignment=Qt.AlignCenter)
        # Add links layout.
        self.links_layout = QHBoxLayout()
        self.base_layout.addLayout(self.links_layout)

    def _sync_avatar(self) -> None:
        """Syncs the local avatar with the database avatar."""
        # Fetch the avatar from the database and save it locally.
        self.thread = QThread()
        self.worker = AvatarWorker(self.data.name)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.on_avatar_finished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_avatar_finished(self, avatar: QPixmap) -> None:
        """Sets the avatar pixmap to the label.

        Args:
            avatar: The avatar pixmap to set.
        """
        self.thread.quit()
        self.thread.wait()
        self.avatar_pix = avatar
        self._add_avatar()

    def _add_avatar(self) -> None:
        """Adds the author's avatar to the author tab."""
        avatar_pix = self.avatar_pix.scaledToHeight(100)
        self.avatar_lbl.setPixmap(avatar_pix)

    def _add_links(self) -> None:
        """Adds all links to the author tab as clickable."""
        for text, url in self.data.links.items():
            link_lbl = QLabel()
            link_lbl.setText(Text.lbl_link.format(text=text, link=url))
            link_lbl.setOpenExternalLinks(True)
            self.links_layout.addWidget(link_lbl)

    def _add_kits(self) -> None:
        """Iterate over the author's kits and add them to the UI."""
        for authors_kit in get_author_kits(self.data.name):
            # Add fold-able element for each kit
            folder = FoldContainer(name=authors_kit.label, version=authors_kit.version)
            # Since we are on the authors tab, don't show the author on each kit.
            kit_widget = KitWidget(authors_kit, show_author=False)
            folder.set_content(kit_widget)
            self.base_layout.addWidget(folder)


class InfoTab(QWidget):
    """Class to display the help information in the main UI."""

    def __init__(self) -> None:
        """Initialization of the Help Tab."""
        super(InfoTab, self).__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        """Builds the UI for the help tab."""
        self.base_layout = QVBoxLayout()
        self.base_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.base_layout)

        # Add about text
        self.about = QLabel()
        self.about.setObjectName("mkc-about")
        self.about.setText(Text.info_block)
        # Wrap the text
        self.about.setWordWrap(True)

        self.base_layout.addWidget(self.about)


# Define a simple type variable for the tab map.
TAB = TypeVar('TAB', KitsTab, AuthorTab, InfoTab)

# Map to hold all tabs for the main window.
tab_map: Dict[str, Type[TAB]] = {
    KEYS.KITS: KitsTab,
    KEYS.AUTHORS: AuthorTab,
    KEYS.INFO: InfoTab
}
