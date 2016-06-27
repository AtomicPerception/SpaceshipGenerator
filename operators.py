# AddOn AnimSpacGen (c) 2016 Michael Davies, Atom
# Animated Spaceship Generator 1.0.1
# Manages and animates generated geometry.
# https://github.com/a1studmuffin/SpaceshipGenerator/blob/master/README.md
# Last Revision 06-27-2016

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy, random

from .events import reviewAnimSpacGen

from .util import to_console
from .util import returnNameDroppedPrefix
from .util import returnObjectNamesLike
from .util import removeObjectFromMemory
from .util import returnRandomColor
from .util import randFloat
from .util import randInt

from .util import ANIMSPACGEN_OB_PREFIX
from .util import ANIMSPACGEN_PROFILE_PREFIX
from .util import OBJECT_PREFIX
from .util import MATERIAL_PREFIX
from .util import MAX_NAME_SIZE

from .util import isBusy

############################################################################
# Operator code.
############################################################################
# Create operator to rename this object with the bleeble_ preifix.   
class OBJECT_OT_rename_to_AnimSpacGen(bpy.types.Operator):
	bl_label = "Rename To AnimSpacGen"
	bl_idname = "op.rename_to_animspacgen"
	bl_description = "Click this button to rename this object with the AnimSpacGen_ prefix. This will make it a AnimSpacGen object."
	
	def invoke(self, context, event):
		ob = context.object
		if ob != None:
			AnimSpacGen_name = OBJECT_PREFIX + ob.name
			if len(AnimSpacGen_name) > MAX_NAME_SIZE:
				# Name too long.
				AnimSpacGen_name = AnimSpacGen_name[:MAX_NAME_SIZE]
			ob_source = bpy.data.objects.get(AnimSpacGen_name)
			if ob_source != None:
				# Hmm...already and object named like this.
				to_console ("Already an object named like [" + AnimSpacGen_name + "] rename manualy.")
			else:
				ob.name = AnimSpacGen_name
		return {'FINISHED'}

# Create operator to add or remove entries to/from the Collection   
class OBJECT_OT_add_remove_String_Items(bpy.types.Operator):
	bl_label = "Add or Remove"
	bl_idname = "op.collection_add_remove"
	add = bpy.props.BoolProperty(default = True)
	
	def invoke(self, context, event):
		add = self.add
		ob = context.object
		if ob != None:
			collection = ob.AnimSpacGen_List
			if add:
				# This adds at the end of the collection list.
				collection.add()
				l = len(collection)
				entry_name = returnNameDroppedPrefix(ob)
				collection[-1].name= ("%s-%i" % (entry_name,l))
			else:
				l = len(collection)
				if l > 1:
					# This removes one item in the collection list function of index value
					index = ob.AnimSpacGen_List_Index
					collection.remove(index)
				else:
					to_console ("Can not remove last item.")
		return {'FINISHED'}
		
def register():
	bpy.utils.register_class(OBJECT_OT_rename_to_AnimSpacGen)
	bpy.utils.register_class(OBJECT_OT_add_remove_String_Items)

def unregister():
	bpy.utils.unregister_class(OBJECT_OT_rename_to_AnimSpacGen)
	bpy.utils.unregister_class(OBJECT_OT_add_remove_String_Items)

