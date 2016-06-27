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

import bpy
import threading, time
from bpy_extras.object_utils import AddObjectHelper

from .util import OBJECT_PREFIX
from .util import ANIMSPACGEN_OB_PREFIX

from .util import to_console
from .util import returnNameDroppedPrefix

from .events import reviewAnimSpacGen

############################################################################
# Thread processing for parameters that are invalid to set in a DRAW context.
# By performing those operations in these threads we can get around the invalid CONTEXT error within a draw event.
# This is fairly abusive to the system and may result in instability of operation.
# Then again as long as you trap for stale data it just might work..?
# For best result keep the sleep time as quick as possible...no long delays here.
############################################################################
def AnimSpacGen_new_source(lock, passedSourceName, passedSleepTime):
	time.sleep(passedSleepTime) # Feel free to alter time in seconds as needed.   
	to_console("AnimSpacGen threading: AnimSpacGen_new_source")
	ob_source = bpy.data.objects.get(passedSourceName)
	if ob_source !=None:
			ob_source.show_name = True
			# Populate the new entry in the collection list.
			collection = ob_source.AnimSpacGen_List
			collection.add()
			l = len(collection)
			animspacgen_name = returnNameDroppedPrefix(ob_source)
			collection[-1].name= ("%s-%i" % (animspacgen_name,l))
			#collection[-1].name= (ENTRY_NAME + str(l))
			to_console("AnimSpacGen threading: New entry established on [%s]." % passedSourceName)
	else:
		to_console("AnimSpacGen threading: Source not found [%s]." % passedSourceName) 

############################################################################
# PANEL code.
############################################################################   
supported_types = ['MESH'] 

# Template List Draw Routine
class ATOMS_265_UI_Template_List(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.label(text=item.name, translate=False, icon_value=icon)
		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)
			
class OBJECT_PT_AnimSpacGen(bpy.types.Panel):
	bl_label = "AnimSpacGen"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "object"

	@classmethod
	def poll(cls, context):
		result = False
		if context != None:
			ob = context.object
			if ob != None:
				if ob.type in supported_types:
					result = True
		return result

	def draw(self, context):
		if context != None:
			ob = context.object
			if ob != None:
				if ob.type in supported_types:
					layout = self.layout
					try:
						# Looks like all is good, we can proceed.
						ob = context.object
						can_proceed = True
					except:
						# We got an error, we are in a crash/rendering state.
						# Skip this update.
						can_proceed = False
					if can_proceed == True:

						l = len(OBJECT_PREFIX)
						if ob.name[:l] == OBJECT_PREFIX:
							try:
								l = len(ob.AnimSpacGen_List)
							except:
								l = 0
							if l > 0:
								# Related items go in this box.
								box = layout.box()
								
								# Display list of targets in panel.
								#box.label("Ship Sets: Participant Manager")
										
								# Display self created properties.
								entry = ob.AnimSpacGen_List[ob.AnimSpacGen_List_Index]
								name_base = entry.name
								
								# Parameters draw in this box.
								box = box.box()
								box.prop(entry, "random_seed")
								layout.separator()
								box.prop(entry, "create_face_detail")
								box.prop(entry, "num_hull_segments_min")
								box.prop(entry, "num_hull_segments_max")
								layout.separator()
								box.prop(entry, "create_asymmetry_segments")
								box.prop(entry, "num_asymmetry_segments_min")
								box.prop(entry, "num_asymmetry_segments_max")
								box.prop(entry, "allow_horizontal_symmetry")
								box.prop(entry, "allow_vertical_symmetry")
								
								#box.prop(entry, "apply_bevel_modifier")
								#box.prop(entry, "assign_materials")
		
							else:
								# We have no collections so we have to add one.
								# But Blender has a WriteID lock in place at this time.
								# So we launch a thread that will run in a very, very short time from now.
								# Meanwhile we simply exit because the def this new thread calls will do the work we intended to do here.
								#ob.AnimSpacGen_List.add()
								
								# Launch a thread to set the remaining values that would generate a CONTEXT error if issued now. (listed below)
								lock = threading.Lock()
								lock_holder = threading.Thread(target=AnimSpacGen_new_source, args=(lock,ob.name,0.02), name='AnimSpacGen_New_Source')
								lock_holder.setDaemon(True)
								lock_holder.start()
						else:
							# Common to end up here for other non-AnimSpacGen objects.
							layout.label("Not a AnimSpacGen object yet.",icon='INFO')  
							layout.operator("op.rename_to_animspacgen", icon="SORTALPHA", text="(rename with '" + OBJECT_PREFIX +"' prefix to enable)")
					else:
						to_console("ERROR: Can not proceed..?")
		else:
			# This can happen sometimes after a render.
			to_console ("AnimSpacGen was given an invalid context, imagine that..")
			self.layout.label("AnimSpacGen was given an invalid context.",icon='HELP')

###########################################################################
# Menu code.
###########################################################################
def install_animspacgen(self, context):
	# Time to actually create a AnimSpacGen object.
	ob = bpy.data.objects.new("AnimSpacGen_Controller",None)
	if ob != None:
		ob.show_axis = True
		context.scene.objects.link(ob)
		result = "AnimSpacGen [%s] added to the scene." % ob.name
	else:
		result = "Failed to create a new AnimSpacGen object." 
		# This adds at the end of the collection list.
				
	# Add the first spaceship generator item to the collection.
	collection = ob.AnimSpacGen_List
	collection.add()
	l = len(collection)
	entry_name = returnNameDroppedPrefix(ob)
	collection[-1].name= ("%s-%i" % (entry_name,l))
	collection[-1].start = 0.1
	collection[-1].stop = 0.9
	#reviewAnimSpacGen(context.scene)
	to_console(result)
	
class OBJECT_OT_add_animspacgen(bpy.types.Operator, AddObjectHelper):
	"""AnimSpacGen"""
	bl_idname = "ob.add_animspacgen"
	bl_label = "AnimSpacGen"
	bl_description = "AnimSpacGen generates a spaceship with animatable hull parameters."
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		install_animspacgen(self, context)
		return {'FINISHED'}

def add_animspacgen(self, context):
	self.layout.operator(
		OBJECT_OT_add_animspacgen.bl_idname,
		text="AnimSpacGen",
		icon="MESH_TORUS")
		   
def register():
	bpy.utils.register_class(OBJECT_PT_AnimSpacGen)
	bpy.utils.register_class(ATOMS_265_UI_Template_List)
	bpy.utils.register_class(OBJECT_OT_add_animspacgen)
	bpy.types.INFO_MT_curve_add.append(add_animspacgen)

def unregister():
	bpy.utils.unregister_class(OBJECT_PT_AnimSpacGen)
	bpy.utils.unregister_class(ATOMS_265_UI_Template_List)
	bpy.utils.unregister_class(OBJECT_OT_add_animspacgen)
	bpy.types.INFO_MT_curve_add.remove(add_animspacgen)

