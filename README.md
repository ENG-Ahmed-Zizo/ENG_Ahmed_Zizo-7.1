# 🐢 turtle_controller

A ROS2 package that drives a turtlesim turtle with the keyboard and reads
color sensor data from its environment.

**MIA Robotics — Electrical Training 2026/27 — Task 7**

---

## What it does

- Moves the turtle using keyboard input (W/A/S/D or arrow keys)
- Reads the turtle's color sensor and figures out the dominant background color
- Logs the color and publishes it to its own topic
- Everything is launched together with one command

---

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select turtle_controller
source install/setup.bash
```

## Run

```bash
ros2 launch turtle_controller turtle_launch.py
```

This starts `turtlesim` and the controller node together.

---

## Controls

Click into the terminal running the node, then use:

| Key | Move |
|---|---|
| W / ↑ | Forward |
| S / ↓ | Backward |
| A / ← | Turn left |
| D / → | Turn right |

---

## Parameters

Topic names aren't hardcoded — they can be changed at launch time:

| Parameter | Default |
|---|---|
| `cmd_vel_topic` | `/turtle1/cmd_vel` |
| `color_sensor_topic` | `/turtle1/color_sensor` |
| `dominant_color_topic` | `/dominant_color` |
| `use_stamped_vel` | `false` |

Example:
```bash
ros2 launch turtle_controller turtle_launch.py use_stamped_vel:=true
```

---

## Why only forward/back and turning?

A turtlesim turtle can't slide sideways — it can only move along the
direction it's facing and rotate, just like a real differential-drive robot.
That's why the code only ever sets `linear.x` and `angular.z` on the
velocity message.

---

## Author

Ahmed Zizo
