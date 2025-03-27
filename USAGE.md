## 使用流程 Demo 

+ 复位机械臂，并启动实时控制接口
``` bash
cd ~/rokae_imitation/build
sudo ./all_control joint_pose
```
> 第一次复位之后，程序可能会自动退出，属于正常情况。此时需要重新执行`all_control`程序

+ 启动Moveit!与Rviz节点
``` bash
source ~/.bashrc
roslaunch xmatepro7_calib_moveit_config demo.launch
```

+ 启动`ros_pub`脚本向Moveit!和Rviz发送关节角度
``` bash
source ~/.bashrc
mamba activate ros
cd ~/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts
python3 ros_pub.py
```

+ 执行`demo`脚本
``` bash
source ~/.bashrc
mamba activate ros
cd ~/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts
python3 demo.py
```

## 手眼标定 For Hand-eye calibration

+ 复位机械臂，并启动实时控制接口
``` bash
cd ~/rokae_imitation/build
sudo ./all_control joint_pose
```
> 第一次复位之后，程序可能会自动退出，属于正常情况。此时需要重新执行`all_control`程序

+  启动Moveit!与Rviz节点
``` bash
source ~/.bashrc
roslaunch xmatepro7_calib_moveit_config demo.launch
```

+ 启动`ros_pub`脚本向Moveit!和Rviz发送关节角度
``` bash
source ~/.bashrc
mamba activate ros
cd ~/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts
python3 ros_pub.py
```

+ （第一次启动时）重置相机接口
``` bash
source ~/.bashrc
mamba activate ros
cd ~/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts
sudo bash install_udev_rules.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
```

+ 根据预设位姿移动机械臂，获取标定所需数据
``` bash
source ~/.bashrc
mamba activate ros
cd ~/rokae_ws/src/rokae_xmatepro7/xmatepro7_moveit_config/scripts
python3 calibration.py
```

