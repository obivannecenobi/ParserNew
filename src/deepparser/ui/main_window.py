from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QProgressBar,
    QStatusBar,
)
from .starfield import StarfieldWidget

BASE_DIR = Path(__file__).resolve().parents[2]
RES_DIR = BASE_DIR / "res"
LOGO_PATH = RES_DIR / "logo.jpg"


class MainWindow(QMainWindow):
    """Minimal main window implementing a subset of the P0 roadmap."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("DeepParser")
        if LOGO_PATH.exists():
            self.setWindowIcon(QIcon(str(LOGO_PATH)))

        self._create_actions()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_central_widget()
        self._create_status_bar()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _create_actions(self) -> None:
        self.save_docx_action = QAction("Export DOCX", self)
        self.save_docx_action.triggered.connect(self.export_docx)
        self.toggle_starfield_action = QAction("Starfield", self, checkable=True)

    def _create_toolbar(self) -> None:
        toolbar = QToolBar("Navigation", self)
        self.addToolBar(toolbar)

        self.prev_btn = QPushButton("Prev")
        self.next_btn = QPushButton("Next")
        toolbar.addWidget(self.prev_btn)
        toolbar.addWidget(self.next_btn)

        self.chapter_box = QComboBox()
        self.chapter_box.setEditable(True)
        toolbar.addWidget(self.chapter_box)

        self.model_box = QComboBox()
        self.model_box.addItems(["Gemini", "Qwen"])
        toolbar.addWidget(self.model_box)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        toolbar.addWidget(self.progress_bar)

        self.progress_label = QLabel("0/0")
        toolbar.addWidget(self.progress_label)

        toolbar.addAction(self.save_docx_action)

    def _create_central_widget(self) -> None:
        central = QWidget(self)
        layout = QVBoxLayout(central)

        # titles
        title_layout = QHBoxLayout()
        self.original_title = QLabel("Original Title")
        self.translation_title = QLineEdit()
        self.translation_title.setPlaceholderText("Translation title")
        title_layout.addWidget(self.original_title)
        title_layout.addWidget(self.translation_title)
        layout.addLayout(title_layout)

        # editors
        editors_layout = QHBoxLayout()
        self.original_editor = QTextEdit()
        self.original_editor.setReadOnly(True)
        self.translation_editor = QTextEdit()
        editors_layout.addWidget(self.original_editor)
        editors_layout.addWidget(self.translation_editor)
        layout.addLayout(editors_layout)

        self.mini_prompt = QLineEdit()
        self.mini_prompt.setPlaceholderText("Mini prompt")
        layout.addWidget(self.mini_prompt)

        self.starfield = StarfieldWidget(central)
        self.starfield.toggle(False)
        self.setCentralWidget(self.starfield)
        self.toggle_starfield_action.toggled.connect(self.starfield.toggle)

    def _create_menu_bar(self) -> None:
        menu = self.menuBar().addMenu("View")
        menu.addAction(self.toggle_starfield_action)

    def _create_status_bar(self) -> None:
        status = QStatusBar(self)
        self.setStatusBar(status)
        self.project_label = QLabel("Active: none")
        status.addPermanentWidget(self.project_label)
        status.showMessage("Ready")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def export_docx(self) -> None:
        """Export the translation to a DOCX file.

        Currently this is a stub that simply writes the translation text to a
        plain text file with a ``.docx`` extension so that the action can be
        tested without additional dependencies.
        """
        text = self.translation_editor.toPlainText()
        if not text:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Chapter", "chapter.docx", "DOCX Files (*.docx)"
        )
        if not filename:
            return
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(text)
