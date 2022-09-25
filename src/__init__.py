from __future__ import annotations

from chimerax.core.toolshed import BundleAPI

class _MyAPI(BundleAPI):

    api_version = 1

    # Override method
    @staticmethod
    def start_tool(session, bi, ti):
        from ._api import ChimeraX
        chimerax = ChimeraX(session)
        
        from chimerax.core.commands import run
        run(session, "ui tool show Shell")
        
        from chimerax.map.volume_viewer import (
            add_volume_opened_callback, add_volume_closed_callback
        )
        add_volume_opened_callback(session, chimerax.reset_choices)
        add_volume_closed_callback(session, chimerax.reset_choices)
        
        from IPython import get_ipython
        shell = get_ipython()
        if shell is None:
            return
        
        
        # register all the types
        from . import _magicgui
        
        # update namespace
        import numpy
        namespace = {
            "ui": chimerax,
            "np": numpy,
            "Volume": _magicgui.Volume,
            "VolumeData": _magicgui.VolumeData,
            "VolumeDataTuple": _magicgui.VolumeDataTuple,
        }
        shell.push(namespace)
        

    @staticmethod
    def get_class(class_name):
        pass

bundle_api = _MyAPI()
