import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MesafeKontrol(Node):
    def __init__(self):
        super().__init__('mesafe_kontrol_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        self.hiz = 0.2
        self.hedef_mesafe = 2.0
        self.sure = self.hedef_mesafe / self.hiz

        self.baslangic_zamani = self.get_clock().now()

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info(f'Robot {self.hedef_mesafe} metre gitmeye başladı')

    def timer_callback(self):
        gecen_sure = (self.get_clock().now() - self.baslangic_zamani).nanoseconds / 1e9

        if gecen_sure < self.sure:
            msg = Twist()
            msg.linear.x = self.hiz
            self.publisher_.publish(msg)

            kalan = self.hedef_mesafe - (gecen_sure * self.hiz)
            self.get_logger().info(
                f'Kalan mesafe: {kalan:.2f} m',
                throttle_duration_sec=0.5
            )
        else:
            self.publisher_.publish(Twist())
            self.get_logger().info('Hedefe varıldı, robot durdu 🛑')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = MesafeKontrol()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

