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

from .events import reviewAnimSpacGen
from .util import to_console

############################################################################
# Parameter Definitiions That Can Be Animated And Appear In Panels
############################################################################
def updateAnimSpacGenParameter(self,context):
	try:
		scene = context.scene
	except:
		scene = None
	if scene != None:
		result = "updateAnimSpacGenParameter: [%s]" % self.name
		to_console(result)
		reviewAnimSpacGen(scene)

class cls_AnimSpacGen(bpy.types.PropertyGroup):
	#z_count = bpy.props.IntProperty(name="Z Count", description="Count for Z axis.", default = 0, min = 0, max = 256, update=updateAnimSpacGenParameter)
	#x_offset = bpy.props.FloatProperty(name="X Offset", description="X distance between grid points.", default=1.0, min=0.0, max=2000.0, update=updateAnimSpacGenParameter)
	#recursive_offset = bpy.props.BoolProperty(name="Use Recursive Offset", description="When active, offset is accumulative.", default=False, options={'ANIMATABLE'}, subtype='NONE', update=updateAnimSpacGenParameter)
	#offset_object_name = bpy.props.StringProperty(name="Offset Name", description="Type an object name to derive transformation from, typically an Empty.", update=updateAnimSpacGenParameter)

	random_seed = bpy.props.IntProperty(name="Seed", description="Set the random seed for this AnimSpacGen object", default = 31, min = -420, max = 420, update=updateAnimSpacGenParameter)

	num_hull_segments_min = bpy.props.IntProperty(name="Hull Seg Min", description="Min. Hull Segments", default = 3, min = 1, max = 24, update=updateAnimSpacGenParameter)
	num_hull_segments_max = bpy.props.IntProperty(name="Hull Seg Max", description="Max. Hull Segments", default = 6, min = 1, max = 24, update=updateAnimSpacGenParameter)
	num_asymmetry_segments_min = bpy.props.IntProperty(name="Sym Seg Min", description="Min. Asymmetry Segments", default = 1, min = 1, max = 24, update=updateAnimSpacGenParameter)
	num_asymmetry_segments_max = bpy.props.IntProperty(name="Sym Seg Max", description="Max. Asymmetry Segments", default = 5, min = 1, max = 24, update=updateAnimSpacGenParameter)

	create_asymmetry_segments = bpy.props.BoolProperty(name="Create Asymmetry Segments", default=True, options={'ANIMATABLE'}, subtype='NONE', update=updateAnimSpacGenParameter)
	create_face_detail = bpy.props.BoolProperty(name="Create Face Detail", default=True, options={'ANIMATABLE'}, subtype='NONE', update=updateAnimSpacGenParameter)
	allow_horizontal_symmetry = bpy.props.BoolProperty(name="Allow Horizontal Symmetry", default=True, options={'ANIMATABLE'}, subtype='NONE', update=updateAnimSpacGenParameter)
	allow_vertical_symmetry = bpy.props.BoolProperty(name="Allow Vertical Symmetry", default=False, options={'ANIMATABLE'}, subtype='NONE', update=updateAnimSpacGenParameter)
	apply_bevel_modifier = bpy.props.BoolProperty(name="Apply Bevel Modifier", default=True, options={'ANIMATABLE'}, subtype='NONE', update=updateAnimSpacGenParameter)
	assign_materials = bpy.props.BoolProperty(name="Assign Materials", default=True, options={'ANIMATABLE'}, subtype='NONE', update=updateAnimSpacGenParameter)

	rnd_normal_chance = bpy.props.FloatProperty(name="Rnd Normal Chance", default=0.5, min=0.0001, max=1.0, update=updateAnimSpacGenParameter)
	rnd_extrusion_chance = bpy.props.FloatProperty(name="Rnd Extrusion Chance", default=0.1, min=0.0001, max=1.0, update=updateAnimSpacGenParameter)
	rnd_extrusion_deviation_chance = bpy.props.FloatProperty(name="Rnd Extrusion Chance", default=0.75, min=0.0001, max=1.0, update=updateAnimSpacGenParameter)
	rnd_hull_extrude_chance = bpy.props.FloatProperty(name="Rnd Hull Extrude Chance", default=0.5, min=0.0001, max=1.0, update=updateAnimSpacGenParameter)
	rnd_scaling_chance = bpy.props.FloatProperty(name="Rnd Scaling Chance", default=0.5, min=0.0001, max=1.0, update=updateAnimSpacGenParameter)
	rnd_side_trans_chance = bpy.props.FloatProperty(name="Rnd Sideways Translate Chance", default=0.5, min=0.0001, max=1.0, update=updateAnimSpacGenParameter)
	rnd_roty_chance = bpy.props.FloatProperty(name="Rnd Rotate Y Axis Chance", default=0.5, min=0.0001, max=1.0, update=updateAnimSpacGenParameter)

	material_types = [
				("0","Custom","custom"),
				("1","Matte","matte"),
				("2","Glass","glass"),
				("3","Mirror","mirror"),
				("4","Toon","toon"),
				("5","Emissive","emissive"),
				("6","Shadow Matte","shadow_matte"),
				]
	material = bpy.props.EnumProperty(name="Material", description="The material for this feature.", default="1", items=material_types, update=updateAnimSpacGenParameter)
	material_name = bpy.props.StringProperty(name="Material Name", description="Type a name of a material for this feature.", update=updateAnimSpacGenParameter)  

	bevel_profiles = [
				("0","Custom","custom"),
				("1","Tube","tube"),
				("2","Round Square","round square"),
				("3","C","c"),
				("4","L","l"),
				("5","T","t"),
				]
	profile = bpy.props.EnumProperty(name="Profile", description="The profile shape of this feature.", default="1", items=bevel_profiles, update=updateAnimSpacGenParameter)
	profile_name = bpy.props.StringProperty(name="Profile Name", description="Type a name that is a profile curve for this ring.", update=updateAnimSpacGenParameter) 
	profile_size_x = bpy.props.FloatProperty(name="Profile Size X", description="The X scale applied to non-custom profiles.", default=1.0, min=0.0, max=420.0, update=updateAnimSpacGenParameter)
	profile_size_y = bpy.props.FloatProperty(name="Profile Size Y", description="The Y scale applied to non-custom profiles.", default=1.0, min=0.0, max=420.0, update=updateAnimSpacGenParameter)

# collection of property group classes that need to be registered on module startup
classes = [cls_AnimSpacGen]

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	# Add these properties to every object in the entire Blender system (muha-haa!!)
	bpy.types.Object.AnimSpacGen_List_Index = bpy.props.IntProperty(min = 0,default = 0,description="Internal value. Do not animate.")
	bpy.types.Object.AnimSpacGen_List = bpy.props.CollectionProperty(type=cls_AnimSpacGen,description="Internal list class.")

def unregister():
	bpy.utils.unregister_module(__name__)
