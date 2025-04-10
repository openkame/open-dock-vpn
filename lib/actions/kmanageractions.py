from core.actions import KAction
from core.manager import states
from core.labels import Label

class KQuitAppAction(KAction):
    def __init__(self, parent):
        super().__init__(parent, Label.UI_MAIN_LABEL_QUIT_APP)
        self.triggered.connect(self._on_triggered)

    def _on_triggered(self):
        if self.isEnabled():
            states.emit_quit_app_request()

class KOpenLogConsoleAction(KAction):
    def __init__(self, parent):
        super().__init__(parent, Label.UI_MAIN_LABEL_CONSOLE_LOGS)
        self.triggered.connect(self._on_triggered)
    
    def _on_triggered(self):
        if self.isEnabled():
            states.emit_open_logs_request()

class KOpenProfilesManagerAction(KAction):
    def __init__(self, parent):
        super().__init__(parent, Label.UI_MAIN_LABEL_MANAGE_PROFILES)
        self.triggered.connect(self._on_triggered)
    
    def _on_triggered(self):
        if self.isEnabled():
            states.emit_open_profiles_manager_request()

class KOpenAddClientAction(KAction):
    def __init__(self, parent):
        super().__init__(parent, Label.UI_MAIN_LABEL_ADD_CLIENT)
        self.triggered.connect(self._on_triggered)
    
    def _on_triggered(self):
        if self.isEnabled():
            states.emit_open_add_client_request()

class KToggleTooltipsAction(KAction):
    def __init__(self, parent):
        super().__init__(parent, Label.UI_MAIN_LABEL_TOOLTIP_TOGGLER)
        self.triggered.connect(self._on_triggered)
    
    def _on_triggered(self):
        """ Désactivé, A Coder !"""
        print('To dev')
        # if self.isEnabled():

class KSwitchViewAction(KAction):
    def __init__(self, parent=None):
        super().__init__(parent, Label.UI_MAIN_LABEL_VIEW_SWITCHER)
        self.triggered.connect(self._on_triggered)
    
    def _on_triggered(self):
        if self.isEnabled():
            states.emit_switch_view_request()

class KHideViewAction(KAction):
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent, "❌")
        self.triggered.connect(self._on_triggered)
    
    def _on_triggered(self):
        if self.isEnabled():
            states.emit_hide_view_requested(self._parent.objectName)

    