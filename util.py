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
import os,sys,colorsys

import mathutils
from mathutils import Vector, Matrix

import random
from random import randint, uniform


#####################################################################
# Globals.
#####################################################################
# Global busy flag. Try to avoid events if we are already busy.
isBusy = False
isRendering = False
lastFrameUpdated = 0.0
frameChangeCount = 0
      
# Objects are managed by name prefix. Customize here...e.g. ReRing_Cube
ANIMSPACGEN_OB_PREFIX = "asg_"        #For managed object naming.
ANIMSPACGEN_CURVE_PREFIX = "cu_asg_"  #For managed datablock naming.
ANIMSPACGEN_PROFILE_PREFIX = "asgp_"   #For managed datablock naming.
MATERIAL_PREFIX = "mat_asg_"

OBJECT_PREFIX = "SpacGen_"       #For control object naming.
ENTRY_NAME = "item-"            #For new list entries.

TUBE_NAME = "profile_circle"
SQUARE_NAME = "profile_round_square"
C_NAME = "profile_C"
L_NAME = "profile_L"
T_NAME = "profile_T"
                
MAX_NAME_SIZE = 42
GLOBAL_ZERO_PADDING = 4             # The number of zeros to padd strings with when converting INTs to STRINGs.
DELIMITER = ","

#####################################################################
# Simple debug message control.
#####################################################################
SHOW_MESSAGES = True
MSG_PREFIX = "asg=#> "
def to_console(passedItem):
	if SHOW_MESSAGES == True:
		if len(passedItem) == 0:
			print("")
		else:
			s = str(passedItem)
			print(MSG_PREFIX + s)

#####################################################################
# Memory Management.
#####################################################################
def removeCurveFromMemory (passedName):
	# Extra test because this can crash Blender if not done correctly.
	result = False
	curve = bpy.data.curves.get(passedName)
	if curve != None:
		if curve.users == 0:
			try:
				curve.user_clear()
				can_continue = True
			except:
				can_continue = False
			
			if can_continue == True:
				try:
					bpy.data.curves.remove(curve)
					result = True
					#to_console("removeCurveFromMemory: MESH [" + passedName + "] removed from memory.")
				except:
					result = False
					to_console("removeCurveFromMemory: FAILED to remove [" + passedName + "] from memory.")
			else:
				# Unable to clear users, something is holding a reference to it.
				# Can't risk removing. Favor leaving it in memory instead of risking a crash.
				to_console("removeCurveFromMemory: Unable to clear users for MESH, something is holding a reference to it.")
				result = False
		else:
			to_console ("removeCurveFromMemory: Unable to remove CURVE because it still has [" + str(curve.users) + "] users.")
	else:
		# We could not fetch it, it does not exist in memory, essentially removed.
		result = True
	return result
	
def removeMeshFromMemory (passedName):
	# Extra test because this can crash Blender if not done correctly.
	result = False
	mesh = bpy.data.meshes.get(passedName)
	if mesh != None:
		if mesh.users == 0:
			try:
				mesh.user_clear()
				can_continue = True
			except:
				can_continue = False
			
			if can_continue == True:
				try:
					bpy.data.meshes.remove(mesh)
					result = True
					#to_console("removeMeshFromMemory: MESH [" + passedName + "] removed from memory.")
				except:
					result = False
					to_console("removeMeshFromMemory: FAILED to remove [" + passedName + "] from memory.")
			else:
				# Unable to clear users, something is holding a reference to it.
				# Can't risk removing. Favor leaving it in memory instead of risking a crash.
				to_console("removeMeshFromMemory: Unable to clear users for MESH, something is holding a reference to it.")
				result = False
		else:
			to_console ("removeMeshFromMemory: Unable to remove MESH because it still has [" + str(mesh.users) + "] users.")
	else:
		# We could not fetch it, it does not exist in memory, essentially removed.
		result = True
	return result

def removeObjectFromMemory (passedName):
	# Extra test because this can crash Blender if not done correctly.
	result = False
	ob = bpy.data.objects.get(passedName)
	if ob != None:
		if ob.users == 0:
			try:
				ob.user_clear()
				can_continue = True
			except:
				can_continue = False
			
			if can_continue == True:
				try:
					bpy.data.objects.remove(ob)
					result = True
				except:
					result = False
			else:
				# Unable to clear users, something is holding a reference to it.
				# Can't risk removing. Favor leaving it in memory instead of risking a crash.
				to_console("removeObjectFromMemory: Unable to clear users for OBJECT, something is holding a reference to it.")
				result = False
		else:
			to_console ("removeObjectFromMemory: Unable to remove OBJECT because it still has [" + str(ob.users) + "] users.") 
	else:
		# We could not fetch it, it does not exist in memory, essentially removed.
		result = True
	return result 
	
#####################################################################
# Name management
##################################################################### 
def returnAllObjectNames (scene):
    # NOTE: This returns all object names in the passed scene.
    result = []
    for ob in scene.objects:
        result.append(ob.name)
    return result 

def returnObjectNamesLike(passedScene, passedName):
	# Return objects named like our passedName in the passed scene.
	result = []
	isLike = passedName
	l = len(isLike)
	all_obs = returnAllObjectNames(passedScene)
	for name in all_obs:
		candidate = name[0:l]
		if isLike == candidate:
			result.append(name)
	return result

def returnNameForNumber(passedFrame):
    frame_number = str(passedFrame)
    post_fix = frame_number.zfill(GLOBAL_ZERO_PADDING)
    return post_fix

def returnNameDroppedPrefix(ob):
    # Use only right half of name, i.e. discard xxxx_ prefix.
    lst_name = ob.name.split('_')
    return lst_name[1]

############################################################################
# Random code.
############################################################################
def randFloat(a, b):
    #random.seed(RANDOM_SEED)
    return random.random()*(b-a)+a

def randInt(a, b):
    #random.seed(RANDOM_SEED)
    return random.randint(int(a),int(b))

def returnRandomColor (color_base = None):
    if color_base == None:
        # Ugly random color.
        return (randFloat(0.2,1.0),randFloat(0.2,1.0),randFloat(0.2,1.0))
    else:
        # Random color based upon base color hue.
        h, s, v = colorsys.rgb_to_hsv(color_base[0],color_base[1],color_base[2])
        # Use the HUE from color base to determine this unique random color.
        return (returnRndRGBFromHue (h))

############################################################################
# Color code.
############################################################################
def returnNumberOfColors(count):
    N = count
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    return RGB_tuples

def returnRndRGBFromHue (h):
    #h = uniform(0.25, 0.38) # Select random green'ish hue from hue wheel
    s = uniform(0.4, 1.0)
    v = uniform(0.2, 0.9)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return r,g,b