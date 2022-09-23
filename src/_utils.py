from __future__ import annotations
from typing import TYPE_CHECKING

from chimerax.map import volume_from_grid_data, Volume
from chimerax.map_data import GridData

if TYPE_CHECKING:
    from chimerax.core.session import Session
    
def add_grid(grid: GridData, session: Session) -> Volume:
    """Add a grid to the ChimeraX session with unique ID."""
    i = 1
    while session.models.have_id((i,)):
        i += 1
    return volume_from_grid_data(grid, session, model_id=(i,))
