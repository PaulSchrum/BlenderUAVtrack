'''
From
https://docs.blender.org/api/blender_python_api_2_65_5/info_tutorial_addon.html
Other help from:
https://www.youtube.com/watch?v=OEkrQGFqM10

I was able to get this addon to work, so now I will modify it to do what I need it to do.
'''

bl_info = {
    "name": "Paths",
    "category": "Object",
}

try:
    import bpy
except:
    pass

import dinkyKMLwrangler as dKw

testFile = r"D:\SourceModules\Python\BlenderUAVtrack\testData\Afarm_Flight1.kml"
pointSequence = dKw.DinkyKML(testFile)

# class PathEditor(bpy.types.Panel):
class PathEditor(bpy.types.Operator):
    """Import and (maybe) edit a Path"""  # tooltip for menu items and buttons.

    bl_idname = 'path.editor'
    bl_options = {'REGISTER', 'UNDO'}   # enable undo for the operator.
    bl_label = '3D Path Load'
    bl_context = 'objectmode'
    bl_category = 'Paths'
    # bl_category = "GIS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def __init__(self):
        self.fileLocation = \
            r"D:\SourceModules\Python\BlenderUAVtrack\testData\Afarm_Flight1.kml"
        pass

    def execute(self, context):        # execute() is called by blender when running the operator.

        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        self.report({'INFO'}, "Mouse coords are %d %d" % (self.x, self.y))
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

    def invoke(self, context, event):
        self.x = event.mouse_x  # Dummy code from an example file.
        self.y = event.mouse_y
        return self.execute(context)

def register():
    print("registering . . .")
    bpy.utils.register_class(PathEditor)
    print(); print('registered'); print()


def unregister():
    bpy.utils.unregister_class(PathEditor)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
