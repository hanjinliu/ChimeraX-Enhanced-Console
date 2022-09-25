from __future__ import annotations

from typing import NewType, TYPE_CHECKING, Any
import numpy as np
from magicgui import register_type
from magicgui.widgets import FunctionGui

from chimerax.map.volume import Volume
from chimerax.map_data import ArrayGridData

from ._utils import add_grid

if TYPE_CHECKING:
    from chimerax.core.session import Session

VolumeData = NewType("VolumeData", np.ndarray)
VolumeDataTuple = NewType("VolumeDataTuple", tuple)

def get_session() -> Session:
    from ._api import ChimeraX
    return ChimeraX._session

def get_volumes(_) -> list[tuple[str, Volume]]:
    """Get the list of available volumes and the names."""
    models = get_session().models.list()
    return [(m.name, m) for m in models if isinstance(m, Volume)]

def get_volume_data(_) -> list[tuple[str, np.ndarray]]:
    """Get the list of available volume data and the names."""
    models = get_session().models.list()
    return [(m.name, m.matrix()) for m in models if isinstance(m, Volume)]

def add_or_update(arr: np.ndarray, name: str, **kwargs):
    session = get_session()
    if isinstance(arr, np.ndarray):
        from ._api import ChimeraX
        grid = ArrayGridData(arr, name=name, **kwargs)
    else:
        raise NotImplementedError()
    
    for vol in session.models.list(type=Volume):
        vol: Volume
        if vol.name == name:
            vol.replace_data(grid)
            return
        
    vol = add_grid(grid, session)
    return

def add_volume_data_to_chimerax(gui: FunctionGui, result: Any, return_type: type) -> None:
    return add_or_update(result, gui.result_name)

def add_volume_data_tuple_to_chimerax(gui: FunctionGui, result: Any, return_type: type) -> None:
    if not isinstance(result, tuple):
        raise TypeError(f"Expected tuple, got {type(result)}")
    nout = len(result)
    if nout == 1:
        arr = result[0]
        name = gui.result_name
        kwargs = {}
    elif nout == 2:
        arr, second_arg = result
        if isinstance(second_arg, dict):
            name = second_arg.pop("name", gui.result_name)
            kwargs = second_arg
        else:
            name = second_arg
            kwargs = {}
    elif nout == 3:
        arr, name, kwargs = result
    else:
        raise ValueError(f"Length of VolumeDataTuple must be < 4, was {nout}.")

    return add_or_update(arr, name, **kwargs)
        

register_type(
    VolumeData,
    return_callback=add_volume_data_to_chimerax,
    choices=get_volume_data,
    nullable=False,
)

register_type(
    Volume,
    choices=get_volumes,
    nullable=False,
)

register_type(
    VolumeDataTuple,
    return_callback=add_volume_data_tuple_to_chimerax,
)
