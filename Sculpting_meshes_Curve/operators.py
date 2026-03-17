import bpy

# ============================================================
# ADD MESH
# ============================================================

class SCULPT_OT_add_mesh_object(bpy.types.Operator):
    bl_idname = "sculpt.add_mesh_object"
    bl_label = "Add Mesh"
    bl_description = "Adds a mesh for sculpting"
    bl_options = {'REGISTER', 'UNDO'}

    mesh_type: bpy.props.EnumProperty(
        items=[
            ('PLANE', "Plane", ""),
            ('SPHERE', "Sphere", ""),
            ('ICO', "Ico Sphere", ""),
            ('QUADSPHERE', "Quad Sphere", ""),
            ('CUBE', "Cube", ""),
            ('CYLINDER', "Cylinder", ""),
            ('CONE', "Cone", ""),
            ('TORUS', "Torus", ""),
            ('CAPSULE', "Capsule", ""),
        ],
        default='SPHERE'
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT'

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')

        if self.mesh_type == 'PLANE':
            bpy.ops.mesh.primitive_plane_add()
        elif self.mesh_type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5)
        elif self.mesh_type == 'ICO':
            bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5, subdivisions=2)
        elif self.mesh_type == 'QUADSPHERE':
            bpy.ops.mesh.primitive_cube_add(size=1.0)
            obj = context.active_object
            mod = obj.modifiers.new("Subdiv", type='SUBSURF')
            mod.levels = 2
            mod.render_levels = 2
            mod.subdivision_type = 'CATMULL_CLARK'
            bpy.ops.object.modifier_apply(modifier=mod.name)
            obj.name = "Quadsphere"
        elif self.mesh_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add()
        elif self.mesh_type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add()
        elif self.mesh_type == 'CONE':
            bpy.ops.mesh.primitive_cone_add()
        elif self.mesh_type == 'TORUS':
            bpy.ops.mesh.primitive_torus_add()
        elif self.mesh_type == 'CAPSULE':
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.5,
                depth=2.0,
                location=(0, 0, 0)
            )
            obj = context.active_object
            bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
            bevel.offset_type = 'OFFSET'
            bevel.width = 0.4
            bevel.segments = 4
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=bevel.name)

        return {'FINISHED'}


# ============================================================
# CLONE
# ============================================================

class SCULPT_OT_clone_object(bpy.types.Operator):
    bl_idname = "sculpt.clone_object"
    bl_label = "Clone"
    bl_description = "Duplicates the active mesh safely while sculpting"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.mode == 'SCULPT' and obj and obj.type == 'MESH'

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}


# ============================================================
# BACK TO SCULPT
# ============================================================

class SCULPT_OT_back_to_sculpt(bpy.types.Operator):
    bl_idname = "sculpt.back_to_sculpt"
    bl_label = "Sculpt on Mesh"
    bl_description = "Returns to Sculpt Mode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and context.mode != 'SCULPT'

    def execute(self, context):
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}


# ============================================================
# JOIN
# ============================================================

class SCULPT_OT_join_meshes(bpy.types.Operator):
    bl_idname = "sculpt.join_meshes"
    bl_label = "Join"
    bl_description = "Joins selected meshes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT' and len(context.selected_objects) > 1

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}


# ============================================================
# BOOLEAN
# ============================================================

class SCULPT_OT_boolean_modifier(bpy.types.Operator):
    bl_idname = "sculpt.add_boolean_modifier"
    bl_label = "Boolean Difference"
    bl_description = "Adds a boolean DIFFERENCE modifier and hides the cutter"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT' and len(context.selected_objects) > 1

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')

        active = context.active_object
        target = next(o for o in context.selected_objects if o != active)

        mod = active.modifiers.new("Boolean", 'BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = target

        target.hide_set(True)
        target.hide_render = True

        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}


# ============================================================
# MULTIRESOLUTION
# ============================================================

class SCULPT_OT_add_multires(bpy.types.Operator):
    bl_idname = "sculpt.add_multires"
    bl_label = "Add Multires (Sculpt Base Mesh)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def execute(self, context):
        obj = context.active_object

        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        mod = obj.modifiers.new(name="Multires", type='MULTIRES')
        mod.use_sculpt_base_mesh = True

        bpy.ops.object.mode_set(mode='SCULPT')

        return {'FINISHED'}


# ============================================================
# MIRROR
# ============================================================

class SCULPT_OT_add_mirror(bpy.types.Operator):
    bl_idname = "sculpt.add_mirror"
    bl_label = "Mirror"
    bl_description = "Adds a mirror"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT' and context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        if not any(m.type == 'MIRROR' for m in obj.modifiers):
            mod = obj.modifiers.new("Mirror", 'MIRROR')
            mod.use_clip = True
            mod.use_mirror_merge = True
        return {'FINISHED'}


class SCULPT_OT_apply_mirror(bpy.types.Operator):
    bl_idname = "sculpt.apply_mirror"
    bl_label = "Apply Mirror"
    bl_description = "Applies the mirror modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.mode == 'SCULPT' and obj and any(m.type == 'MIRROR' for m in obj.modifiers)

    def execute(self, context):
        obj = context.active_object
        mirror_mod = next(m for m in obj.modifiers if m.type == 'MIRROR')

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_apply(modifier=mirror_mod.name)
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}


# ============================================================
# CURVE
# ============================================================

class SCULPT_OT_add_curve(bpy.types.Operator):
    bl_idname = "sculpt.add_curve"
    bl_label = "Curve"
    bl_description = "Adds a Bezier curve for sculpting"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT'

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.curve.primitive_bezier_curve_add()
        curve = context.active_object.data
        curve.dimensions = '3D'
        curve.bevel_resolution = 4
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


class SCULPT_OT_finish_curve(bpy.types.Operator):
    bl_idname = "sculpt.finish_curve"
    bl_label = "Sculpt on Curve"
    bl_description = "Evaluates curve geometry, converts to mesh, enters Sculpt Mode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CURVE'

    def execute(self, context):
        obj = context.active_object
        curve = obj.data

        bevel = curve.bevel_depth
        extrude = curve.extrude

        if bevel == 0 and extrude == 0:
            curve.bevel_depth = 0.04
            curve.use_fill_caps = True
        elif bevel > 0:
            curve.use_fill_caps = True

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}


# ============================================================
# REGISTER
# ============================================================

classes = (
    SCULPT_OT_add_mesh_object,
    SCULPT_OT_clone_object,
    SCULPT_OT_back_to_sculpt,
    SCULPT_OT_join_meshes,
    SCULPT_OT_boolean_modifier,
    SCULPT_OT_add_multires,
    SCULPT_OT_add_mirror,
    SCULPT_OT_apply_mirror,
    SCULPT_OT_add_curve,
    SCULPT_OT_finish_curve,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
