from widgets.kwidgets import KStatusBar
from core.labels import Label

class KRootStatusBar(KStatusBar):
    def __init__(self, parent=None, text:str|Label|None=None):
        KStatusBar.__init__(self, parent, text)