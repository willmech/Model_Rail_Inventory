from __future__ import annotations

import sys
from typing import List

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableView,
    QLabel,
)

from rail_inventory.database.locomotives_dao import get_all_locomotives
from rail_inventory.models.locomotive import Locomotive


class LocomotivesTableModel(QAbstractTableModel):
    HEADERS = ["Road", "Number", "Model Mfr", "Prototype Mfr", "Control", "Decoder ID", "HP"]

    def __init__(self, rows: List[Locomotive]) -> None:
        super().__init__()
        self._rows = rows

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # type: ignore[override]
        return len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # type: ignore[override]
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.HEADERS[section]
        return str(section + 1)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        loco = self._rows[index.row()]
        col = index.column()

        values = [
            loco.road_name,
            loco.locomotive_number,
            loco.model_manufacturer,
            loco.prototype_manufacturer,
            loco.control_type,
            loco.decoder_id,
            loco.horsepower,
        ]
        v = values[col]
        return "" if v is None else str(v)

    def set_rows(self, rows: List[Locomotive]) -> None:
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rail Inventory")
        self.resize(1100, 650)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # --- Locomotives tab ---
        locomotives_tab = QWidget()
        tabs.addTab(locomotives_tab, "Locomotives")

        loco_layout = QVBoxLayout(locomotives_tab)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_locomotives)  # type: ignore[attr-defined]
        loco_layout.addWidget(self.refresh_btn)

        self.table = QTableView()
        self.model = LocomotivesTableModel([])
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        loco_layout.addWidget(self.table)

        # --- Rolling Stock tab placeholder ---
        rolling_stock_tab = QWidget()
        rs_layout = QVBoxLayout(rolling_stock_tab)
        rs_layout.addWidget(QLabel("Rolling Stock module coming later."))
        tabs.addTab(rolling_stock_tab, "Rolling Stock")

        self.load_locomotives()

    def load_locomotives(self) -> None:
        rows = get_all_locomotives()
        self.model.set_rows(rows)


def run_qt_app() -> None:
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
