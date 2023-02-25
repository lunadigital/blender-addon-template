import bpy
import requests
import json
import textwrap
import os
import time
from . import config

# This fun little script created by Anthony Aragues:  https://AnthonyAragues.com
# 1. Update the defaults and constants at the top
# 2. add the register(bl_info) and unregister() in init chain
# 3. call the draw function from the panel you want it to appear: version.draw_version_box(self, context)

URL = 'https://anthonyaragues.com/animix_check.json'
PREFIX = 'TMP'
if config and config.ADDON_PREFIX:
    PREFIX = config.ADDON_PREFIX
ALLOW_DISMISS_VERSION = True
CHECK_FREQUENCY = 86400 * 30
CHECK_EVERY = 10
objDefault = {
    "version": "0",
    "ver_message": "Update Available",
    "bm_url": "blendermarket url",
    "gm_url": "gumrd url",
    "message": "",
    "btn_name": "",
    "url": "",
    "hide_message": True,
    "hide_version": True
}
# ----====|| EVERYTHING BELOW HERE SHOULD NOT NEED TO BE MODIFIED MANUALLY ||====----
VERSION_FILE = os.path.join(os.path.dirname(
    __file__), f'{PREFIX}_version.json')
arrClasses = []


def prefix_name(opClass):
    opClass.__name__ = PREFIX.upper() + '_OT_' + opClass.__name__
    arrClasses.append(opClass)
    return opClass


@prefix_name
class Hide_Version(bpy.types.Operator):
    bl_idname = f'{PREFIX.lower()}.hide_version_panel'
    bl_label = "x"
    bl_description = "Dismiss this version"

    def execute(self, context):
        objVersion = getVersionFile()
        objVersion["hide_version"] = True
        setVersionFile(objVersion)
        return {'FINISHED'}


@prefix_name
class Hide_Message(bpy.types.Operator):
    bl_idname = f'{PREFIX.lower()}.hide_message_panel'
    bl_label = "x"
    bl_description = "Dismiss this message"

    def execute(self, context):
        objVersion = getVersionFile()
        objVersion["hide_message"] = True
        setVersionFile(objVersion)
        return {'FINISHED'}


def getIntVersion(strVersion):
    strVersion = strVersion.replace(",", ".").replace(")", "").replace("(", "")
    return int(strVersion.replace(".", "").replace(" ", ""))


def getVersionFile():
    objVersion = None
    try:
        objFile = open(VERSION_FILE)
        objVersion = json.load(objFile)
        objFile.close()
        for strKey in objDefault.keys():
            if strKey not in objVersion:
                objVersion[strKey] = objDefault['strKey']
    except:
        objVersion = objDefault
    return objVersion


def setVersionFile(objVersionFile):
    objFile = open(VERSION_FILE, 'w')
    objFile.write(json.dumps(objVersionFile))
    objFile.close()


def check_version(bl_info):
    objResponse = None
    objVersion = None
    objPreference = getVersionFile()
    # some fail early modes
    # throttle check frequency by setting
    intTime = int(time.time())
    if 'checkIn' in objPreference:
        if objPreference['checkIn'] > 0:
            objPreference['checkIn'] = objPreference['checkIn']-1
            setVersionFile(objPreference)
            return

    if 'lastCheck' in objPreference and objPreference['lastCheck'] + CHECK_FREQUENCY > intTime:
        return

    try:
        print('check url')
        objResponse = requests.get(URL)
    except:
        pass
    if objResponse and objResponse.status_code == 200:
        try:
            objVersion = json.loads(objResponse.text)
        except:
            pass
        if objVersion is not None:
            objVersion['lastCheck'] = intTime
            objVersion['checkIn'] = CHECK_EVERY
            if getIntVersion(objVersion["version"]) > getIntVersion(str(bl_info["version"])):
                if getIntVersion(objVersion["version"]) > getIntVersion(objPreference["version"]):
                    objVersion["hide_version"] = False
                else:
                    objVersion["hide_version"] = objPreference["hide_version"]
            else:
                objVersion["hide_version"] = True
            if objVersion["message"] != objPreference["message"]:
                objVersion["hide_message"] = False
            else:
                objVersion["hide_message"] = objPreference["hide_message"]
            setVersionFile(objVersion)


def getTextArray(context, text):
    intWidth = int(context.region.width)-30
    chars = intWidth / 7   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    return wrapper.wrap(text=text)


def draw_version_box(objPanel, context):
    # ---------------  VERSION CHECK PANEL -----------------
    objVersion = getVersionFile()
    layout = objPanel.layout
    if objVersion is not None and "hide_version" in objVersion.keys() and objVersion["hide_version"] != True:
        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'EXPAND'
        row.label(icon="INFO", text=objVersion["ver_message"])
        if ALLOW_DISMISS_VERSION:
            row.operator(f'{PREFIX}.hide_version_panel', text="", icon="X")
        if "bm_url" in objVersion.keys():
            row = box.row()
            row.operator(
                'wm.url_open', text="Blender Market", icon="URL").url = objVersion["bm_url"]
        if "gm_url" in objVersion.keys():
            row = box.row()
            row.operator(
                'wm.url_open', text="GumRoad", icon="URL").url = objVersion["gm_url"]


def register(bl_info):
    for i in arrClasses:
        bpy.utils.register_class(i)
    check_version(bl_info)


def unregister():
    for i in reversed(arrClasses):
        bpy.utils.unregister_class(i)
