from __future__ import annotations

from typing import Any, TYPE_CHECKING

import numpy as np

from qtpy import QtWidgets as QtW
from qtpy.QtCore import Qt

if TYPE_CHECKING:
    from chimerax.core.session import Session

class ChimeraX:
    def __init__(self, session):
        self._session = session
    
    @property
    def session(self) -> Session:
        return self._session
    
    @property
    def models(self):
        return self.session.models.list()
    
    def log(self, text: str) -> None:
        from chimerax.core.commands import run
        run(self.session, f"log html {text}")
        return None
    
    @property
    def _main_window(self) -> QtW.QMainWindow:
        return self.session.ui.main_window
    
    def add_dock_widget(self, widget: QtW.QWidget, name: str = ""):
        name = name or widget.objectName()
        dock = QtW.QDockWidget(name)
        dock.setWidget(widget)
        self._main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        return dock

    def add_volume(
        self,
        data: np.ndarray,
        *,
        name: str | None = None,
    ):
        from chimerax.map_data import ArrayGridData
        from chimerax.map import volume_from_grid_data
        grid = ArrayGridData(data, name=name or "Volume")
        return volume_from_grid_data(grid, self.session)
