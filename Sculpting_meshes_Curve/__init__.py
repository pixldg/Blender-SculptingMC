bl_info = {
    "name": "Sculpting Extra Meshes + Curve",
    "author": "Emir Bojorquez",
    "version": (1, 0, 0),
    "blender": (5, 0, 1),
    "location": "View3D Top Bar",
    "category": "Sculpt",
}

from .operators import classes
from . import ui
import bpy

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_HT_header.append(ui.sculpt_header_draw)

def unregister():
    bpy.types.VIEW3D_HT_header.remove(ui.sculpt_header_draw)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
