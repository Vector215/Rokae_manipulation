# Rokae_manipulation
A repo for roake_xmatepro7 robot manipulation based on [rokae_imitation](https://github.com/destroy314/rokae_imitation) and moveit!

基于络石机械臂的实时控制规划与手眼标定

## Usage 使用
详情请参考文档 [USAGE.md](USAGE.md)


## Installation 环境配置与安装

+ 首先安装对应版本的ros组件
```
rm -rf build/*
catkin_make clean
catkin_make
```
+ 安装 `rokae_imitation` 并编译
```
git clone https://github.com/destroy314/rokae_imitation.git
cd build
cmake ..
make
```
