from Robotic.Rokae import RokaexMatePro7
import random
import time
from Env.BaseEnv import BaseEnv
import numpy as np
from utils.robot_utils import tcp_pose_trans
from Robotic.RosNode import RosMoveitPlanner
from copy import deepcopy

robot = RokaexMatePro7()
planner = RosMoveitPlanner()
env = BaseEnv(robot=robot, motion_planner=planner)
env.reset()

arrays = []
with open('/home/icrlab/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts/joint_position.txt', 'r') as f:
    for line in f:
        # 去掉行首尾空格和换行符，然后将字符串转换为 NumPy 数组
        array = np.fromstring(line.strip()[1:-1], sep=' ')
        arrays.append(array)

print(arrays)

for joint in arrays:
    env.movej(joint)
    time.sleep(5)
qpose = env.robot.pose_home

# pose_list = []
# pose1 = np.array([0.34428389 ,-0.35731281  ,0.35907232 , 3.13275609,  0.48070026,  0.48917881])
# pose2 = np.array([0.34428389 ,-0.1 ,0.35907232 , 3.13275609,  0.48070026,  0.48917881])
# pose_list.append(pose2)

# tmp = deepcopy(pose1)
# joints = []
# for i in range(5):
#     tmp[:3] += np.array([0.03, 0.03, 0.03])
#     pose_list.append(deepcopy(tmp))

# tmp = deepcopy(pose1)
# for i in range(5):
#     tmp[:3] += np.array([0.03, 0.02, 0.01])
#     pose_list.append(deepcopy(tmp))

# tmp = deepcopy(pose1)
# for i in range(5):
#     tmp[:3] += np.array([0.03, -0.02, -0.01])
#     pose_list.append(deepcopy(tmp))

# for pose in pose_list:
#     pose = tcp_pose_trans(pose)
#     env.movep(pose)
#     time.sleep(3)
#     joints.append(deepcopy(env.robot.joints))
#     time.sleep(3)

# with open('joint_position.txt', 'w') as f:
#     for item in joints:
#         f.write(f"{item}\n")
# qpose1 = np.array([-13.192, 22.813, -13.699, 68.206, -17.833, 104.968, 122.943])
# qpose1 = qpose1/180 * 3.14159

# env.movej(qpose1)
# print(env.robot.joints)
# print(env.robot.tcp_pose)




