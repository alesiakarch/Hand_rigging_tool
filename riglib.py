import sys
import maya.cmds as cmds 
sys.path.insert(0, cmds.workspace(expandName = 'scripts'))
sys.path.insert(0, cmds.workspace(expandName = 'scenes'))

def duplicate_rename_joints(in_chain, fk_chain, ik_chain): # duplicates joints to prepare for the IK/FK setup
    '''
    duplicate and rename joitns

    in_chain : list names of input joints
    fk_chain : list of names to assign to a created fk chain
    ik_chain : list of names to assign to a created ik chain

    On Exit:
    duplicates the chain twice
    renames input joints to result joints
    groups 3 jnt chains 

    '''
    #duplicates fk ik chain and reparents joints in the correct order to keep naming convention

    for i in range(0, len(in_chain)):

        cmds.duplicate(in_chain[i], name=fk_chain[i], parentOnly=True)
        cmds.duplicate(in_chain[i], name=ik_chain[i], parentOnly=True)
        
        if i > 0:
            cmds.parent(fk_chain[i], fk_chain[i-1])
            cmds.parent(ik_chain[i], ik_chain[i-1])
        else:
            continue

    # renames the in chain into a result chain
    for i in range(0, len(in_chain)):
        cmds.rename (in_chain[i], in_chain[i].replace('JNT','result_JNT'))

    #groups the chains into a name_GRP
    cmds.group(in_chain[0].replace('JNT','result_JNT'),
               fk_chain[0], ik_chain[0], 
               name = in_chain[0].replace('JNT','GRP'))

def add_fk_cntrls (fk_chain, circle_suffix='_CNTRL'): # parents NURBS circles to the FK joint chain
                              
    ''' 
    add FK controls

    fk_chain : names of FK joints
    circle_suffix : name of suffix for FK controls

    On Exit:
    creates NURBs circles for (the number of joints-1), 
    renames them as FK_CNTRLs,
    then parents their shapes to the FK joints and deletes the duplicate

    '''
    #creates fk controls
    for i in range(0, len(fk_chain) - 1):  
        control_name = fk_chain[i] + circle_suffix
        cmds.circle(name = control_name, radius = 2)
        cmds.parent (control_name + 'Shape', fk_chain[i], add = True, shape = True)
        cmds.delete (control_name)   

def create_ik_handle(ik_chain, ik_cntrl, joint_orientation = 'xyz', up_vector = 'yup', ik_suffix='_Handle', effector_suffix='_effector', ): # creates IK handle 
   
    '''
    create IK handles

    ik_chain : names of IK joints
    ik_cntrl : name of IK controls to parent the handle to
    joint_orientation : string of what to orient the joints to
    up_vector : string of where should the up vector point in the IK handle settings
    ik_suffix: name of suffix for IK handles
    effector_suffix : name of suffix for the effectors

    On Exit:
    selects 2 necessary joints,
    sets prefered angle
    creates a rotate plain ik handle,
    renames the effector,
    parents the handle to IK control

    '''
    # select orient joints # set prefered angle
    cmds.joint(ik_chain, edit = True, orientJoint = joint_orientation, sao = up_vector, setPreferredAngles = True)
   
    # create rotate plane solver IK handle, select first and last jnt
    handle_name=ik_chain[0] + ik_suffix
    cmds.select(ik_chain[0], ik_chain[-1])
    cmds.ikHandle(name = handle_name)
    effector_name = handle_name + effector_suffix
    cmds.rename('effector1',effector_name)
    cmds.matchTransform(ik_cntrl, ik_chain[-1])
    cmds.makeIdentity(ik_cntrl, apply = True)
    cmds.parent(handle_name, ik_cntrl)

def ik_fk_switch(switch_name, snap_jnt): # create IK/FK control

    '''
    ik fk switch

    switch_name : name of the ikfk switch circle
    snap_jnt : name of the joint to snap the switch control

    On Exit:

    creates a circle and names as ik fk control
    snaps to the snap joint
    offsets the control 
    freezes transformations
    adds ik fk switch attribute
    
    '''

    #creates ik fk switch control
    cmds.circle(name=switch_name, normal=(0,1,0),radius=3)
    cmds.matchTransform(switch_name,snap_jnt, pos=1)
    cmds.setAttr(switch_name+'.translateX', -10)
    cmds.makeIdentity(switch_name, apply=True, t=1, r=1, s=1, n=0)
    cmds.addAttr(longName='IK_FK_Switch',attributeType='float', keyable=1, defaultValue=0, minValue=0, maxValue=1)

def leg_blend(fk_chain, ik_chain, result_chain, switch_cntrl): # hooks up IK/FK to the switch control
    
    '''
    leg blend

    fk_chain : names of fk joints
    ik_chain : nams of ik joints
    result_chain : names of result joints
    switch_cntrl : name of switch control

    On Exit:

    generated blend_names,
    creates blendColors nodes for translation and rotation,         
    connects IK and FK rotations and translations to the blend nodes,          
    connects the blend nodes to translation and rotatoin of result joints,           
    connects blender attribute to the IK FK Switch

    '''
    blends_names = []
    for i in range (0, len(result_chain)):
        blends_names.append(result_chain[i].replace('result_JNT', 'IK_FK_Blend'))                        



    for i in range (0,len(fk_chain)):
        
        #creates blend nodes for translation and rotation of the joint chains
        cmds.createNode('blendColors', n=blends_names[i]+'_Rot')
        cmds.createNode('blendColors', n=blends_names[i]+'_Trans')
        
        #connects fk
        cmds.connectAttr(fk_chain[i]+'.rotate',blends_names[i]+'_Rot'+'.color1', f=1)
       
        cmds.connectAttr(fk_chain[i]+'.translate',blends_names[i]+'_Trans'+'.color1', f=1)
        
        #connects ik
        cmds.connectAttr(ik_chain[i]+'.rotate',blends_names[i]+'_Rot'+'.color2', f=1)
        
        cmds.connectAttr(ik_chain[i]+'.translate',blends_names[i]+'_Trans'+'.color2', f=1)
        
       #connects result 
        cmds.connectAttr(blends_names[i]+'_Rot'+'.output', result_chain[i]+'.rotate', f=1)
        
        cmds.connectAttr(blends_names[i]+'_Trans'+'.output',result_chain[i]+'.translate', f=1)
        
        #connect blender attr to switch attr
        cmds.connectAttr(switch_cntrl+'.IK_FK_Switch', blends_names[i]+'_Rot'+'.blender', f=1)
        
        cmds.connectAttr(switch_cntrl+'.IK_FK_Switch', blends_names[i]+'_Trans'+'.blender', f=1)

def sdk_ik_fk_visibility (fk_chain, ik_chain, ik_cntrls, ik_fk_switch='R_Leg_Switch_CNTRL' + '.IK_FK_Switch', knee_locator = ' '):  # sets IK/FK visibility
    '''
    visibility set driven key

    fk_chain : names of fk joints with visibility suffix
    ik_chain : names of ik joints with visibility suffix
    ik_cntrls : names of ik controls with visibility suffix
    knee_locator : name of the pole vector locator if needed, with visibility suffix
    ik_fk_switch : names of ik fk switch control with ik fk switch attribute

    On Exit:
    generates visibility chains for ik and fk
    makes set driven keys on joint chains and controls to be hidden in the respective mode
     
    '''     
    # add visibility to the lists 
    fk_vis_chain = []
    ik_vis_chain = []

    for i in range(0, len(fk_chain)):
        fk_vis_chain.append(fk_chain[i] + '.visibility')     
        ik_vis_chain.append(ik_chain[i] + '.visibility')     

    ik_cntrls = ik_cntrls + '.visibility'

    # makes visibility set drive keys
    for i in range(0,len(fk_chain)):
        cmds.setAttr(ik_fk_switch, 0)
        cmds.setAttr(ik_cntrls, 1)
        cmds.setAttr(fk_vis_chain[i], 0)
        cmds.setAttr(ik_vis_chain[i], 1)
        if knee_locator != ' ':
            cmds.setAttr(knee_locator, 1)
            cmds.setDrivenKeyframe(fk_vis_chain[i], ik_vis_chain[i], ik_cntrls, knee_locator, cd=ik_fk_switch)
        else:
            cmds.setDrivenKeyframe(fk_vis_chain[i], ik_vis_chain[i], ik_cntrls, cd=ik_fk_switch)

        cmds.setAttr(ik_fk_switch, 1)
        cmds.setAttr(ik_cntrls, 0)
        cmds.setAttr(fk_vis_chain[i], 1)
        cmds.setAttr(ik_vis_chain[i], 0)
        if knee_locator != ' ':
            cmds.setAttr(knee_locator, 0)
            cmds.setDrivenKeyframe(fk_vis_chain[i], ik_vis_chain[i], ik_cntrls, knee_locator, cd=ik_fk_switch)
        else:
            cmds.setDrivenKeyframe(fk_vis_chain[i], ik_vis_chain[i], ik_cntrls, cd=ik_fk_switch)

def add_twist(jnt_chain): # adds twist to the joint chain
    '''
    add twist

    jnt_chain : names of joint chain, from first to last, with the twist jnts in the middle

    On Exit:

    adds mulpiply divides to hook up the rotation of the joints to the hand joint

    '''
    # take the hand joint and the amount of twist joints
    # hook each up to a multiplyDivide node
    # set the multiplyDivide node to miltiply but 100/amount of twist joints
    for i in range (1, len(jnt_chain)-1):
        multDiv = cmds.shadingNode('multiplyDivide', asUtility = True) # create multiplyDivide
        cmds.connectAttr(jnt_chain[-1]+'.rotateX', multDiv+'.input1X') # connect multDiv to master joint
        cmds.connectAttr(multDiv+'.outputX', jnt_chain[i]+'.rotateX') # connect the twist joint to multDiv output
        weight = i * (1/(len(jnt_chain)-1)) # calculate weight for each twist joint
        cmds.setAttr(multDiv+'.input2X', weight) 
