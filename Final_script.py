import sys
import maya.cmds as cmds 
sys.path.insert(0, cmds.workspace(expandName = 'scripts'))
sys.path.insert(0, cmds.workspace(expandName = 'scenes'))

'''
    Before applying the script
    1. Create the joint chain and rename it as desired
    2. Orient them
    3. Make sure the rotations are zeroed out
    4. Import the IK controld for your leg
    5. Create 4 locator for futer footroll and place them accordingly (toe, heel, inner, outer)
'''

'''
#creates 4 locators
cmds.spaceLocator(n='R_Leg_Heel_LOC', p=(0,0,0))
cmds.spaceLocator(n='R_Leg_outer_LOC', p=(0,0,0))
cmds.spaceLocator(n='R_Leg_inner_LOC', p=(0,0,0))
cmds.spaceLocator(n='R_Leg_Toe_LOC', p=(0,0,0))
'''

'''
    In the Demo file the locators are created and placed for you and ik controls are also imported
'''

def duplicate_rename_joints(in_chain=['R_Leg_Femur_result_JNT',
                                      'R_Leg_Thigh_result_JNT1',
                                      'R_Leg_Knee_result_JNT1',
                                      'R_Leg_Ankle_result_JNT1',
                                      'R_Leg_Heel_result_JNT1',
                                      'R_Leg_Toe_result_JNT1'],
                           out_chain=['R_Leg_Femur_FK_JNT',
                                      'R_Leg_Thigh_FK_JNT',
                                      'R_Leg_Knee_FK_JNT',
                                      'R_Leg_Ankle_FK_JNT',
                                      'R_Leg_Heel_FK_JNT',
                                      'R_Leg_Toe_FK_JNT']):
        '''
        duplicate and rename joitns

        in_chain : names of input joints
        out_chain : names of output joints

        On Exit:
        duplicates the chain twice
        renames input joints to output joints

        '''
        #duplicates fk chain
        cmds.duplicate(in_chain[0], name=out_chain[0], renameChildren=True)
        for i in range(1, len(in_chain)):
            cmds.rename (in_chain[i], out_chain[i])
            
        #duplicates ik chain
        cmds.duplicate(in_chain[0], name=out_chain[0].replace('FK','IK'), renameChildren=True)
        for i in range(1, len(in_chain)):
            cmds.rename (in_chain[i], out_chain[i].replace('FK','IK'))

def add_FK_CNTRLs (out_chain=['R_Leg_Femur_FK_JNT',
                          'R_Leg_Thigh_FK_JNT',
                          'R_Leg_Knee_FK_JNT',
                          'R_Leg_Ankle_FK_JNT',
                          'R_Leg_Heel_FK_JNT',
                          'R_Leg_Toe_FK_JNT'],
                    circle_suffix='_CNTRL'):
                              
    ''' 
    add FK controls

    out_chain : names of FK joints
    circle_suffix : name of suffix for FK controls

    On Exit:
    creates NURBs circles for (the number of joints-1), 
    renames them as FK_CNTRLs,
    then parents their shapes to the FK joints and deletes the duplicate

    '''
    #creates fk controls
    for i in range(0,len(out_chain)-1):
        control_name=out_chain[i]+circle_suffix
        cmds.circle(name=control_name,radius=15)
        cmds.parent (control_name+'Shape', out_chain[i], add=True, shape=True)
        cmds.delete (control_name)
 
def create_ik_handles(ik_jnts=['R_Leg_Femur_IK_JNT',
                               'R_Leg_Thigh_IK_JNT',
                               'R_Leg_Ankle_IK_JNT',
                               'R_Leg_Heel_IK_JNT',
                               'R_Leg_Toe_IK_JNT'],
                      ik_suffix='_Handle',
                      effector_suffix='_effector'):
   
    '''
    create IK handles

    ik_jnts : names of IK joints
    ik_suffix: name of suffix for IK handles
    effector_suffix : name of suffix for the effectors

    On Exit:
    selects 2 necessary joints,
    creates a basic rotate plain ik handle,
    renames the effector,

    '''
    #creates ik handles
    for i in range (0,len(ik_jnts)-1):
        handle_name=ik_jnts[i]+ik_suffix
        effector_name=handle_name+effector_suffix
        cmds.select(ik_jnts[i],ik_jnts[i+1])
        cmds.ikHandle(name=handle_name)
        cmds.rename('effector1',effector_name)
        
def ik_controls_setup(ik_cntrls=['R_Leg_IK_Top_CNTRL','R_Leg_IK_CNTRL'], 
                      ik_jnts=['R_Leg_Femur_IK_JNT','R_Leg_Heel_IK_JNT'],
                      ik_handles=['R_Leg_Femur_IK_JNT_Handle',
                                  'R_Leg_Thigh_IK_JNT_Handle',
                                  'R_Leg_Ankle_IK_JNT_Handle',
                                  'R_Leg_Heel_IK_JNT_Handle'],
                      top_offset_grp='R_Leg_IK_Top_CNTRL_Offset_GRP'):
                          
    '''
    ik controls setup

    ik_cntrls : names of IK controls
    ik_jnts : names of IK joints
    ik_handles : names of IK handles
    top_offset_grp : name of the offset group on the top control

    On Exit: 
    moves IK controls to their respective joints 
    freezes transformations
    parents the top ik handle under the top control
    parents the leg ik handles under the foot control
    creates an offset group for the top ik control

    '''

    #places ik controls into place
    for i in range (0, len(ik_cntrls)):
        cmds.matchTransform(ik_cntrls[i],ik_jnts[i], pos=1)
        cmds.makeIdentity(ik_cntrls[i], apply=True, t=1, r=1, s=1, n=0)
    #parents ik handles to respective controls    
    cmds.parent(ik_handles[1:],ik_cntrls[1])
    cmds.parent(ik_handles[0],ik_cntrls[0])
    
    #creates an offset group for the top control
    cmds.group(ik_cntrls[0], n=top_offset_grp)
    cmds.matchTransform(top_offset_grp, ik_cntrls[0], piv=1)

def no_flip_knee(locators=['R_Hip_Loc',
                           'R_Heel_follow_Loc',
                           'R_Mid_Loc'],
                 knee_loc='R_Knee_LOC',
                 ik_chain=['R_Leg_Thigh_IK_JNT',
                           'R_Leg_Ankle_IK_JNT',
                           'R_Leg_Knee_IK_JNT'],
                ik_cntrl_name='R_Leg_IK_CNTRL',
                ik_handle_name='R_Leg_Thigh_IK_JNT_Handle'):
    '''
     no flip knee setup

     locators : names of the locators
     ik_chain : names of IK joints
     knee_loc : name of the knee locator
     ik_cntrl_name : name of the IK control
     ik_handle_name : name of the main IK handle

     On Exit:

     part 1:
     creates a Knee locator
     snaps to the knee
     offsets it behind the knee
     freezes its transformations
     makes pole vector constraint

     part 2:
     creates 3 locators for the no flip setup
     snaps them to the respective joints
     freezes its transformations
     parents bottom and knee locators to the ik control
     makes point constraint for the mid_loc betwee the top_loc and bottom_loc
     makes aim constraint from bottom to top locator
     makes orient constraint from top to mid locator
     makes parent constraint from mid to knee locator with offset 
     
    '''       
                  
    #creates poleVector knee setup
    cmds.spaceLocator(n=knee_loc, p=(0,0,0))
    cmds.matchTransform(knee_loc,ik_chain[2], pos=1)
    cmds.setAttr(knee_loc+'.translateX', -26)
    cmds.makeIdentity(knee_loc, apply=True, t=1, r=1, s=1, n=0)
    cmds.poleVectorConstraint(knee_loc,ik_handle_name)
    
    #creates noFlip setup locators
    for i in range(0, len(locators)):
        cmds.spaceLocator(n=locators[i], p=(0,0,0))
        cmds.matchTransform(locators[i],ik_chain[i], pos=1)
        cmds.makeIdentity(locators[i], apply=True, t=1, r=1, s=1, n=0)

    #noFlip setup with constraints        
    cmds.parent(locators[1], knee_loc, ik_cntrl_name)            
    cmds.pointConstraint(locators[0],locators[1],locators[2])           
    cmds.aimConstraint(locators[1],locators[0], u=(0.0, 0.0, -1.0), aim=(0.0, 1.0, 0.0), wut='objectrotation', wuo=locators[1], wu=(0.0, 0.0, 1.0))
    cmds.orientConstraint(locators[0],locators[2]) 
    cmds.parentConstraint(locators[2], knee_loc, mo=1)      

def ik_fk_switch(switch_name='R_Leg_Switch_CNTRL',
                 snap_jnt='R_Leg_Ankle_IK_JNT'):

    '''
    ik fk switch

    switch_name : name of the ikfk switch circle
    snap_jnt : name of the joint to snap the switch control, usually ankle joint

    On Exit:

    creates a circle and names as ik fk control
    snaps to the ankle joint
    offsets the control behind the knee
    freezes transformations
    adds ik fk switch attribute
    
    '''

    #creates ik fk switch control
    cmds.circle(name=switch_name, normal=(0,1,0),radius=3)
    cmds.matchTransform(switch_name,snap_jnt, pos=1)
    cmds.setAttr(switch_name+'.translateX', -20)
    cmds.makeIdentity(switch_name, apply=True, t=1, r=1, s=1, n=0)
    cmds.addAttr(longName='IK_FK_Switch',attributeType='float', keyable=1, defaultValue=0, minValue=0, maxValue=1)
 
def leg_blend(fk_chain=['R_Leg_Femur_FK_JNT',
                        'R_Leg_Thigh_FK_JNT',
                        'R_Leg_Knee_FK_JNT',
                        'R_Leg_Ankle_FK_JNT',
                        'R_Leg_Heel_FK_JNT',
                        'R_Leg_Toe_FK_JNT'],
              ik_chain=['R_Leg_Femur_IK_JNT',
                         'R_Leg_Thigh_IK_JNT',
                         'R_Leg_Knee_IK_JNT',
                         'R_Leg_Ankle_IK_JNT',
                         'R_Leg_Heel_IK_JNT',
                         'R_Leg_Toe_IK_JNT'],
              blends_names=['R_Leg_Femur_IK_FK_Blend',
                            'R_Leg_Thigh_IK_FK_Blend',
                            'R_Leg_Knee_IK_FK_Blend',
                            'R_Leg_Ankle_IK_FK_Blend',
                            'R_Leg_Heel_IK_FK_Blend',
                            'R_Leg_Toe_IK_FK_Blend'],
              result_chain=['R_Leg_Femur_result_JNT',
                            'R_Leg_Thigh_result_JNT',
                            'R_Leg_Knee_result_JNT',
                            'R_Leg_Ankle_result_JNT',
                            'R_Leg_Heel_result_JNT',
                            'R_Leg_Toe_result_JNT'],
              switch_cntrl='R_Leg_Switch_CNTRL'):
    '''
    leg blend

    fk_chain : names of fk joints
    ik_chain : nams of ik joints
    blends_names : names of blend colours nodes
    result_chain : names of result joints
    switch_cntrl : name of switch control

    On Exit:

    creates blendColors nodes for translation and rotation,         
    connects IK and FK rotations and translations to the blend nodes,          
    connects the blend nodes to translation and rotatoin of result joints,           
    connects blender attribute to the IK FK Switch

    '''                         
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

def parent_footroll_locators(locators=['R_Leg_Heel_LOC',
                                       'R_Leg_outer_LOC',
                                       'R_Leg_inner_LOC',
                                       'R_Leg_Toe_LOC'],
                           ik_handles=['R_Leg_Thigh_IK_JNT_Handle',
                                       'R_Leg_Ankle_IK_JNT_Handle',
                                       'R_Leg_Heel_IK_JNT_Handle'],
                        ik_cntrl_name='R_Leg_IK_CNTRL'):                                        

    '''
    parent footroll locators

    locators : names of footroll locators
    ik_handles : names of IK handles
    ik_cntrl_name : name of the ik control

    On Exit:

    parents locator in the footroll hierarchy
    parents the locators to the ik control
    parents ik handles to the respective locators
    
    '''

    #parent locators to each other
    for i in range(1,len(locators)):
        cmds.parent(locators[i],locators[i-1])

    #parents locators to ik control   
    cmds.parent(locators[0], ik_cntrl_name)

    #parenting the ik handles
    cmds.parent(ik_handles[2],locators[2])
    cmds.parent(ik_handles[0],ik_handles[1],locators[3])

def footroll(attributes=['Roll',
                         'Tilt',
                         'Toe_Spin'],
             ik_cntrl='R_Leg_IK_CNTRL',
             clamp_names=['R_Heel_rot_Clamp','R_Toe_rot_Clamp'],
             loc_names=['R_Leg_Heel_LOC','R_Leg_Toe_LOC','R_Leg_outer_LOC','R_Leg_inner_LOC']):

    '''
    footroll

    attributes : names of the attributes to be created
    ik_cntrl : name of the ik control
    clamp_names : names of the clamp nodes to be created
    loc_names : names of the locator used for a footroll

    On Exit:

    creates roll, tilt and toe_spin attributes on the ik control
    sets up roll attribute backwards with clamp nodes
    sets up roll attribute forwards with clamp nodes
    sets up toe_spin attribute by connecting the rotate attribute
    sets up tilt attribute with set driven key

    '''
    #add foot attributes
    for i in range (0, len(attributes)):
        cmds.select(ik_cntrl)
        cmds.addAttr(longName=attributes[i], attributeType='float', keyable=1, defaultValue=0)
    
    #roll attr
    cmds.createNode('clamp', n=clamp_names[0])
    cmds.connectAttr(ik_cntrl+'.Roll',clamp_names[0]+'.inputR')
    cmds.setAttr(clamp_names[0]+'.maxR', 90)
    cmds.connectAttr(clamp_names[0]+'.outputR',loc_names[0]+'.rotateZ')

    #toe lift in the footroll
    cmds.createNode('clamp', n=clamp_names[1])
    cmds.connectAttr(ik_cntrl+'.Roll',clamp_names[1]+'.inputR')
    cmds.setAttr(clamp_names[1]+'.minR', -90)
    cmds.connectAttr(clamp_names[1]+'.outputR',loc_names[1]+'.rotateZ')

    #toe spin attr
    cmds.connectAttr(ik_cntrl+'.Toe_Spin',loc_names[1]+'.rotateY')

    #tilt attr with SDK
    cmds.setDrivenKeyframe(loc_names[2]+'.rotateX', loc_names[3]+'.rotateX', cd=ik_cntrl+'.Tilt')
    cmds.setAttr(ik_cntrl+'.Tilt', 90)
    cmds.setAttr(loc_names[2]+'.rotateX', 90)
    cmds.setDrivenKeyframe(loc_names[2]+'.rotateX', cd=ik_cntrl+'.Tilt')
    cmds.setAttr(ik_cntrl+'.Tilt', -90)
    cmds.setAttr(loc_names[3]+'.rotateX', -90)
    cmds.setDrivenKeyframe(loc_names[3]+'.rotateX', cd=ik_cntrl+'.Tilt')
    cmds.setAttr(ik_cntrl+'.Tilt', 0)
    
def sdk_ik_fk_visibility (fk_chain=['R_Leg_Femur_FK_JNT.visibility',
                                    'R_Leg_Thigh_FK_JNT.visibility',
                                    'R_Leg_Knee_FK_JNT.visibility',
                                    'R_Leg_Ankle_FK_JNT.visibility',
                                    'R_Leg_Heel_FK_JNT.visibility',
                                    'R_Leg_Toe_FK_JNT.visibility'],
                          ik_chain=['R_Leg_Femur_IK_JNT.visibility',
                                    'R_Leg_Thigh_IK_JNT.visibility',
                                    'R_Leg_Knee_IK_JNT.visibility',
                                    'R_Leg_Ankle_IK_JNT.visibility',
                                    'R_Leg_Heel_IK_JNT.visibility',
                                    'R_Leg_Toe_IK_JNT.visibility'],
                         ik_cntrls=['R_Leg_IK_CNTRL.visibility',
                                    'R_Leg_IK_Top_CNTRL.visibility'],
                        knee_locator='R_Knee_LOC.visibility',
                        ik_fk_switch='R_Leg_Switch_CNTRL.IK_FK_Switch'): 
    '''
    visibility set driven key

    fk_chain : names of fk joints with visibility suffix
    ik_chain : names of ik joints with visibility suffix
    ik_cntrls : names of ik controls with visibility suffix
    knee_locator : name of the knee locator with visibility suffix
    ik_fk_switch : names of ik fk switch control with ik fk switch attribute

    On Exit:

    makes set driven keys on joint chains and controls to be hidden in the respective mode
     
    '''                   

    #makes visibility set drive keys
    for i in range(0,len(fk_chain)):
        cmds.setAttr(ik_fk_switch, 0)
        cmds.setAttr(ik_cntrls[0], 1)
        cmds.setAttr(ik_cntrls[1], 1)
        cmds.setAttr(fk_chain[i], 0)
        cmds.setAttr(ik_chain[i], 1)
        cmds.setAttr(knee_locator, 1)
        cmds.setDrivenKeyframe(fk_chain[i], ik_chain[i], ik_cntrls[0], knee_locator, ik_cntrls[1], cd=ik_fk_switch)
        cmds.setAttr(ik_fk_switch, 1)
        cmds.setAttr(ik_cntrls[0], 0)
        cmds.setAttr(ik_cntrls[1], 0)
        cmds.setAttr(fk_chain[i], 1)
        cmds.setAttr(ik_chain[i], 0)
        cmds.setAttr(knee_locator, 0)
        cmds.setDrivenKeyframe(fk_chain[i], ik_chain[i], ik_cntrls[0], knee_locator, ik_cntrls[1], cd=ik_fk_switch)

def leg_rig(result_grp_name='R_Leg_Femur_result_JNT',
            ik_grp_name='R_Leg_Femur_IK_JNT',
            fk_grp_name='R_Leg_Femur_FK_JNT',
            hip_loc_grp_name='R_Hip_Loc',
            mid_loc_grp_name='R_Mid_Loc',
            ik_cntrl_grp_name='R_Leg_IK_CNTRL',
            offset_grp_name='R_Leg_IK_Top_CNTRL_Offset_GRP',
            switch_grp_name='R_Leg_Switch_CNTRL',
             main_grp_name='R_Leg_GRP'):

    '''
    leg rig

    result_grp_name : name of the top result joint
    ik_grp_name : name of the top ik joint
    fk_grp_name : name of the top fk joint
    hip_loc_grp_name : name of the hip locator used for no-flip knee
    mid_loc_grp_name :name of the mid locator used for no-flip knee
    ik_cntrl_grp_name : name of the ik control
    offset_grp_name : name of the offset group
    switch_grp_name : name of the switch control
    main_grp_name : name of the final leg group

    On Exit:

    executes all previous functions

    groups the created hierarchy into R_Leg_GRP

    '''

    #Duplicate the join chain 2 times and replace the result_ with IK_ and FK_
    duplicate_rename_joints() 

    #Making FK leg controls
    #Create as many nurb circles as the joints-1 and scale them to be manipulative later
    add_FK_CNTRLs()

    #Create several IK handles on the IK leg chain. 
    create_ik_handles()

    #snap controls to the respected joints
    ik_controls_setup()

    #creates no flip knee set up with the triangle locators solution
    no_flip_knee()

    #creates ik fk switch
    ik_fk_switch()

    #hook ip the joints
    leg_blend()

    #parent locators to each other and foot control
    parent_footroll_locators()

    #set up footroll for the ik leg
    footroll()

    #SDK of the visibility of ik fk joints
    sdk_ik_fk_visibility()
    
    cmds.group(result_grp_name,
                ik_grp_name,
                fk_grp_name,
                hip_loc_grp_name,
                mid_loc_grp_name,
                ik_cntrl_grp_name,
                offset_grp_name,
                switch_grp_name,                      
                n=main_grp_name)

leg_rig()

'''

After applying the script:
1. Manipulate the FK controls in place
2. Skin the bones to the mesh

'''