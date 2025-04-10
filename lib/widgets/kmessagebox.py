from enum import Enum
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys


from widgets.kwidgets import KWidget, KLabel, KButton
from widgets.kheader import KHeader
from widgets.kdialog import KDialog

from core.labels import Label

class KMessageBoxButton(Enum):
    Ok = (Label.BUTTONS_OK, "message_box_ok_button")
    Cancel = (Label.BUTTONS_CANCEL, "message_box_cancel_button")
    Yes = (Label.BUTTONS_YES, "message_box_confirm_button")
    No = (Label.BUTTONS_NO, "message_box_cancel_button")
    Retry = (Label.BUTTONS_RETRY, "message_box_retry_button")
    Abort = (Label.BUTTONS_ABORT, "message_box_danger_button")
    Ignore = (Label.BUTTONS_IGNORE, "message_box_default_button")

    def __init__(self, key: str, style: str = "message_box_default_button"):
        self._key = key
        self._style = style

    @property
    def key(self) -> str:
        return self._key

    @property
    def style(self) -> str:
        return self._style

class KMessageBox(KDialog):
    def __init__(
        self,
        parent=None,
        title: Label | None = None,
        text: Label | None = None,
        icon=None,
        buttons: list = [KMessageBoxButton.Ok]
    ):
        super().__init__(parent)

        self.central_widget = KWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.installHeader(KHeader(self, title=title))

        # ───── Message texte
        text_label = KLabel(text)
        text_label.setWordWrap(False)

        if icon:
            icon_layout = QHBoxLayout()
            icon_label = KLabel()
            icon_label.setPixmap(icon.pixmap(32, 32))
            icon_layout.addWidget(icon_label, alignment=Qt.AlignTop)
            icon_layout.addWidget(text_label, 1)
            self.main_layout.addLayout(icon_layout)
        else:
            self.main_layout.addWidget(text_label)

        # ───── Boutons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self._buttons = {}

        for btn in buttons:
            if isinstance(btn, KMessageBoxButton):
                kbtn = KButton({"key": btn.key}, style=btn.style)
                self._buttons[kbtn] = btn
            else:
                kbtn = KButton(btn)
                self._buttons[kbtn] = btn
            kbtn.clicked.connect(self._handle_button)
            button_layout.addWidget(kbtn)

        self.main_layout.addLayout(button_layout)
        self._clicked_button = None

    def _handle_button(self):
        sender = self.sender()
        self._clicked_button = self._buttons.get(sender)
        self.accept()

    @staticmethod
    def information(parent, title, text, buttons=[KMessageBoxButton.Ok]):
        box = KMessageBox(
            parent,
            title,
            text,
            icon=QIcon.fromTheme("dialog-information"),
            buttons=buttons
        )
        box.exec()
        return box._clicked_button

    @staticmethod
    def warning(parent, title, text, buttons=[KMessageBoxButton.Ok]):
        box = KMessageBox(
            parent,
            title,
            text,
            icon=QIcon.fromTheme("dialog-warning"),
            buttons=buttons
        )
        box.exec()
        return box._clicked_button

    @staticmethod
    def question(parent, title, text, buttons=[KMessageBoxButton.Ok, KMessageBoxButton.No]):
        box = KMessageBox(
            parent,
            title,
            text,
            icon=QIcon.fromTheme("dialog-question"),
            buttons=buttons
        )
        box.exec()
        return box._clicked_button


# Test standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    result = KMessageBox.question(
        None,
        title={"key": "confirm.title"},
        text={"key": "confirm.exit"}
    )
    print("Clicked:", result)
    if result == KMessageBoxButton.Yes:
        print("User said YES")
    elif result == KMessageBoxButton.No:
        print("User said NO")
    sys.exit(0)