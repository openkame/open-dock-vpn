from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QWidget


class KHBoxLayout(QHBoxLayout):
    def __init__(self, parent:QWidget|None=None):
        self._parent = parent
        if self._parent:
            QHBoxLayout.__init__(self, parent)
        else:
            QHBoxLayout.__init__(self)

class KVBoxLayout(QVBoxLayout):
    def __init__(self, parent:QWidget|None=None):
        self._parent = parent
        if parent:
            QVBoxLayout.__init__(self, parent)
        else:
            QVBoxLayout.__init__(self)

class KGridLayout(QGridLayout):
    def __init__(self, parent:QWidget|None=None):
        self._parent = parent
        if parent:
            QGridLayout.__init__(self, parent)
        else:
            QGridLayout.__init__(self)