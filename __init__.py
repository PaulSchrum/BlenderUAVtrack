'''
From
https://docs.blender.org/api/blender_python_api_2_65_5/info_tutorial_addon.html
Other help from:
https://www.youtube.com/watch?v=OEkrQGFqM10

I was able to get this addon to work, so now I will modify it to do what I need it to do.
'''

import dinkyKMLwrangler as dinky

bl_info = {
    "name": "Paths",
    "category": "Object",
}

try:
    import bpy
    import bmesh
    from Blender import *
except:
    pass

# import dinkyKMLwrangler as dKw

testFile = r"D:\SourceModules\Python\BlenderUAVtrack\testData\Afarm_Flight1.kml"
# pointSequence = dKw.DinkyKML(testFile)

import bpy
from mathutils import Vector

w = 1 # weight
listOfVectors = [Vector((0,0,0)),Vector((1,0,0)),Vector((2,0,0)),Vector((2,3,0)),
        Vector((0,2,1))]

# from http://blenderscripting.blogspot.com/2011/05/blender-25-python-bezier-from-list-of.html
def MakePolyLine(objname, curvename, ptList):
    curvedata = bpy.data.curves.new(name=curvename, type='CURVE')
    curvedata.dimensions = '3D'

    objectdata = bpy.data.objects.new(objname, curvedata)
    objectdata.location = (0,0,0) #object origin
    bpy.context.scene.objects.link(objectdata)

    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(ptList) - 1)
    # for num in range(len(cList)):
    #     x, y, z = cList[num]
    #     polyline.points[num].co = (x, y, z, w)
    for num, aPt in enumerate(ptList):
        x, y, z = aPt
        polyline.points[num].co = (x, y, z, 1)

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
        self.alignment = None

    def execute(self, context):        # execute() is called by blender when running the operator.

        self.alignment = dinky.DinkyKML(self.fileLocation)
        self.report({'INFO'}, "Loaded: " + str(self.alignment))

        # Adapted from
        # https://blender.stackexchange.com/a/21595/51056
        # scene = context.scene
        prevPt = self.alignment.pointSequence[0]
        for aPt in self.alignment.pointSequence[1:]:
            begPt = (prevPt.x, prevPt.y, prevPt.elev)
            endPt = (aPt.x, aPt.y, aPt.elev)
            MakePolyLine("FlightPath", "Segment1", [begPt, endPt])
            prevPt = aPt

        bpy.ops.mesh.primitive_uv_sphere_add(size=10.0,
                        location=(prevPt.x, prevPt.y, prevPt.elev))

        for aPoint in self.alignment.pointSequence:
            bpy.ops.mesh.primitive_uv_sphere_add(size=10.0,
                location=(aPoint.x, aPoint.y, aPoint.elev))

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
