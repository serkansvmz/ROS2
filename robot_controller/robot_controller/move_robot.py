import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoveRobot(Node):
    def __init__(self):
        super().__init__('move_robot_node')
        # Hız komutu yayınlayacağımız (publisher) topic'i tanımlıyoruz
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Her 0.5 saniyede bir hareket komutu gönder
        self.timer = self.create_timer(0.5, self.send_velocity)
        self.get_logger().info('Robot hareket kodu başlatıldı!')

    def send_velocity(self):
        msg = Twist()
        msg.linear.x = 0.2  # İleri gitme hızı (m/s)
        msg.angular.z = 0.0 # Dönme hızı (rad/s) - 0 ise düz gider
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoveRobot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
