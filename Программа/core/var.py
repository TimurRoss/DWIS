"""File with global variables for whole programm"""
from dataclasses import dataclass
import multiprocessing as multproc

manager = multproc.Manager()
Vars = manager.dict()

# IMU App variables
Vars['imuapp_is_enabled'] = False

# Variables of settings for drone
Vars['dronesett_depth'] = 0