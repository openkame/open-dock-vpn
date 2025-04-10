from PySide6.QtGui import Qt, QMouseEvent

from widgets.kwidgets import KWidget, KLabel
from widgets.klayouts import KHBoxLayout
from core.labels import Label

# TODO essayer d'ajouter des kmenus aussi

class KHeader(KWidget):
    def __init__(self, parent:KWidget, title:Label|str, left_buttons=None, right_buttons=None):
        self._parent = parent
        self._title = title
        super().__init__(parent)
        self.setFixedHeight(60)
        self._drag_position = None
        self.header_layout = KHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)       

        # ➖ Left buttons
        if left_buttons:
            for btn in left_buttons:
                self.header_layout.addWidget(btn)

        # 🏷️ Title (centered)
        self._title = KLabel(self._title)
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout.addWidget(self._title, 1)

        # ➕ Right buttons
        if right_buttons:
            for btn in right_buttons:
                self.header_layout.addWidget(btn)

        

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self._parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self._drag_position:
            self._parent.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_position = None