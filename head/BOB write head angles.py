#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*******************************************************************************
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************


#*******************************************************************************
#***********************     Read and Write Example      ***********************
#  Required Environment to run this example :
#    - Protocol 2.0 supported DYNAMIXEL(X, P, PRO/PRO(A), MX 2.0 series)
#    - DYNAMIXEL Starter Set (U2D2, U2D2 PHB, 12V SMPS)
#  How to use the example :
#    - Select the DYNAMIXEL in use at the MY_DXL in the example code. 
#    - Build and Run from proper architecture subdirectory.
#    - For ARM based SBCs such as Raspberry Pi, use linux_sbc subdirectory to build and run.
#    - https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/
#  Author: Ryu Woon Jung (Leon)
#  Maintainer : Zerom, Will Son
# *******************************************************************************

import os

dxl_goal_position1 = 10
dxl_goal_position2 = 10
dxl_goal_position3 = 10 #Let these be input angles for yaw, pitch, and roll

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

#********* DYNAMIXEL Model definition *********
#***** (Use only one definition at a time) *****
MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended)


# Control table address
ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 57600
    
# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID_1                     = 1
DXL_ID_2                     = 2
DXL_ID_3                     = 3

# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/ttyUSB0'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

index = 0
#dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE//2, DXL_MAXIMUM_POSITION_VALUE//2]         # Goal position


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque
dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result_2, dxl_error_2 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_2, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result_3, dxl_error_3 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_3, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result_1 != COMM_SUCCESS or dxl_comm_result_2 != COMM_SUCCESS or dxl_comm_result_3 != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_1))
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_2))
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_3))
elif dxl_error_1 != 0 or dxl_error_2 != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error_1))
    print("%s" % packetHandler.getRxPacketError(dxl_error_2))
    print("%s" % packetHandler.getRxPacketError(dxl_error_3))
else:
    print("Dynamixel has been successfully connected")

while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    # Write goal position
    if (MY_DXL == 'XL320'): # XL320 uses 2 byte Position Data, Check the size of data in your DYNAMIXEL's control table
        dxl_comm_result_1, dxl_error_1 = packetHandler.write2ByteTxRx(portHandler, DXL_ID_1, ADDR_GOAL_POSITION, dxl_goal_position1)
        dxl_comm_result_2, dxl_error_2 = packetHandler.write2ByteTxRx(portHandler, DXL_ID_2, ADDR_GOAL_POSITION, dxl_goal_position2)
        dxl_comm_result_3, dxl_error_3 = packetHandler.write2ByteTxRx(portHandler, DXL_ID_3, ADDR_GOAL_POSITION, dxl_goal_position3)
    else:
        dxl_comm_result_1, dxl_error_1 = packetHandler.write4ByteTxRx(portHandler, DXL_ID_1, ADDR_GOAL_POSITION, dxl_goal_position1)
        dxl_comm_result_2, dxl_error_2 = packetHandler.write4ByteTxRx(portHandler, DXL_ID_2, ADDR_GOAL_POSITION, dxl_goal_position2)
        dxl_comm_result_3, dxl_error_3 = packetHandler.write4ByteTxRx(portHandler, DXL_ID_3, ADDR_GOAL_POSITION, dxl_goal_position3)
    
    if dxl_comm_result_1 != COMM_SUCCESS or dxl_comm_result_2 != COMM_SUCCESS or dxl_comm_result_3 != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_1))
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_2))
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result_3))
    elif dxl_error_1 != 0 or dxl_error_2 != 0 or dxl_error_3 != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error_1))
        print("%s" % packetHandler.getRxPacketError(dxl_error_2))
        print("%s" % packetHandler.getRxPacketError(dxl_error_3))

    while 1:
        # Read present position
        if (MY_DXL == 'XL320'): # XL320 uses 2 byte Position Data, Check the size of data in your DYNAMIXEL's control table
            dxl_present_position_1, dxl_comm_result_1, dxl_error_1 = packetHandler.read2ByteTxRx(portHandler, DXL_ID_1, ADDR_PRESENT_POSITION)
            dxl_present_position_2, dxl_comm_result_2, dxl_error_2 = packetHandler.read2ByteTxRx(portHandler, DXL_ID_2, ADDR_PRESENT_POSITION)
            dxl_present_position_3, dxl_comm_result_3, dxl_error_3 = packetHandler.read2ByteTxRx(portHandler, DXL_ID_3, ADDR_PRESENT_POSITION)
        else:
            dxl_present_position_1, dxl_comm_result_1, dxl_error_1 = packetHandler.read4ByteTxRx(portHandler, DXL_ID_1, ADDR_PRESENT_POSITION)
            dxl_present_position_2, dxl_comm_result_2, dxl_error_2 = packetHandler.read4ByteTxRx(portHandler, DXL_ID_2, ADDR_PRESENT_POSITION)
            dxl_present_position_3, dxl_comm_result_3, dxl_error_3 = packetHandler.read4ByteTxRx(portHandler, DXL_ID_3, ADDR_PRESENT_POSITION)
        
        if dxl_comm_result_1 != COMM_SUCCESS or dxl_comm_result_2 != COMM_SUCCESS or dxl_comm_result_3 != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result_1))
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result_2))
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result_3))
        elif dxl_error_1 != 0 or dxl_error_2 != 0 or dxl_error_3 != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error_1))
            print("%s" % packetHandler.getRxPacketError(dxl_error_2))
            print("%s" % packetHandler.getRxPacketError(dxl_error_3))
        
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_1, dxl_goal_position1, dxl_present_position_1))
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_2, dxl_goal_position2, dxl_present_position_2))
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID_3, dxl_goal_position3, dxl_present_position_3))

        if not abs(dxl_goal_position1 - dxl_present_position_1) > DXL_MOVING_STATUS_THRESHOLD:
            break
        if not abs(dxl_goal_position2 - dxl_present_position_2) > DXL_MOVING_STATUS_THRESHOLD:
            break
        if not abs(dxl_goal_position3 - dxl_present_position_3) > DXL_MOVING_STATUS_THRESHOLD:
            break


# Disable Dynamixel Torque
dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result_2, dxl_error_2 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_2, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result_3, dxl_error_3 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_3, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result_1 != COMM_SUCCESS or dxl_comm_result_2 != COMM_SUCCESS or dxl_comm_result_3 != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_1))
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_2))
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result_3))
elif dxl_error_1 != 0 or dxl_error_2 != 0 or dxl_error_3 != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error_1))
    print("%s" % packetHandler.getRxPacketError(dxl_error_2))
    print("%s" % packetHandler.getRxPacketError(dxl_error_3))

# Close port
portHandler.closePort()
