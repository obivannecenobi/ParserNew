from __future__ import annotations

import os
import sys
from typing import Optional

from PyQt6.QtWidgets import QApplication

from .ui.main_window import MainWindow


def run(argv: Optional[list[str]] = None) -> int:
    """Entry point for running the DeepParser application.

    Parameters
    ----------
    argv:
        Optional list of arguments to pass to ``QApplication``. When ``None``
        the arguments from ``sys.argv`` are used.
    """
    if argv is None:
        argv = sys.argv

    # Allow running in headless environments by falling back to the
    # ``offscreen`` Qt platform if no display is detected.
    if not os.environ.get("DISPLAY") and os.name != "nt":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    app = QApplication(argv)
    window = MainWindow()
    window.show()
    return app.exec()
