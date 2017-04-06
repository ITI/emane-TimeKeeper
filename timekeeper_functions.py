#
# File  : timekeeper_functions.py
# 
# Brief : Exposes TimeKeeper API in python
#
# authors : Vignesh Babu
#


import os
from signal import SIGSTOP, SIGCONT
import time
import subprocess
import libs.gettimepid as gpd
from libs.gettimepid import gettimepid

TIMEKEEPER_FILE_NAME = "/proc/dilation/status"
DILATE = 'A'
DILATE_ALL = 'B'
FREEZE_OR_UNFREEZE = 'C'
FREEZE_OR_UNFREEZE_ALL = 'D'
LEAP = 'E'

ADD_TO_EXP_CBE = 'F'
ADD_TO_EXP_CS = 'G'
SYNC_AND_FREEZE = 'H'
START_EXP = 'I'
SET_INTERVAL = 'J'
PROGRESS = 'K'
FIX_TIMELINE = 'L'
RESET = 'M'
STOP_EXP = 'N'
SET_CBE_EXP_TIMESLICE = 'T'
SET_NETDEVICE_OWNER  = 'U'





def is_root() :

	if os.geteuid() == 0 :
		return 1
	print "Needs to be run as root"
	return 0


def is_Module_Loaded() :

	if os.path.isfile(TIMEKEEPER_FILE_NAME) == True:
		return 1
	else :
		print "Timekeeper module is not loaded"
		return 0


# Associates the given pid with a net_device
def set_netdevice_owner(pid,dev_name) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		print "ERROR in Set Netdevice Owner. TimeKeeper is not loaded!"
		return -1
	cmd = SET_NETDEVICE_OWNER + "," + str(pid) + "," + str(dev_name)

	return send_to_timekeeper(cmd)




# Converts the double into a integer, makes computation easier in kernel land
# ie .5 is converted to -2000, 2 to 2000

def fixDilation(dilation) :
        
	dil = 0

	if dilation < 0 :
		printf("Negative dilation does not make sense\n");
		return -1
        
	if dilation < 1.0 and dilation > 0.0 :
		dil = (int)((1/dilation)*1000.0)
		dil = dil*-1
        
	elif dilation == 1.0 or dilation == -1.0 :
                dil = 0
        
        else :
                dil = (int)(dilation*1000.0)
        
        return dil;


def getpidfromname(lxcname) :

	my_pid = os.getpid()
	pid = -1
	temp_file = "/tmp/" + str(my_pid) + "_timekeeper.txt"

	# For different versions of LXCs
	command = "lxc-info -n %s | grep PID | tr -s ' ' | cut -d ' ' -f 2 > %s" % (lxcname,temp_file)
	os.system(command)
	

	with open(temp_file,"r") as f :
		pidstr = f.read()
		if pidstr != "" :
			pid = int(pidstr)
	if pid == -1 :
		command  = "lxc-info -n %s | grep pid | tr -s ' ' | cut -d ' ' -f 2 > %s" % (lxcname,temp_file)
        	os.system(command)
		with open(temp_file,"r") as f :
	                pidstr = f.read()
        	        if pidstr != "" :
                	        pid = int(pidstr)

	
	
	os.remove(temp_file)
	
	return pid

def send_to_timekeeper(cmd) :

	if is_root()== 0 or is_Module_Loaded() == 0 :
		print "ERROR sending cmd to timekeeper"
		return -1

	with open(TIMEKEEPER_FILE_NAME,"w") as f :
		f.write(cmd)
	return 1

# timeslice in nanosecs
def set_cbe_experiment_timeslice(timeslice) :


	if is_root() == 0 or is_Module_Loaded() == 0 :
		print "ERROR setting timeslice value"
		return -1
	
	#timeslice = int(timeslice/1000000)
	cmd = SET_CBE_EXP_TIMESLICE + "," + str(timeslice)

	return send_to_timekeeper(cmd)


#
#Given a pid, add that container to a CBE experiment.
#

def addToExp(pid) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		return -1 
	cmd = ADD_TO_EXP_CBE + "," + str(pid)
	return send_to_timekeeper(cmd)



#
#Starts a CBE Experiment
#

def startExp():

	if is_root() == 0 or is_Module_Loaded() == 0 :
		print "ERROR starting CBE Experiment"
		return -1
	cmd = START_EXP
	return send_to_timekeeper(cmd)


#
#Given all Pids added to experiment, will set all their virtual times to be the same, then freeze them all (CBE and CS)
#

def synchronizeAndFreeze() :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		print "ERROR in Synchronize and Freeze"
		return -1
	cmd = SYNC_AND_FREEZE
	return send_to_timekeeper(cmd)





#
#Stop a running experiment (CBE or CS) **Do not call stopExp if you are waiting for a s3fProgress to return!!**
#

def stopExp() :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		print "ERROR in Synchronize and Freeze"
		return -1
	cmd = STOP_EXP
	return send_to_timekeeper(cmd)



#
#Sets the TDF of the given pid
#

def dilate(pid,dilation) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		print "ERROR in setting dilation for pid :", pid
		return -1
	dil = fixDilation(dilation)
	if dil == - 1 :
		return - 1
	elif dil < 0 :
		cmd = DILATE + "," + str(pid) + ",1," + str(-1*dil)
	else :
		cmd = DILATE + "," + str(pid) + "," + str(dil)

	return send_to_timekeeper(cmd)

#
# Will set the TDF of a LXC and all of its children
#

def dilate_all(pid,dilation) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		print "ERROR in setting dilation for pid :", pid
		return -1
	dil = fixDilation(dilation)
	if dil == - 1 :
		return - 1
	elif dil < 0 :
		cmd = DILATE_ALL + "," + str(pid) + ",1," + str(-1*dil)
	else :
		cmd = DILATE_ALL + "," + str(pid) + "," + str(dil)

	return send_to_timekeeper(cmd)


#
# Takes an integer (pid of the process). This function will essentially 'freeze' the
# time of the process. It does this by sending a sigstop signal to the process.
#

def freeze(pid) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		return -1
	else :
		cmd = FREEZE_OR_UNFREEZE + "," + str(pid) + "," + SIGSTOP
		return send_to_timekeeper(cmd)

	

#
# Takes an integer (pid of the process). This function will unfreeze the process.
# When the process is unfrozen, it will think that no time has passed, and will
# continue doing whatever it was doing before it was frozen.
#

def unfreeze(pid) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		return -1
	cmd = FREEZE_OR_UNFREEZE + "," + str(pid) + "," +SIGCONT
	return send_to_timekeeper(cmd)




#
# Same as freeze, except that it will freeze the process as well as all of its children.
#

def freeze_all(pid) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		return -1
	else :
		cmd = FREEZE_OR_UNFREEZE_ALL + "," + str(pid) + "," + SIGSTOP
		return send_to_timekeeper(cmd)

	


# 
# Same as unfreeze, except that it will unfreeze the process as well as all of its children.
#

def unfreeze(pid) :

	if is_root() == 0 or is_Module_Loaded() == 0 :
		return -1
	cmd = FREEZE_OR_UNFREEZE_ALL + "," + str(pid) + "," +SIGCONT
	return send_to_timekeeper(cmd)


		
def get_current_virtual_time_pid(specified_pid) :
    return float(gettimepid(specified_pid))



def get_current_virtual_time() :
    try :
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(script_dir + "/dilate_pids.txt","r") as f :
             lines = f.readlines()
        lines = [x.strip() for x in lines]
        first_dilated_pid = int(lines[0])
        curr_time = get_current_virtual_time_pid(first_dilated_pid)
        return curr_time
    except:
        return time.time()

    
		

