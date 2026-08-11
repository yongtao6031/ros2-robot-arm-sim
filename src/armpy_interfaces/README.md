# armpy_interfaces

`armpy_interfaces` 定义本项目中跨节点使用的自定义 ROS2 接口。

这个包只负责通信协议，不包含节点逻辑、机器人模型或仿真启动文件。

## Interfaces

```text
msg/ArmPose.msg
srv/ArmPoseRange.srv
```

### ArmPose.msg

```text
int32 x
int32 y
int32 z
int32 vel
```

用于表示机械臂目标坐标和速度参数。当前仿真中由 `keyboard_node` 发布，被 `mock_arm_node` 和 `pose_to_joint_states_node` 订阅。

### ArmPoseRange.srv

```text
int32 x
int32 y
int32 z
---
bool in_range
string message
```

用于检查目标坐标是否在模拟机械臂的允许范围内。当前由 `mock_arm_node` 提供服务，`keyboard_node` 可调用该服务做范围检查。

## Build

```bash
cd ~/armpy-ros2-ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select armpy_interfaces
source install/setup.bash
```

## Checks

```bash
ros2 interface show armpy_interfaces/msg/ArmPose
ros2 interface show armpy_interfaces/srv/ArmPoseRange
```

