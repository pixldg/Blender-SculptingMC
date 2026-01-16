bl_info = {
    "name": "Sculpting Extra Meshes + Curve",
    "author": "Emir Bojorquez",
    "version": (1, 2, 0),
    "blender": (5, 0, 1),
    "location": "View3D Top Bar",
    "category": "Sculpt",
}

import bpy
from . import operators
from . import ui


def register():
    operators.register()
    ui.register()


def unregister():
    ui.unregister()
    operators.unregister()


if __name__ == "__main__":
    register()
