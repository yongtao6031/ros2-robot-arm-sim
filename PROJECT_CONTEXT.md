# PROJECT_CONTEXT.md

## Project Snapshot

Project name:

- Chinese: 基于 ROS2 的仿真机械臂控制系统
- English: ROS2 Simulated Robotic Arm Control System

This repository is a ROS2 Jazzy workspace for a simulated robotic arm control-flow visualization project. It is designed to verify a minimal no-hardware control chain:

```text
keyboard target input -> simulated executor -> joint state conversion -> URDF robot model + scene markers -> RViz2 visualization
```

The current project is intentionally lightweight. It focuses on ROS2 fundamentals and a clean, inspectable architecture before introducing heavier robotics frameworks.

## Current Mainline

The repository currently contains three ROS2 packages:

| Package | Build Type | Responsibility |
| --- | --- | --- |
| `armpy_interfaces` | `ament_cmake` | Defines custom `ArmPose.msg` and `ArmPoseRange.srv` interfaces |
| `armpy_description` | `ament_cmake` | Provides URDF/xacro robot model with a simple gripper, RViz2 config, and model display launch |
| `armpy_sim` | `ament_python` | Provides keyboard input, simulated arm executor, pose-to-joint-state conversion, scene markers, and system launch |

The current runtime graph is:

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
  -> /armpy_scene
     -> /rviz2
```

## Important Entry Points

Human-facing documentation:

- `README.md`
- `src/armpy_interfaces/README.md`
- `src/armpy_description/README.md`
- `src/armpy_sim/README.md`

Core interfaces:

- `src/armpy_interfaces/msg/ArmPose.msg`
- `src/armpy_interfaces/srv/ArmPoseRange.srv`

Robot model and visualization:

- `src/armpy_description/urdf/simple_arm.urdf.xacro`
- `src/armpy_description/rviz/armpy_sim.rviz`
- `src/armpy_description/launch/display.launch.py`

Simulation/control-flow nodes:

- `src/armpy_sim/armpy_sim/keyboard_node.py`
- `src/armpy_sim/armpy_sim/mock_arm_node.py`
- `src/armpy_sim/armpy_sim/pose_to_joint_states_node.py`
- `src/armpy_sim/armpy_sim/scene_marker_node.py`
- `src/armpy_sim/launch/keyboard_rviz.launch.py`

## Current Stage Goal

Current goal:

1. Keep the project open-source safe and understandable.
2. Make the ROS2 package structure clear enough for humans and AI agents to maintain.
3. Stabilize the no-hardware RViz2 visualization chain.
4. Use this project as a foundation for later robotic arm simulation experiments.

The project should remain focused on a clear mechanical-arm learning and demonstration path. More complex robotics experiments can be added gradually after the current architecture is understood.

## Current Boundaries

Already implemented:

- ROS2 Jazzy workspace.
- Custom msg/srv definitions.
- rclpy topic/service nodes.
- URDF/xacro robotic arm model.
- `/joint_states` publishing.
- `robot_state_publisher` and TF visualization chain.
- Simple gripper links and finger joints in URDF.
- RViz2 scene markers for a ball and an open box.
- RViz2 visualization workflow.

Not implemented yet:

- Gazebo physical simulation.
- MoveIt2 motion planning.
- ros2_control controller integration.
- Camera, vision, or point cloud processing.
- Real hardware drivers.

Do not describe these unimplemented items as completed in README, package docs, or public project summaries.

## Near-Term Decisions

Keep the current three-package structure:

- `armpy_interfaces`: communication contract.
- `armpy_description`: robot description and visualization config.
- `armpy_sim`: no-hardware simulation/control-flow nodes.

Recommended next technical steps:

1. Read and understand the current implementation in this order: interfaces, URDF/xacro, nodes, launch.
2. Read the new gripper links/joints in `simple_arm.urdf.xacro` and understand how prismatic finger joints are represented.
3. Read `scene_marker_node.py` and understand how RViz2 MarkerArray represents the ball and open box.
4. Only introduce MoveIt2 after the current joint-state, TF, gripper, and scene marker chain is well understood.
5. Only introduce Gazebo/ros2_control when physical interaction, controllers, or more realistic simulation are actually needed.

## Code Management Notes

Do not commit generated ROS2 build outputs:

```text
build/
install/
log/
```

Public docs should stay generic and technical. Private notes, personal planning context, local machine paths, credentials, and chat-specific history should stay outside this repository or in explicitly local-only files.
