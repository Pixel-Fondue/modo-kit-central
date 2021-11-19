# python

resources = None
authors = None

# TODO: Enable location based text for all regions not just english
# import locale
# locale.getdefaultlocale()[0] == "en_US"


class Text:
    title = "Community Hub"
    author = "Author: <a href='{}' style='color: white'>{}</a>"
    lbl_link = "<a href='{link}' style='color: white'>{text}</a>"


class KEYS:
    videos = "videos"
    kits = "kits"
    social = "social"
    authors = "authors"


CSS = """
QListWidget,
QListWidget::item:selected {
    background-color: rgb(70, 70, 70);
}
#description {
    background-color: rgb(65, 65, 65);
    color: rgb(220, 220, 220);
}
"""