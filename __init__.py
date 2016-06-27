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
# <pep8-80 compliant>

	
bl_info = {
    "name": "Animated Spaceship Generator",
    "author": "Michael Davies, Atom (adds animatable parameters)",
    "version": (1, 0, 1),
    "blender": (2, 77, 0),
    "location": "View3D > Add > Mesh",
    "description": "Procedurally generate 3D spaceships from a random seed.",
    "wiki_url": "https://github.com/a1studmuffin/SpaceshipGenerator/blob/master/README.md",
    "tracker_url": "https://github.com/a1studmuffin/SpaceshipGenerator/issues",
    "category": "Add Mesh"
}

modules = ("util", "properties", "events", "operators", "ui")
if "bpy" in locals():
    import imp
    for mod in modules:
        exec("imp.reload(%s)" % mod)
else:
    for mod in modules:
        exec("from . import %s" % mod)

import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty
from bpy.types import Operator

class GenerateSpaceship(Operator):
    """Procedurally generate 3D spaceships from a random seed."""
    bl_idname = "mesh.generate_spaceship"
    bl_label = "Spaceship Animator"
    bl_options = {'REGISTER', 'UNDO'}

    random_seed = StringProperty(default='', name='Seed')
    num_hull_segments_min      = IntProperty (default=3, min=0, soft_max=16, name='Min. Hull Segments')
    num_hull_segments_max      = IntProperty (default=6, min=0, soft_max=16, name='Max. Hull Segments')
    create_asymmetry_segments  = BoolProperty(default=True, name='Create Asymmetry Segments')
    num_asymmetry_segments_min = IntProperty (default=1, min=1, soft_max=16, name='Min. Asymmetry Segments')
    num_asymmetry_segments_max = IntProperty (default=5, min=1, soft_max=16, name='Max. Asymmetry Segments')
    create_face_detail         = BoolProperty(default=True,  name='Create Face Detail')
    allow_horizontal_symmetry  = BoolProperty(default=True,  name='Allow Horizontal Symmetry')
    allow_vertical_symmetry    = BoolProperty(default=False, name='Allow Vertical Symmetry')
    apply_bevel_modifier       = BoolProperty(default=True,  name='Apply Bevel Modifier')
    assign_materials           = BoolProperty(default=True,  name='Assign Materials')

    def execute(self, context):
        spaceship_generator.generate_spaceship(
            self.random_seed,
            self.num_asymmetry_segments_min,
            self.num_asymmetry_segments_max,
            self.create_asymmetry_segments,
            self.num_asymmetry_segments_min,
            self.num_asymmetry_segments_max,
            self.create_face_detail,
            self.allow_horizontal_symmetry,
            self.allow_vertical_symmetry,
            self.apply_bevel_modifier)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(GenerateSpaceship.bl_idname, text="Spaceship")

def register():
	properties.register()
	ui.register()
	events.register()
	operators.register()

def unregister():
	properties.unregister()
	ui.unregister()
	events.unregister()
	operators.unregister()
