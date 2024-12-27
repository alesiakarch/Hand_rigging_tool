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
	
in_finger_chain = ['Index_JNT_1', 'Index_JNT_2', 'Index_JNT_3', 'Index_end_JNT_4']
fingers = ['Index', 'Middle', 'Ring', 'Pinky']
fk_finger_chain = []
ik_finger_chain = []
hand_jnts = ['Hand_base_JNT', 'Hand_rot_JNT', 'Thumb_base_JNT', 'Thumb_JNT_1', 'Thumb_JNT_2', 'Thumb_end_JNT_3']
snap_jnt = ['Index_IK_JNT_1', 'Middle_IK_JNT_1', 'Ring_IK_JNT_1', 'Pinky_IK_JNT_1']
result_finger_chain = ['Index_result_JNT_1', 'Index_result_JNT_2', 'Index_result_JNT_3', 'Index_end_result_JNT_4']
switch_names = ['IK_FK_Switch1', 'IK_FK_Switch2', 'IK_FK_Switch3', 'IK_FK_Switch4']
twist_chain = ['Hand_base_JNT', 'Hand_twist_JNT_1', 'Hand_twist_JNT_2', 'Hand_twist_JNT_3', 'Hand_rot_JNT']
ik_cntrl = 'Index_IK_CNTRL'



for i in range(0, len(in_finger_chain)):
    fk_finger_chain.append(in_finger_chain[i].replace('JNT','FK_JNT'))
    ik_finger_chain.append(in_finger_chain[i].replace('JNT','IK_JNT'))

print(fk_finger_chain)
print(ik_finger_chain)

# master loop that runs all the functions for each finger
rl.add_fk_cntrls(hand_jnts)
# adds twist to the hand
rl.add_twist(twist_chain)
# add orient jnt to the thumb
cmds.insertJoint('Thumb_JNT_1')
cmds.rename('joint1', 'Thumb_orient_JNT')
#rotate and freeze transforms

for i in range(4):
    rename_fingers(in_finger_chain, fingers[i])
    rename_fingers(fk_finger_chain, fingers[i])
    rename_fingers(ik_finger_chain, fingers[i])
    rename_fingers(result_finger_chain, fingers[i])
    
    string_parts = ik_cntrl.split('_', 1) 
    ik_cntrl = fingers[i] + '_' + string_parts[1]
     
    rl.duplicate_rename_joints(in_finger_chain, fk_finger_chain, ik_finger_chain)
    rl.add_fk_cntrls(fk_finger_chain)
    rl.create_ik_handle(ik_finger_chain, ik_cntrl)
    rl.ik_fk_switch('IK_FK_Switch'+str(i+1), snap_jnt[i])
    # below works only on first finger
    rl.leg_blend(fk_finger_chain, ik_finger_chain, result_finger_chain, switch_names[i])
    # add this function
    rl.sdk_ik_fk_visibility(fk_finger_chain, ik_finger_chain, ik_cntrl, switch_names[i] + '.IK_FK_Switch')
    
# add spread, curl 
cmds.select('Index_FK_JNT_1')
cmds.addAttr(longName = 'Spread', attributeType = 'float', defaultValue = 0.0, minValue = 0.0, keyable = True)
# hooks up spread
cmds.addAttr(attributeType = 'float', defaultValue = 0.0, longName = 'Master_Curl', minValue = 0.0, maxValue = 90.0, keyable = True)
# hooks up hand cntrl to finger curl
cmds.addAttr(attributeType = 'float', defaultValue = 0.0, longName = 'Curl', parent = 'Master_Curl', minValue = 0.0, maxValue = 90.0, keyable = True)
# hooks up curl for each finger

#rig done now grouping
cmds.group('Index_IK_CNTRL', 'Middle_IK_CNTRL', 'Ring_IK_CNTRL', 'Pinky_IK_CNTRL', name = 'Hand_CNTRL_GRP')
cmds.group('Hand_base_JNT', name = 'Hand_JNT_GRP_DO_NOT_TOUCH')
cmds.group('Hand_JNT_GRP_DO_NOT_TOUCH', 'Hand_CNTRL_GRP', 'Hand_GEO', name = 'Hand_Rig')

    