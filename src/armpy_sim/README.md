# armpy_sim

`armpy_sim` 实现机械臂控制流程的无硬件可视化闭环。

这个包回答的问题是：如何让 ROS2 控制链路跑起来，并在 RViz2 中看到机械臂姿态变化。

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

提供仿真执行节点和范围检查服务：

```text
/arm/pose -> /mock_arm_node
/mock_arm_node -> /arm/pose/range
```

该节点订阅目标坐标，打印收到的控制目标，并通过服务返回目标是否在允许范围内。

### pose_to_joint_states_node

将目标坐标近似转换为关节状态：

```text
/arm/pose -> /pose_to_joint_states_node -> /joint_states
```

`robot_state_publisher` 读取 `/joint_states` 后发布 TF，RViz2 根据 TF 显示机械臂姿态。

### scene_marker_node

发布简单任务场景：

```text
/scene_marker_node -> /visualization_marker_array
```

该节点使用 `visualization_msgs/MarkerArray` 发布一个球和一个开口盒子，用于在 RViz2 中表达后续夹取与放置实验的目标环境。

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

也可以一键启动键盘节点、仿真节点和 RViz2：

```bash
ros2 launch armpy_sim keyboard_rviz.launch.py start_keyboard:=true
```

交互式键盘节点更推荐单独终端运行，便于稳定接收键盘输入。

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
/scene_marker_node
  -> /visualization_marker_array
     -> /rviz2
```

## Checks

```bash
ros2 node list
ros2 topic info /arm/pose --verbose
ros2 topic info /joint_states --verbose
ros2 topic info /visualization_marker_array --verbose
ros2 service call /arm/pose/range armpy_interfaces/srv/ArmPoseRange "{x: 220, y: 80, z: 180}"
```

## Boundary

这个包当前不包含：

- 物理级仿真。
- 运动规划。
- 控制器链路。
- 视觉感知或点云处理。
- 实体硬件驱动。
