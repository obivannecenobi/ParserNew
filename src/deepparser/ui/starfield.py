from __future__ import annotations

import random
from typing import Optional

from PyQt6.QtCore import QPointF, QTimer, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget, QVBoxLayout


class StarfieldWidget(QWidget):
    """Widget that draws a simple animated starfield behind its child.

    The animation is intentionally lightweight and used purely for decoration.
    It can be enabled or disabled via :py:meth:`toggle` and the speed adjusted
    via :py:meth:`set_speed`.
    """

    def __init__(self, child: QWidget, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._child = child
        self._stars: list[QPointF] = []
        self._speed = 0.5
        self._enabled = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(child)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)

    # ------------------------------------------------------------------
    # Control API
    # ------------------------------------------------------------------
    def toggle(self, enabled: bool) -> None:
        """Enable or disable the starfield animation."""
        self._enabled = enabled
        if enabled:
            self._init_stars()
            self._timer.start(33)
        else:
            self._timer.stop()
            self._stars.clear()
            self.update()

    def set_speed(self, value: float) -> None:
        """Set animation speed in arbitrary units."""
        self._speed = value

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _init_stars(self) -> None:
        self._stars = [
            QPointF(random.random() * self.width(), random.random() * self.height())
            for _ in range(100)
        ]

    def _advance(self) -> None:
        height = self.height()
        for i, pt in enumerate(self._stars):
            y = pt.y() + self._speed
            if y > height:
                y = 0
            self._stars[i] = QPointF(pt.x(), y)
        self.update()

    # ------------------------------------------------------------------
    # Qt events
    # ------------------------------------------------------------------
    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        if self._enabled:
            self._init_stars()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        if not self._enabled:
            return
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)
        painter.setPen(Qt.white)
        for pt in self._stars:
            painter.drawPoint(int(pt.x()), int(pt.y()))
        painter.end()
        # Child widgets paint themselves as usual.
