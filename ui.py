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
from bpy.types import Panel

#
# Add additional functions here
#

class MyPanel(Panel):
    bl_label = 'My Awesome Panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type= 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        row = self.layout.row()
        row.prop(context.scene, 'my_property')

def register():
    bpy.utils.register_class(MyPanel)

def unregister():
    bpy.utils.unregister_class(MyPanel)
