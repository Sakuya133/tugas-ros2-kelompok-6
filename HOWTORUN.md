# Menjalankan Semua Node

Siapkan ROS 2, `turtlesim`, dan `colcon`. Repo ini harus berada di folder `src` workspace (`ros2_ws/src`). Jalankan perintah berikut **manual di satu terminal**. Ganti path ROS jika lokasi instalasimu berbeda.

## Linux

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build --packages-select digit_relay
source install/setup.bash
ros2 launch digit_relay relay.launch.py
```

## macOS

```bash
source ~/ros2_jazzy/install/setup.bash
cd ~/ros2_ws
colcon build --packages-select digit_relay
source install/setup.bash
ros2 launch digit_relay relay.launch.py
```

## Windows (Command Prompt)

```bat
call C:\dev\ros2_jazzy\local_setup.bat
cd /d C:\ros2_ws
colcon build --merge-install --packages-select digit_relay
call install\setup.bat
ros2 launch digit_relay relay.launch.py
```

Launch menjalankan `turtlesim_node` dan `member1`–`member6`.
