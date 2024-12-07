import sys
import maya.cmds as cmds 
import riglib as rl
sys.path.insert(0, cmds.workspace(expandName = 'scripts'))
sys.path.insert(0, cmds.workspace(expandName = 'scenes'))

rl.duplicate_rename_joints()