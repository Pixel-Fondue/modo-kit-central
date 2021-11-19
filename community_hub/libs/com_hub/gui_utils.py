try:
    from PySide2.QtCore import Qt, QTimer
    from PySide2.QtGui import QCursor, QPixmap, QColor
    from PySide2.QtWidgets import (QLabel, QDesktopWidget, QMainWindow, QApplication, QTabWidget,
                                   QPushButton, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QScrollArea)
except ImportError:
    from PySide.QtCore import Qt, QTimer
    from PySide.QtGui import (QPixmap, QLabel, QDesktopWidget, QMainWindow, QCursor, QColor,
                              QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget,
                              QListWidget, QListWidgetItem, QScrollArea)

from com_hub.utils import load_resource
from com_hub.prefs import KEYS
from com_hub.widgets import widget_map, KitTab


def build_tab(tab_type):
    # Get tab resource
    tab_data = load_resource(tab_type)
    if not tab_data:
        return
    # Get the widget by class type
    widget_class = widget_map.get(tab_type)

    if tab_type == KEYS.kits:
        tab_list = KitTab(tab_data)
    else:
        tab_list = QListWidget()

        for name, info in tab_data.items():
            # Create Widget for info
            widget = widget_class(name, info)
            # Create QList widget for item
            item = QListWidgetItem()
            # Add the QListWidgetItem to the QListView
            tab_list.addItem(item)
            # Set the widget to the QListWidgetItem
            tab_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    return tab_list
