from PySide6.QtWidgets import QFrame, QWidget
from widgets.kmixins import KThemeMixin

from core.manager import states

class KFrame(QFrame, KThemeMixin):
    def __init__(self, parent:QWidget|None=None, style:str="default_frame"):
        self._parent = parent
        self._style = style
        if parent:
            QFrame.__init__(self, parent=self._parent)
        else:
            QFrame.__init__(self)
        KThemeMixin.__init__(self, self._style)
    
    def showEvent(self, event):
        states.emit_widget_show(self)
        return super().showEvent(event)