# Menjalankan `member1` Secara Manual

ROS 2 dan `turtlesim` harus sudah terpasang. **Ketik perintah langsung di dua terminal; tidak ada skrip `.sh` atau `.cmd`.** Ganti lokasi ROS dan repo di bawah jika berbeda. Saat ini program hanya menggambar angka **1**, lalu menunggu `member2`.

## Linux

Terminal 1 (turtlesim):

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 (member1):

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws/src
PYTHONPATH="$PWD/digit_relay:$PYTHONPATH" python3 -m digit_relay.member1
```

## macOS

Terminal 1 (turtlesim):

```bash
source ~/ros2_jazzy/install/setup.bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 (member1):

```bash
source ~/ros2_jazzy/install/setup.bash
cd ~/ros2_ws/src
PYTHONPATH="$PWD/digit_relay:$PYTHONPATH" python3 -m digit_relay.member1
```

## Windows (Command Prompt)

Terminal 1 (turtlesim):

```bat
call C:\dev\ros2_jazzy\local_setup.bat
ros2 run turtlesim turtlesim_node
```

Terminal 2 (member1):

```bat
call C:\dev\ros2_jazzy\local_setup.bat
cd /d C:\ros2_ws\src
set "PYTHONPATH=%CD%\digit_relay;%PYTHONPATH%"
python -m digit_relay.member1
```
