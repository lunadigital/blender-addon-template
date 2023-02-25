import bpy
from . import config

# collect all the classes to register
arrClasses = []


def prefix_name(opClass):
    opClass.__name__ = config.ADDON_PREFIX.upper() + '_OT_' + opClass.__name__
    arrClasses.append(opClass)
    return opClass


@prefix_name
class shoot_first(bpy.types.Operator):
    """first operators tooltip"""
    bl_idname = f'{config.ADDON_PREFIX.lower()}.shoot_first'
    bl_label = "Shoot"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        # put stuff here as a condition fo enabling the operator return True or False for enabling
        return True

    def execute(self, context):
        print("I shot!")
        return {'FINISHED'}


#### || CLASS MAINTENANCE ||####
def register():
    for i in arrClasses:
        bpy.utils.register_class(i)


def unregister():
    for i in reversed(arrClasses):
        bpy.utils.unregister_class(i)
