from __future__ import annotations

from typing import Any, TYPE_CHECKING, Sequence
import weakref
import numpy as np

from qtpy import QtWidgets as QtW
from qtpy.QtCore import Qt

if TYPE_CHECKING:
    from chimerax.core.session import Session

class ChimeraX:
    _session: Session | None = None
    _docked_widgets: weakref.WeakValueDictionary[str, QtW.QWidget]
    
    def __init__(self, session):
        self.__class__._session = session
        self._docked_widgets = weakref.WeakValueDictionary()
    
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
            qwidget = widget.native
        else:
            qwidget = widget
            name = name or widget.objectName()
        dock = QtW.QDockWidget(name)
        dock.setWidget(qwidget)
        self._main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        self._docked_widgets[name] = widget
        return dock
    
    def reset_choices(self, *_) -> None:
        for dock in self._docked_widgets.values():
            if hasattr(dock, "reset_choices"):
                dock.reset_choices()
        return None

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

    def open(self, path: str, name: str | None = None):
        from chimerax.map import open_map
        open_map(self.session, path, name=name)
        