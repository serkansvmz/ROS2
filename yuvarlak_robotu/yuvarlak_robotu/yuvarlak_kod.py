import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class YuvarlakNode(Node):
    def __init__(self):
        super().__init__('yuvarlak_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Daire çizmeye başlıyorum')

        self.start_time = self.get_clock().now()
        self.duration = 15.0  # saniye

        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        if elapsed < self.duration:
            msg = Twist()
            msg.linear.x = 0.4
            msg.angular.z = 0.6
            self.publisher_.publish(msg)
        else:
            self.publisher_.publish(Twist())
            self.get_logger().info('Bitti')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = YuvarlakNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

