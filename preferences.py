import bpy
from . import config

arrClasses = []


def prefix_name(opClass):
    opClass.__name__ = config.ADDON_PREFIX.upper() + opClass.__name__
    arrClasses.append(opClass)
    return opClass


@prefix_name
class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    some_path: bpy.props.StringProperty(
        name="Custom Folder Path",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="PREFERENCES")
        row = layout.row()
        row.prop(self, "some_path")


#### || CLASS MAINTENANCE ||####
def register():
    for i in arrClasses:
        bpy.utils.register_class(i)


def unregister():
    for i in reversed(arrClasses):
        bpy.utils.unregister_class(i)
