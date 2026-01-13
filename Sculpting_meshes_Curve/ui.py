import bpy
from .operators import classes

def sculpt_header_draw(self, context):
    layout = self.layout

    if context.mode == 'SCULPT':
        layout.separator()
        layout.operator("sculpt.add_curve", text="Curve", icon='CURVE_BEZCURVE')
        layout.separator()

        for icon, mesh in [
            ('MESH_PLANE', 'PLANE'),
            ('SPHERE', 'SPHERE'),
            ('MESH_ICOSPHERE', 'ICO'),
            ('MESH_UVSPHERE', 'QUADSPHERE'),
            ('CUBE', 'CUBE'),
            ('MESH_CYLINDER', 'CYLINDER'),
            ('MESH_CONE', 'CONE'),
            ('MESH_TORUS', 'TORUS'),
        ]:
            op = layout.operator("sculpt.add_mesh_object", text="", icon=icon)
            op.mesh_type = mesh

        layout.separator()
        layout.operator("sculpt.join_meshes", text="Join", icon='AUTOMERGE_ON')
        layout.operator("sculpt.add_boolean_modifier", text="Boolean", icon='MOD_BOOLEAN')
        layout.operator("sculpt.add_mirror", text="Mirror", icon='MOD_MIRROR')

    if context.active_object:
        if context.active_object.type == 'CURVE':
            layout.operator("sculpt.finish_curve", text="Finish Curve", icon='CHECKMARK')
        if any(m.type == 'MIRROR' for m in context.active_object.modifiers):
            layout.operator("sculpt.apply_mirror", text="Apply Mirror", icon='CHECKMARK')

