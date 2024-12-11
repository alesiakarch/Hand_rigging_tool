import sys
import maya.cmds as cmds 
import riglib as rl
sys.path.insert(0, cmds.workspace(expandName = 'scripts'))
sys.path.insert(0, cmds.workspace(expandName = 'scenes'))

# duplicate rename to set up joing chains
rl.duplicate_rename_joints()

# parent fk controls
rl.add_fkFK_cntrls()

# create IK handles for each finger, set prefered angle + basic rotate plane solver (fingers somewhat work but still twist uncontrollably)
rl.create_ik_handle()

# create IK FK control
rl.ik_fk_switch()

# hook IK FK together
rl.leg_blend()
rl.sdk_ik_fk_visibility()
# create a wrist twist (adds serveral joints and hooks them up together with the result chain controls)

