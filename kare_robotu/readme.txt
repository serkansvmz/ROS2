dosya oluşturma
touch ~/robot_ws/src/mesafe_robotu/dosya_adi.txt

rm -rf build/ install/ log/

cd ~/robot_ws
colcon build --packages-select kare_robotu
source install/setup.bash
ros2 launch kare_robotu gazebo.launch.py


