from PySide6.QtWidgets import QWidgetAction
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal
from widgets.kmixins import KTextMixin, KThemeMixin
from core.labels import Label

class KAction(QAction, KTextMixin):
    def __init__(self, parent=None, text:Label|str|None=None):
        if parent:
            QAction.__init__(self, parent)
        else:
            QAction.__init__(self)
        KTextMixin.__init__(self, text)
        if text: self.updateText()

class KWidgetAction(QWidgetAction, KTextMixin, KThemeMixin):
    def __init__(self, parent=None, text:str|Label|None=None, style:str|None=None):
        self._parent = parent
        if parent:
            QWidgetAction.__init__(self, parent)
        else:
            QWidgetAction.__init__(self)
        KTextMixin.__init__(self, text)
        KThemeMixin.__init__(self, style)
        if text: self.updateText()


class KCheckableAction(KAction):
    checked_changed = Signal(bool)
    def __init__(self, parent, text:Label|str|None=None):
        KAction.__init__(self, parent, text)
        self._checked = False
        self._checkable = True
        self._disabled = False
    
    def setChecked(self, checked: bool):
        if self._checked != checked:
            self._checked = checked
            self.checked_changed.emit(checked)
            self.changed.emit()
        

    def setCheckable(self, checkable: bool):
        if self._checkable != checkable:
            self._checkable = checkable
            self.changed.emit()
    
    def setDisabled(self, disabled: bool):
        if self._disabled != disabled:
            self._disabled = disabled
            self.changed.emit()
    
    def isCheckable(self):
        return self._checkable

    def isChecked(self):
        return self._checked
    
    def isDisabled(self):
        return self._disabled