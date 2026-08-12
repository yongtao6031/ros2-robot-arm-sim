# armpy_description

`armpy_description` 定义机械臂模型和 RViz2 显示配置。

这个包回答的问题是：机器人模型由哪些 link 和 joint 组成，RViz2 如何显示它。

## Contents

```text
urdf/simple_arm.urdf.xacro
rviz/armpy_sim.rviz
launch/display.launch.py
```

## Responsibilities

- 使用 URDF/xacro 定义简化机械臂模型。
- 定义 `base_link`、`upper_arm`、`forearm`、`wrist_link`、`gripper_palm`、`left_finger`、`right_finger` 等 link。
- 定义 `base_yaw_joint`、`shoulder_joint`、`elbow_joint`、`wrist_joint`、`left_finger_joint`、`right_finger_joint` 等 joint。
- 提供 RViz2 配置，默认显示 Grid、RobotModel、TF 和 Scene MarkerArray。
- 提供单独查看模型的 launch 文件。

## Display Only

只显示模型：

```bash
cd ~/armpy-ros2-ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch armpy_description display.launch.py
```

单独运行 `display.launch.py` 时，如果没有节点发布 `/joint_states`，机械臂会保持默认状态或提示缺少关节状态。这是正常现象。

完整控制可视化链路请运行：

```bash
ros2 launch armpy_sim keyboard_rviz.launch.py
```

## Boundary

这个包不负责：

- 键盘控制。
- 仿真执行节点。
- 目标坐标到关节状态转换。
- 场景 Marker 发布。
- Gazebo 物理仿真。
- MoveIt2 运动规划。
