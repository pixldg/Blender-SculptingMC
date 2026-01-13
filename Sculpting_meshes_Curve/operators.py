import bpy

# ============================================================
# ADD MESH
# ============================================================
class SCULPT_OT_add_mesh_object(bpy.types.Operator):
    bl_idname = "sculpt.add_mesh_object"
    bl_label = "Add Mesh"
    bl_description = "Adds a sculpting mesh"
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
        elif self.mesh_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add()
        elif self.mesh_type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add()
        elif self.mesh_type == 'CONE':
            bpy.ops.mesh.primitive_cone_add()
        elif self.mesh_type == 'TORUS':
            bpy.ops.mesh.primitive_torus_add()

        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

# ============================================================
# JOIN
# ============================================================
class SCULPT_OT_join_meshes(bpy.types.Operator):
    bl_idname = "sculpt.join_meshes"
    bl_label = "Join"
    bl_description = "Joins selected sculpting meshes"
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
    bl_label = "Boolean"
    bl_description = "Adds a boolean modifier to the active mesh"
    bl_options = {'REGISTER', 'UNDO'}

    operation: bpy.props.EnumProperty(
        items=[
            ('DIFFERENCE', "Difference", ""),
            ('UNION', "Union", ""),
            ('INTERSECT', "Intersect", ""),
        ],
        default='DIFFERENCE'
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT' and len(context.selected_objects) > 1

    def execute(self, context):
        active = context.active_object
        target = next(o for o in context.selected_objects if o != active)

        bpy.ops.object.mode_set(mode='OBJECT')
        mod = active.modifiers.new("Boolean", 'BOOLEAN')
        mod.operation = self.operation
        mod.object = target
        target.hide_set(True)
        target.hide_render = True
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

# ============================================================
# MIRROR
# ============================================================
class SCULPT_OT_add_mirror(bpy.types.Operator):
    bl_idname = "sculpt.add_mirror"
    bl_label = "Mirror"
    bl_description = "Adds a mirror modifier to the active mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        bpy.ops.object.mode_set(mode='OBJECT')
        if not any(m.type == 'MIRROR' for m in obj.modifiers):
            mod = obj.modifiers.new("Mirror", 'MIRROR')
            mod.use_clip = True
            mod.use_mirror_merge = True
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

class SCULPT_OT_apply_mirror(bpy.types.Operator):
    bl_idname = "sculpt.apply_mirror"
    bl_label = "Apply Mirror"
    bl_description = "Applies the mirror modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return any(m.type == 'MIRROR' for m in context.active_object.modifiers)

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        mirror = next(m for m in context.active_object.modifiers if m.type == 'MIRROR')
        bpy.ops.object.modifier_apply(modifier=mirror.name)
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

# ============================================================
# CURVE
# ============================================================
class SCULPT_OT_add_curve(bpy.types.Operator):
    bl_idname = "sculpt.add_curve"
    bl_label = "Curve"
    bl_description = "Adds a Bezier curve in 3D"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT'

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.curve.primitive_bezier_curve_add()
        curve = context.active_object.data
        curve.dimensions = '3D'
        curve.fill_mode = 'FULL'
        curve.use_fill_caps = True
        curve.bevel_depth = 0.05
        curve.bevel_resolution = 4
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class SCULPT_OT_finish_curve(bpy.types.Operator):
    bl_idname = "sculpt.finish_curve"
    bl_label = "Finish Curve"
    bl_description = "Converts the curve to a mesh and returns to Sculpt Mode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CURVE'

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

# ============================================================
# List of all operators for registration
# ============================================================
classes = (
    SCULPT_OT_add_mesh_object,
    SCULPT_OT_join_meshes,
    SCULPT_OT_boolean_modifier,
    SCULPT_OT_add_mirror,
    SCULPT_OT_apply_mirror,
    SCULPT_OT_add_curve,
    SCULPT_OT_finish_curve,
)
