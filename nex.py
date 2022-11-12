from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1
The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:
1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1
	When done, run with:
	$ python run.py solutions/exercise3_solution.py
"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        # added additional check for skipping token already in the list of the grabbed token
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and not(token in silver_list):
            dist=token.dist
            code = token.info.code # added to store also the closest token code
            rot_y=token.rot_y
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, code # added to return also the closest token code

def find_golden_token():
    """
    Function to find the closest golden token
    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        # added additional check for skipping token already in the list of the sorted with a silver token 
        if token.dist < dist and (token.info.marker_type is MARKER_TOKEN_GOLD) and not(token in gold_list):
            dist=token.dist
            code = token.info.code # added to store also the closest token code
            rot_y=token.rot_y
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, code # added to return also the closest token code

# added flag for differentiate the cycle for grabbing a silver token or
# releasing close to a golden token
grab = False
# added two lists for keeping track of the already grabbed silver token and
# of the already sorted golden token with a silver token
gold_list = []
silver_list = []

while 1:
    if silver == True: # if silver is True, than we look for a silver token, otherwise for a golden one
       print("yes")
        dist, rot_y, code = find_silver_token()
        if not code in silver_list: # if the token code is not already in the list
            silver_list.append(code) # update the list with the new silver token to grab
    else:
        dist, rot_y, code = find_golden_token()
        if not code in gold_list: # if the token code is not already in the list
            gold_list.append(code) # update the list with the new golden token to move to
    if dist==-1: # if no token is detected, we make the robot turn 
        print("I don't see any token!!")
        turn(+10, 1)
    elif dist < d_th: # if we are close to the token, we try grab it.
        print("Found it!")
        if not grab: # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
            dist, rot_y, code = find_golden_token()
            gold_list.append(code) # update the list with the new golden token to move to
            d_th = 0.5
            grab = True
            silver = not silver
        else:
            R.release()
            print("yes")
            drive(-20, 1)
            turn(10, 5)
            grab= False
            silver =True
            silver = not silver # we modify the value of the variable silver, so that in the next step we will look for the other type of token
            exit()
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(60, 0.5)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)