# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.  
#  You may obtain a copy of the License at
#  
#      http:# www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
import cv2
import os
from pyorbbecsdk import *
from utils.utils import frame_to_bgr_image

from Robotic.Rokae import RokaexMatePro7
import time
from Env.BaseEnv import BaseEnv
import numpy as np
from Robotic.RosNode import RosMoveitPlanner

ESC_KEY = 27
POSE_PATH = '/home/icrlab/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts/joint_position.txt'
SAVE_PATH = '/home/icrlab/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts/calibrate_data'

def save_depth_frame(frame: DepthFrame, index):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    scale = frame.get_depth_scale()
    depth_format = frame.get_format()
    if depth_format != OBFormat.Y16:
        print("depth format is not Y16")
        return
    data = np.frombuffer(frame.get_data(), dtype=np.uint16)
    data = data.reshape((height, width))
    data = data.astype(np.float32) * scale
    data = data.astype(np.uint16)
    save_image_dir = os.path.join(SAVE_PATH, "depth")
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)
    raw_filename = save_image_dir + "/depth_{}x{}_{}_{}.raw".format(width, height, index, timestamp)
    data.tofile(raw_filename)


def save_color_frame(frame: ColorFrame, index):
    if frame is None:
        return
    width = frame.get_width()
    height = frame.get_height()
    timestamp = frame.get_timestamp()
    save_image_dir = os.path.join(SAVE_PATH, "color")
    if not os.path.exists(save_image_dir):
        os.mkdir(save_image_dir)
    filename = save_image_dir + "/color_{}x{}_{}_{}.png".format(width, height, index, timestamp)
    image = frame_to_bgr_image(frame)
    if image is None:
        print("failed to convert frame to image")
        return
    cv2.imwrite(filename, image)


def start_camera():
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    pipeline = Pipeline()
    config = Config()
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile: VideoStreamProfile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
    except OBError as e:
        print(e)
    depth_profile_list = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
    if depth_profile_list is not None:
        depth_profile = depth_profile_list.get_default_video_stream_profile()
        config.enable_stream(depth_profile)
    pipeline.start(config)
    return pipeline

def stop_camera(pipeline):
    pipeline.stop()


def main():
    pipeline = start_camera()
    
    robot = RokaexMatePro7()
    planner = RosMoveitPlanner()
    env = BaseEnv(robot=robot, motion_planner=planner)
    env.reset()

    arrays = []
    with open(POSE_PATH, 'r') as f:
        for line in f:
            # 去掉行首尾空格和换行符，然后将字符串转换为 NumPy 数组
            array = np.fromstring(line.strip()[1:-1], sep=' ')
            arrays.append(array)

    for i, joint in enumerate(arrays):
        env.movej(joint)
        time.sleep(5)
        try:
            frames = pipeline.wait_for_frames(100)
            if frames is None:
                continue
            color_frame = frames.get_color_frame()
            if color_frame is not None:
                save_color_frame(color_frame, i)
            depth_frame = frames.get_depth_frame()
            if depth_frame is not None:
                save_depth_frame(depth_frame, i)
        except KeyboardInterrupt:
            break
        
        time.sleep(5)
        
    stop_camera(pipeline)


if __name__ == "__main__":
    main()
