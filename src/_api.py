from __future__ import annotations

from typing import Any, TYPE_CHECKING, Sequence

import numpy as np

from qtpy import QtWidgets as QtW
from qtpy.QtCore import Qt

if TYPE_CHECKING:
    from chimerax.core.session import Session

class ChimeraX:
    _session: Session | None = None

    def __init__(self, session):
        self.__class__._session = session
    
    @property
    def session(self) -> Session:
        """Get the ChimeraX session"""
        return self._session
    
    @property
    def models(self):
        return self.session.models.list()
    
    def log(self, text: str) -> None:
        """Print a message to the ChimeraX log."""
        from chimerax.core.commands import run
        run(self.session, f"log html {text}")
        return None
    
    @property
    def _main_window(self) -> QtW.QMainWindow:
        return self.session.ui.main_window
    
    def add_dock_widget(self, widget: QtW.QWidget, *, name: str = ""):
        """Add a widget to the ChimeraX dock"""
        if hasattr(widget, "native"):
            name = name or getattr(widget, "name", None)
            widget = widget.native
            
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
        scale: float | Sequence[float] = 1.,
    ):
        from chimerax.map_data import ArrayGridData
        from ._utils import add_grid
        name = name or "Volume"
        if hasattr(scale, "__iter__"):
            step = tuple(step)
        else:
            step = (scale, scale, scale)
        grid = ArrayGridData(data, name=name, step=step)
        return add_grid(grid, self.session)
