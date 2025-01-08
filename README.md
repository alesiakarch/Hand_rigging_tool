# Hand_rigging_tool

This set of python scripts is used to create a hand rig, using some functionality of my rigging library,
developed for this project.

To use the scripts:

1. Drop riglib.py into your maya/scripts/ folder, usually User/Documents/maya/(version)/scripts/ or home/maya/(version)/scripts/
2. Paste hand_script.py into your script editor and execute

The Source_code folder also includes the hand_demo.ma to test the script in. 
That file contains the hand joint chain and IK_cntrls. 
The script does nothing for the skinning part of the process, but there is a hand geo available to test the rig visually. However you will need to attach skin manually.  

After the script's execution the fingers will be in the spread position, and the fk cntrl nurb circled will have to be adjusted manually. 
The joint chain is created to be optimal, however precise joint placement is very important for IK to bend correctly.