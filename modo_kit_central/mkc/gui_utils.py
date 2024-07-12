from typing import Union

from PySide6.QtWidgets import QListWidget, QListWidgetItem

from .utils import load_resource
from .widgets import widget_tabs, widget_map


# def build_tab(tab_type: str) -> Union[QListWidget, None]:
#     """Generates a tab widget for the kit central.
#
#     Args:
#         tab_type: The type of tab to generate.
#
#     Returns:
#         The tab widget if the resource exists, else None.
#     """
#     # Get tab resource
#     tab_data = load_resource(tab_type)
#     if not tab_data:
#         return
#     # Get the widget by class type
#     widget_class = widget_map.get(tab_type)
#     tab_class = widget_tabs.get(tab_type)
#
#     if tab_class:
#         return tab_class()
#     else:
#         tab_list = QListWidget()
#         tab_list.setObjectName(tab_type)
#
#         for name, info in tab_data.items():
#             # Create Widget for info
#             widget = widget_class(name, info)
#             # Create QList widget for item
#             item = QListWidgetItem()
#             # Add the QListWidgetItem to the QListView
#             tab_list.addItem(item)
#             # Set the widget to the QListWidgetItem
#             tab_list.setItemWidget(item, widget)
#             item.setSizeHint(widget.sizeHint())
#
#     return tab_list
