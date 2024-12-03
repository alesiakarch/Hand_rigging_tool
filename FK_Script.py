
def add_FK_CNTRLs (out_chain = ['Wrist_JNT', 'Hand_Base_JNT','Index_Base_JNT', 'Index_JNT1', 'Index_JNT2', 					'Middle_Base_JNT', 'Middle_JNT1', 'Middle_JNT2',
			  	'Ring_Base_JNT', 'Ring_JNT1', 'Ring_JNT2', 'Pinky_Base_JNT', 'Pinky_JNT1', 					'Pinky_JNT2', 'Thumb_Base_JNT', 'Thumb_JNT1', 'Thumb_Tip_JNT2'],
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
        
add_FK_CNTRLs()
