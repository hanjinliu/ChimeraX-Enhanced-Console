from __future__ import annotations

from typing import NewType, TYPE_CHECKING, Any
import numpy as np
from qtpy import QtWidgets as QtW
from magicgui import register_type
from magicgui.widgets import Widget, FunctionGui
from magicgui.widgets._bases import CategoricalWidget

from chimerax.core.models import Model
from chimerax.map.volume import Volume
from chimerax.map_data import ArrayGridData

from ._utils import add_grid

if TYPE_CHECKING:
    from chimerax.core.session import Session

VolumeData = NewType("VolumeData", np.ndarray)

def get_session() -> Session:
    from ._api import ChimeraX
    return ChimeraX._session


def get_volume_data(widget: CategoricalWidget) -> list[tuple[str, np.ndarray]]:
    """Get the list of available tables and the names."""
    models = get_session().models.list()
    return [(m.name, m.matrix()) for m in models if isinstance(m, Volume)]


def add_volume_data_to_chimerax(gui: FunctionGui, result: Any, return_type: type) -> None:
    session = get_session()
    name = gui.result_name
    if isinstance(result, np.ndarray):
        grid = ArrayGridData(result, name=name)
    else:
        raise NotImplementedError()
    models: dict[str, Model] = {
        model.name: model for model in session.models.list() if hasattr(model, "name")
    }
    if vol := models.get(name, None):
        if isinstance(vol, Volume):
            vol.data = grid
            vol.redraw_needed()
            return
        
    vol = add_grid(grid, session)

register_type(
    VolumeData,
    return_callback=add_volume_data_to_chimerax,
    choices=get_volume_data,
    nullable=False,
)