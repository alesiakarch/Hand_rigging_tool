import sys
import maya.cmds as cmds 
import riglib as rl
sys.path.insert(0, cmds.workspace(expandName = 'scripts'))
sys.path.insert(0, cmds.workspace(expandName = 'scenes'))

def rename_fingers(finger_chain, finger_name):
	# rename_fingers(list, string)
	for i in range(0, len(finger_chain)):
		
		string_parts = finger_chain[i].split('_', 1) 
		finger_chain[i] = finger_name + '_' + string_parts[1]
	
	return finger_chain


# duplicate rename to set up joing chains 
# add grouping for the fingers
# runs duplicate rename for each finger
in_chain = ['Index_JNT_1', 'Index_JNT_2', 'Index_JNT_3', 'Index_end_JNT_4']
fingers = ['Index', 'Middle', 'Ring', 'Pinky']

for i in range(3):
	rename_fingers(in_chain, fingers[i])
	rl.duplicate_rename_joints(in_chain)

# parent fk controls
# add an option to skip twist joints
# and make the circles smaller 
# fk naming convention is a little off
fk_chain = ['Hand_base_JNT', 'Hand_twist_JNT_1', 'Hand_twist_JNT_2', 'Hand_twist_JNT_3', 'Hand_rot_JNT', 
			'Thumb_base_JNT', 'Thumb_JNT_1', 'Thumb_JNT_2', 'Thumb_end_JNT_3', 
			'Index_JNT_1', 'Index_JNT_2', 'Index_JNT_3', 'Index_end_JNT_4', 
			'Middle_JNT_1', 'MIddle_JNT_2', 'Middle_JNT_3', 'MIddle_JNT_4',
			'Ring_JNT_1', 'Ring_JNT_2', 'Ring_JNT_3', 'Ring_end_JNT_4', 
			'Pinky_JNT_1', 'Pinky_JNT_2', 'Pinky_JNT_3', 'Pinky_end_JNT_4']

rl.add_fk_cntrls()

# create IK handles for each finger, set prefered angle + basic rotate plane solver
# add grouping for the fingers
# sometimes set preffered angle is wrong
in_ik_chain = ['Index_IK_JNT_1', 'Index_JNT_8', 'Index_JNT_9', 'Index_end_JNT_6']

for i in range(4):	
	print()
	rename_fingers(in_ik_chain, fingers[i])
	rl.create_ik_handle(in_ik_chain)
# create IK FK control

rl.ik_controls_setup() 


# the position of the controls is way off
snap_jnt = ['Index_JNT_1', 'Middle_JNT_1', 'Ring_JNT_1', 'Pinky_JNT_1']

for i in range(3):
	rl.ik_fk_switch('IK_FK_Switch'+str(i), snap_jnt[i])

# hook IK FK together
in_ik_chain = ['Index_IK_JNT_1', 'Index_JNT_8', 'Index_JNT_9', 'Index_end_JNT_6']
fk_finger_chain = ['Index_FK_JNT_1', 'Index_JNT_5', 'Index_JNT_6', 'Index_end_JNT_5']
result_finger_chain = ['Index_JNT_1', 'Index_result_JNT_2', 'Index_result_JNT_3', 'Index_end_result_JNT_4']
switch_names = ['IK_FK_Switch0', 'IK_FK_Switch1', 'IK_FK_Switch2', 'IK_FK_Switch3']

for i in range(4):
	rename_fingers(in_ik_chain, fingers[i])
	rename_fingers(fk_finger_chain, fingers[i])
	rename_fingers(result_finger_chain, fingers[i])
	rl.leg_blend(fk_finger_chain, in_ik_chain, result_finger_chain, switch_names[i])

# rewrite this
rl.sdk_ik_fk_visibility()

# create a wrist twist (adds serveral joints and hooks them up together with the result chain controls)
twist_chain = ['Hand_base_JNT', 'Hand_twist_JNT_1', 'Hand_twist_JNT_2', 'Hand_twist_JNT_3', 'Hand_rot_JNT']

rl.add_twist(twist_chain)


