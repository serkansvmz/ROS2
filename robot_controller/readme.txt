2. Derle ve Çalıştır (Tek Komut)
Şimdi her şeyi kapat ve tek bir terminalde şunları yap:

Bash
cd ~/robot_ws
colcon build --packages-select robot_controller
source install/setup.bash
ros2 launch robot_controller gazebo.launch.py





Terminal 1 (Görselleştirme): Gazebo'yu ve robotu yükler.

source ~/robot_ws/install/setup.bash
ros2 launch robot_controller gazebo.launch.py



Terminal 2 (Haberleşme): ROS 2 dünyasıyla Gazebo Sim dünyası arasındaki köprüyü kurar.

ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist



Terminal 3 (Zeka/Hareket): Senin yazdığın algoritmayı (düz git, dur vs.) çalıştırır.

source ~/robot_ws/install/setup.bash
ros2 run robot_controller move_robot


1. Standart Derleme Komutu

cd ~/robot_ws
colcon build


Sadece Kendi Paketini Derlemek (Tavsiye Edilen)

colcon build --packages-select robot_controller


3. "Tertemiz" Derleme (Hata Aldığında)

cd ~/robot_ws
rm -rf build/ install/ log/
colcon build --packages-select robot_controller


4. Derlemeden Sonraki "Altın Adım"
colcon build bittikten sonra terminale "Ben bu paketleri derledim, artık onları tanıyabilirsin" demen gerekir. Bunu yapmazsan ros2 run dediğinde hata alırsın:

Bash
source install/setup.bash
