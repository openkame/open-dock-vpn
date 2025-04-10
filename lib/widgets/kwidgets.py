from PySide6.QtWidgets import (
    QMenuBar, QWidget, QStatusBar, QSystemTrayIcon,
    QLabel, QCheckBox, QToolButton, QComboBox, QMenu, 
    QTabWidget, QLineEdit, QTextEdit, QListWidget,
    QFileDialog, QScrollArea
)
from PySide6.QtCore import Qt
from widgets.kmixins import KThemeMixin, KTextMixin, KTitleMixin, KWindowTitleMixin, KStatusMixin
from core.actions import KAction, KCheckableAction
from core.env import APP_DEFAULT_STYLE
from core.manager import tr, states
from core.labels import Label


class KWidget(QWidget, KThemeMixin, KWindowTitleMixin):
    """ 🏷️ QWidget customisé avec thème et traduction dynamiques """
    def __init__(self, parent=None, text:str|Label|None=None, style:str|None=None):
        if parent:
            QWidget.__init__(self, parent)
        else:
            QWidget.__init__(self)
        if style:
            KThemeMixin.__init__(self, style_name=style)
        else:
            KThemeMixin.__init__(self)
        KWindowTitleMixin.__init__(self, text)
        if text: self.updateText()

    def moveEvent(self, event):
        """ 🔥 Déclenche un signal quand la fenêtre est déplacée """
        #state_manager.emit_window_move(self.pos())
        super().moveEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KMenuBar(QMenuBar, KThemeMixin):
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        KThemeMixin.__init__(self)
        self._drag_position = None
        self._dragging = False

    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # ⛔️ Si clique sur un QAction, pas de drag
            if self.actionAt(event.pos()):
                self._drag_position = None
                self._dragging = False
            else:
                self._drag_position = event.globalPosition().toPoint() - self._parent.frameGeometry().topLeft()
                self._dragging = False
        super().mousePressEvent(event)  # 👈 On laisse le menu bar gérer l'event aussi

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_position:
            self._parent.move(event.globalPosition().toPoint() - self._drag_position)
            self._dragging = True  # ✅ Drag confirmé
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self._dragging:
            super().mouseReleaseEvent(event)  # 🎯 C'était juste un clic
        self._drag_position = None
        self._dragging = False

class KStatusBar(QStatusBar, KThemeMixin, KStatusMixin):
    def __init__(self, parent=None, text:str|Label|None=None, style:str|None="status_bar"):
        if parent:
            QStatusBar.__init__(self, parent)
        else:
            QStatusBar.__init__(self)
        KThemeMixin.__init__(self, style)
        KStatusMixin.__init__(self, text)
        if text: self.updateText()
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KSystemTray(QSystemTrayIcon):
    def __init__(self, parent):
        QSystemTrayIcon.__init__(self, parent)

class KLabel(QLabel, KThemeMixin, KTextMixin):
    """ 🏷️ QLabel customisé avec traduction dynamique """
    def __init__(self, text:str|Label|None=None, style:str|None=None):
        QLabel.__init__(self)
        if style:
            KThemeMixin.__init__(self, style_name=style)
        else:
            KThemeMixin.__init__(self)
        KTextMixin.__init__(self, text)
        if text: self.updateText()
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KCheckBox(QCheckBox, KThemeMixin):
    """ ✅ QCheckBox connectée à une KAction """
    def __init__(self, action: KCheckableAction=None, parent=None, style:str|None="default_checkbox"):
        QCheckBox.__init__(self, parent)
        KThemeMixin.__init__(self, style_name=style)
        self._action = None
        if action: 
            action.setParent(self)
            self.setAction(action)

    def setAction(self, action: KCheckableAction):
        """ 🔗 Associe une action à la checkbox """
        if self._action:
            self.toggled.disconnect(action.setChecked)
            self._action.deleteLater()
        self._action = action
        
        self._on_action_changed()
        # 🔁 Sync état CheckBox → Action
        self.toggled.connect(self._action.setChecked)
        # 🔁 Sync Action → CheckBox
        self._action.changed.connect(self._on_action_changed)
    
    def _on_action_changed(self):
        """ 🔁 Met à jour le texte et l’état si l’action change """
        self.setText(self._action.text())
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KComboBox(QComboBox, KThemeMixin):
    def __init__(self):
        QComboBox.__init__(self)
        KThemeMixin.__init__(self, style_name="default_combo")
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KListWidget(QListWidget, KThemeMixin):
    def __init__(self, style:str|None="default_list"):
        QListWidget.__init__(self)
        KThemeMixin.__init__(self, style_name=style)
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KButton(QToolButton, KThemeMixin, KTextMixin):
    def __init__(self, text:str|Label|None=None, style:str|None="default_button", action:KAction|None=None):
        QToolButton.__init__(self)
        if action:
            action.setParent(self)
            self.setDefaultAction(action)

        KThemeMixin.__init__(self, style_name=style)
        KTextMixin.__init__(self, text)
        if text: self.updateText()
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KTabWidget(QTabWidget, KThemeMixin):
    """ 🏷️ QLabel customisé avec traduction dynamique """
    def __init__(self):
        QTabWidget.__init__(self)
        KThemeMixin.__init__(self, style_name="tabber")
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KLineEdit(QLineEdit, KThemeMixin):
    """ 🏷️ QLabel customisé avec traduction dynamique """
    def __init__(self):
        QLineEdit.__init__(self)
        KThemeMixin.__init__(self)

    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KTextEdit(QTextEdit, KThemeMixin):
    """ 🏷️ QLabel customisé avec traduction dynamique """
    def __init__(self):
        QTextEdit.__init__(self)
        KThemeMixin.__init__(self)
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)
        

class KFileDialog(QFileDialog, KThemeMixin):
    def __init__(self):
        QFileDialog.__init__(self)
        KThemeMixin.__init__(self)
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)
    
    @staticmethod
    def getOpenFileName(parent=None, title=None, filename=None, filetypes=None, selected_filter=None):
        """📁 Wrapper sur QFileDialog.getOpenFileName avec support des traductions formatées"""
        def _parse_tr(data):
            if isinstance(data, (list, tuple)):
                key = data[0]
                kwargs = data[1] if len(data) > 1 and isinstance(data[1], dict) else {}
                return tr(key, **kwargs)
            elif isinstance(data, str):
                return tr(data)
            else:
                return ""

        # 🎯 Traduction conditionnelle
        caption = _parse_tr(title)
        dir_path = _parse_tr(filename)
        filters = _parse_tr(filetypes)
        sel_filter = _parse_tr(selected_filter)

        return QFileDialog.getOpenFileName(parent, caption, dir_path, filters, sel_filter)

class KMenu(QMenu, KThemeMixin, KTitleMixin):
    def __init__(self, parent, text:str|Label|None=None, style:str|None="default"):
        super().__init__(parent)
        KThemeMixin.__init__(self, style)
        KTitleMixin.__init__(self, text)
        if text: self.updateText()
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)

class KScrollArea(QScrollArea, KThemeMixin):
    def __init__(self, parent:QWidget|None=None, style:str|None="default_scrollarea" ):
        if parent:
            QScrollArea.__init__(self, parent)
        else:
            QScrollArea.__init__(self)
        KThemeMixin.__init__(self, style)
    
    def showEvent(self, event):
        super().showEvent(event)
        states.emit_widget_show(self)