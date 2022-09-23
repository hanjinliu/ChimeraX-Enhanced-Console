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
        from IPython import get_ipython
        shell = get_ipython()
        if shell is None:
            return
        
        import numpy
        
        # register all the types
        from . import _magicgui
        
        namespace = {
            "ui": chimerax,
            "np": numpy,
            "VolumeData": _magicgui.VolumeData,
        }
        shell.push(namespace)
        

    @staticmethod
    def get_class(class_name):
        pass

bundle_api = _MyAPI()
