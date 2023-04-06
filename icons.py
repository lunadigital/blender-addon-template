import os
import bpy
from . import config


arrIcons = None
strDirectory = os.path.join(os.path.dirname(__file__), config.ICONS_DIRECTORY)

# 0. from . import icons
# 1. update the default path above
# 2. put initIcons in the primary register chain
# 3. put delIcons in the unregister chain
# example use = row.operator("key.set_space", text="SET",icon_value = icons.getIconId("set_space_16"))


def getIconId(strIcon):
    # The initialize_icons_collection function needs to be called first.
    return getIcon(strIcon).icon_id


def getIcon(strIcon, strPath=None):
    if strPath == None:
        strPath = os.path.join(strDirectory, strIcon + ".png")
    if strIcon in arrIcons:
        return arrIcons[strIcon]
    try:
        return arrIcons.load(strIcon, strPath, "IMAGE")
    except:
        print("couldn't find file for icon: ", strIcon, strPath)
        return None


def initIcons():
    global arrIcons
    arrIcons = bpy.utils.previews.new()


def delIcons():
    bpy.utils.previews.remove(arrIcons)
