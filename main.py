import signal
import sys
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QWidget
from AppKit import (
    NSApp,
    NSVisualEffectView,
    NSVisualEffectMaterialHUDWindow,
    NSVisualEffectBlendingModeBehindWindow,
    NSWindowBelow,
    NSColor
)

dimensions = [500, 300]

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 80);
                border-radius: 12px;
            }
        """)

        self.resize(*dimensions)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.drag_pos = QPoint()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(
                event.globalPosition().toPoint()
                - self.drag_pos
            )


app = QApplication(sys.argv)

signal.signal(signal.SIGINT, signal.SIG_DFL)

window = Window()
window.show()

ns_window = NSApp.windows()[0]

ns_window.setOpaque_(False)
ns_window.setBackgroundColor_(NSColor.clearColor())

effect = NSVisualEffectView.alloc().initWithFrame_(
    ns_window.contentView().bounds()
)

effect.setAutoresizingMask_(1 << 1 | 1 << 4)

effect.setMaterial_(NSVisualEffectMaterialHUDWindow)
effect.setBlendingMode_(NSVisualEffectBlendingModeBehindWindow)
effect.setState_(1)

effect.setWantsLayer_(True)
effect.layer().setCornerRadius_(12.0)
effect.layer().setMasksToBounds_(True)

ns_window.contentView().addSubview_positioned_relativeTo_(
    effect,
    NSWindowBelow,
    None
)

sys.exit(app.exec())