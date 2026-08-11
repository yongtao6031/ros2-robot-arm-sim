# armpy_sim

`armpy_sim` 实现无硬件机械臂控制仿真闭环。

这个包回答的问题是：**没有真实机械臂时，如何让 ROS2 控制链路跑起来并在 RViz2 中看到运动。**

## Nodes

### keyboard_node

发布目标坐标：

```text
/keyboard_node -> /arm/pose
```

运行：

```bash
ros2 run armpy_sim keyboard_node
```

键盘控制：

| Key | Effect |
| --- | --- |
| `W/S` | increase/decrease x |
| `Q/E` | increase/decrease y |
| `A/D` | increase/decrease z |
| `C` | quit |

### mock_arm_node

模拟真实机械臂执行节点：

```text
/arm/pose -> /mock_arm_node
/mock_arm_node -> /arm/pose/range
```

它不会打开串口，也不会控制真实硬件，只打印收到的目标坐标，并提供范围检查服务。

### pose_to_joint_states_node

将目标坐标近似转换为关节角：

```text
/arm/pose -> /pose_to_joint_states_node -> /joint_states
```

`robot_state_publisher` 读取 `/joint_states` 后发布 TF，RViz2 根据 TF 显示机械臂姿态。

## Launch

推荐用两个终端运行。

终端 1：

```bash
ros2 launch armpy_sim keyboard_rviz.launch.py
```

终端 2：

```bash
ros2 run armpy_sim keyboard_node
```

一键启动键盘节点、仿真节点和 RViz2：

```bash
ros2 launch armpy_sim keyboard_rviz.launch.py start_keyboard:=true
```

交互式键盘节点更推荐单独终端运行。

## Graph

完整通信关系：

```text
/keyboard_node
  -> /arm/pose
     -> /mock_arm_node
     -> /pose_to_joint_states_node
          -> /joint_states
             -> /robot_state_publisher
                  -> /tf
                     -> /rviz2
```

## Checks

```bash
ros2 node list
ros2 topic info /arm/pose --verbose
ros2 topic info /joint_states --verbose
ros2 service call /arm/pose/range armpy_interfaces/srv/ArmPoseRange "{x: 220, y: 80, z: 180}"
```

## Boundary

这个包当前不包含：

- 真实串口控制节点。
- 摄像头和点云输入。
- Gazebo 物理仿真。
- MoveIt2 运动规划。

