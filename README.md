# 基于ROS2的采摘机械臂控制系统

ROS2 Jazzy 采摘机械臂控制仿真工作空间。

聚焦在机械臂控制仿真的最小闭环：自定义接口、目标坐标输入、mock 执行节点、关节状态发布、URDF 机器人模型和 RViz2 可视化。

## Packages

| Package | Role |
| --- | --- |
| `armpy_interfaces` | 自定义 `ArmPose.msg` 和 `ArmPoseRange.srv` |
| `armpy_description` | 机械臂 URDF/xacro、RViz2 配置和单独显示 launch |
| `armpy_sim` | 键盘控制、mock 执行、目标坐标到 `/joint_states` 的转换和一键仿真 launch |

## Workflow

当前仿真链路：

```text
keyboard_node
  -> /arm/pose
mock_arm_node
  -> 模拟真实机械臂执行节点

pose_to_joint_states_node
  -> /joint_states
robot_state_publisher
  -> TF
RViz2
  -> 显示机械臂姿态
```

## Quick Start

环境建议：

- Ubuntu 24.04
- ROS2 Jazzy

编译：

```bash
cd ~/armpy-ros2-ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

推荐用两个终端启动。终端 1 启动仿真和 RViz2：

```bash
ros2 launch armpy_sim keyboard_rviz.launch.py
```

终端 2 启动键盘控制：

```bash
ros2 run armpy_sim keyboard_node
```

如果你明确想让 launch 同时启动键盘节点，也可以运行：

```bash
ros2 launch armpy_sim keyboard_rviz.launch.py start_keyboard:=true
```

但交互式键盘节点更推荐单独终端运行。

键盘控制：

- `W/S`: increase/decrease x
- `Q/E`: increase/decrease y
- `A/D`: increase/decrease z
- `C`: quit

## Useful Checks

```bash
ros2 topic list
ros2 topic echo /arm/pose
ros2 topic echo /joint_states
ros2 service call /arm/pose/range armpy_interfaces/srv/ArmPoseRange "{x: 220, y: 80, z: 180}"
```

## Scope

已完成或当前目标：

- ROS2 package structure
- custom msg/srv
- rclpy nodes
- URDF/xacro model
- RViz2 visualization
- no-hardware simulation loop

暂不包含：

- Orbbec camera
- PointCloud2/Open3D perception
- Gazebo physics simulation
- MoveIt2 planning
- real serial hardware control
