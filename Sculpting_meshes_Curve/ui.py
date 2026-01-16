import bpy


def sculpt_header_draw(self, context):
    layout = self.layout

    if context.mode == 'SCULPT':
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

        layout.operator("sculpt.clone_object", text="Clone", icon='DUPLICATE')
        layout.operator("sculpt.add_mirror", text="Mirror", icon='MOD_MIRROR')
        layout.operator("sculpt.apply_mirror", text="Apply Mirror", icon='CHECKMARK')
        layout.operator("sculpt.join_meshes", text="Join", icon='AUTOMERGE_ON')
        layout.operator("sculpt.add_boolean_modifier", text="Boolean", icon='MOD_BOOLEAN')
        layout.operator("sculpt.add_curve", text="Curve", icon='CURVE_BEZCURVE')

    if context.mode == 'OBJECT':
        layout.operator("sculpt.back_to_sculpt", text="Sculpt on Mesh", icon='SCULPTMODE_HLT')

    if context.active_object and context.active_object.type == 'CURVE':
        layout.operator("sculpt.finish_curve", text="Sculpt on Curve", icon='CHECKMARK')


def register():
    bpy.types.VIEW3D_HT_header.append(sculpt_header_draw)


def unregister():
    bpy.types.VIEW3D_HT_header.remove(sculpt_header_draw)
