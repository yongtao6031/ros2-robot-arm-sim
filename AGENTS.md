# AGENTS.md

This file provides project-specific guidance for AI coding agents such as Codex, Claude, Cursor, and similar tools.

## First Files To Read

When entering this repository, read these files first:

1. `README.md` - project overview, quick start, package map, and runtime workflow.
2. `PROJECT_CONTEXT.md` - current stage, active goals, boundaries, and near-term decisions.
3. Package README files:
   - `src/armpy_interfaces/README.md`
   - `src/armpy_description/README.md`
   - `src/armpy_sim/README.md`

Then inspect the package manifests and launch entry points:

- `src/armpy_interfaces/package.xml`
- `src/armpy_description/package.xml`
- `src/armpy_sim/package.xml`
- `src/armpy_sim/launch/keyboard_rviz.launch.py`
- `src/armpy_description/launch/display.launch.py`

## Project Boundary

This repository is a ROS2 Jazzy robotic arm visualization and control-flow simulation project.

Current scope:

- Custom ROS2 msg/srv interfaces.
- rclpy topic/service nodes.
- URDF/xacro robot description.
- `/joint_states` and `robot_state_publisher` visualization chain.
- RViz2-based model and TF visualization.

Out of current scope unless explicitly requested:

- Gazebo physical simulation.
- MoveIt2 motion planning.
- ros2_control controller integration.
- Vision, camera, or point cloud processing.
- Real hardware drivers.

## Directory Responsibilities

- `src/armpy_interfaces/`: ROS2 interface definitions only. Keep msg/srv definitions stable and update dependent code when changing them.
- `src/armpy_description/`: robot model, RViz2 config, and display launch files. Do not add control logic here.
- `src/armpy_sim/`: simulation/control-flow nodes and launch files. Keep node responsibilities small and explicit.
- `doc/`: screenshots and lightweight documentation images for README usage.

## Modification Principles

- Prefer existing package boundaries over adding new packages.
- Keep public documentation generic and open-source safe.
- Do not add personal history, private paths, job-search context, or chat-only decisions to public docs.
- Keep generated build outputs out of Git: `build/`, `install/`, and `log/`.
- Avoid broad refactors unless they directly support the requested change.
- If adding a new runtime feature, update the relevant package README and root README when the workflow changes.

## Validation

Recommended validation on Ubuntu 24.04 with ROS2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Useful checks:

```bash
ros2 pkg list | grep armpy
ros2 interface show armpy_interfaces/msg/ArmPose
ros2 interface show armpy_interfaces/srv/ArmPoseRange
ros2 launch armpy_sim keyboard_rviz.launch.py
ros2 run armpy_sim keyboard_node
```

If RViz2 or GUI tools are unavailable, at least validate build, package discovery, interface generation, node launch, and topic/service visibility.

## Privacy And Safety

- Do not commit local machine paths, credentials, tokens, SSH keys, private notes, or personal planning context.
- Do not claim support for physical simulation, motion planning, controllers, perception, or hardware unless the implementation exists in this repository.
- Treat `PROJECT_CONTEXT.md` as a technical state snapshot, not a personal diary.
