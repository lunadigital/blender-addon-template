# Blender Add-on Template
# Contributor(s): Aaron Powell (aaron@lunadigital.tv)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import sys
from bpy.types import Panel
from . import config

# collect all the classes to register
arrClasses = []


def prefix_name(opClass):
    opClass.__name__ = config.ADDON_PREFIX.upper() + '_PT_' + opClass.__name__
    arrClasses.append(opClass)
    return opClass

#
# Add additional functions here
#


@prefix_name
class MyPanel(Panel):
    bl_label = config.ADDON_NAME
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        row = self.layout.row()
        row.prop(context.scene, 'my_property')
        row.op()


#### || CLASS MAINTENANCE ||####
def register():
    for i in arrClasses:
        bpy.utils.register_class(i)


def unregister():
    for i in reversed(arrClasses):
        bpy.utils.unregister_class(i)
