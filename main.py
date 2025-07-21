#from dashboard_control import open_gripper, close_gripper
from robot_control import *
from config import *

ROBOT_IP = "192.168.0.2"  # Reemplaza con la IP real del UR5
ROBOT_PORT = 30002  

if __name__ == '__main__':
    move_to_position(home_position)
    #move_to_position(intermedioPickupHome)    
    #move_to_position(pickup1)    
