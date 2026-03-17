import bpy


class SCULPT_MT_primitives(bpy.types.Menu):
    bl_label = "Primitives"
    bl_idname = "SCULPT_MT_primitives"

    def draw(self, context):
        layout = self.layout

        for icon, mesh, label in [
            ('MESH_PLANE', 'PLANE', "Plane"),
            ('SPHERE', 'SPHERE', "Sphere"),
            ('MESH_ICOSPHERE', 'ICO', "Ico Sphere"),
            ('MESH_UVSPHERE', 'QUADSPHERE', "Quad Sphere"),
            ('CUBE', 'CUBE', "Cube"),
            ('MESH_CYLINDER', 'CYLINDER', "Cylinder"),
            ('MESH_CONE', 'CONE', "Cone"),
            ('MESH_TORUS', 'TORUS', "Torus"),
            ('META_CAPSULE', 'CAPSULE', "Capsule"),
        ]:
            op = layout.operator("sculpt.add_mesh_object", text=label, icon=icon)
            op.mesh_type = mesh


class SCULPT_MT_modifiers(bpy.types.Menu):
    bl_label = "Modifiers"
    bl_idname = "SCULPT_MT_modifiers"

    def draw(self, context):
        layout = self.layout

        layout.operator("sculpt.clone_object", icon='DUPLICATE')
        layout.operator("sculpt.join_meshes", icon='AUTOMERGE_ON')

        layout.separator()

        layout.operator("sculpt.add_mirror", icon='MOD_MIRROR')
        layout.operator("sculpt.apply_mirror", icon='CHECKMARK')

        layout.separator()

        layout.operator("sculpt.add_multires", icon='MOD_MULTIRES')

        layout.separator()

        layout.operator("sculpt.add_boolean_modifier", icon='MOD_BOOLEAN')


def sculpt_header_draw(self, context):
    layout = self.layout

    if context.mode == 'SCULPT':
        layout.menu("SCULPT_MT_primitives", icon='MESH_CUBE')
        layout.menu("SCULPT_MT_modifiers", icon='MODIFIER')
        layout.operator("sculpt.add_curve", icon='CURVE_BEZCURVE')

    if context.mode == 'OBJECT':
        layout.operator("sculpt.back_to_sculpt", text="Sculpt on Mesh", icon='SCULPTMODE_HLT')

    if context.active_object and context.active_object.type == 'CURVE':
        layout.operator("sculpt.finish_curve", text="Sculpt on Curve", icon='CHECKMARK')


classes = (
    SCULPT_MT_primitives,
    SCULPT_MT_modifiers,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_HT_header.append(sculpt_header_draw)


def unregister():
    bpy.types.VIEW3D_HT_header.remove(sculpt_header_draw)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
