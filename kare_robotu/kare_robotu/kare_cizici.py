import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_srvs.srv import Empty
import math

class KareRobot(Node):
    def __init__(self):
        super().__init__('kare_robot_node')

        # Publisher & Subscriber
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Gazebo reset
        self.reset_client = self.create_client(Empty, '/reset_world')
        while not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Reset servisi bekleniyor...')
        self.reset_client.call_async(Empty.Request())
        self.get_logger().info('Gazebo resetlendi')

        # Parametreler
        self.speed = 0.2
        self.turn_speed = 0.5
        self.edge_length = 1.0
        self.angle_tol = 0.05  # ~3 derece

        # Robot durumu
        self.state = "forward"
        self.edge_count = 0

        self.start_x = None
        self.start_y = None
        self.start_yaw = None
        self.target_yaw = None

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

        self.odom_ready = False

        # Kontrol döngüsü (10 Hz)
        self.timer = self.create_timer(0.1, self.control_loop)

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y*q.y + q.z*q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

        self.odom_ready = True

    def control_loop(self):
        if not self.odom_ready:
            return

        if self.edge_count >= 4:
            self.cmd_pub.publish(Twist())
            self.get_logger().info("Kare tamamlandı! 👏")
            self.timer.cancel()
            return

        msg = Twist()

        # ---- İLERİ GİT ----
        if self.state == "forward":
            if self.start_x is None:
                self.start_x = self.current_x
                self.start_y = self.current_y
                self.get_logger().info(f"Kenar {self.edge_count+1} çiziliyor")

            dist = math.sqrt(
                (self.current_x - self.start_x)**2 +
                (self.current_y - self.start_y)**2
            )

            if dist < self.edge_length:
                msg.linear.x = self.speed
            else:
                self.state = "turn"
                self.start_yaw = self.current_yaw
                self.target_yaw = self.normalize_angle(
                    self.start_yaw + math.pi / 2
                )
                self.start_x = None
                self.start_y = None

        # ---- DÖN ----
        elif self.state == "turn":
            yaw_error = self.normalize_angle(
                self.target_yaw - self.current_yaw
            )

            if abs(yaw_error) > self.angle_tol:
                msg.angular.z = self.turn_speed
            else:
                self.state = "forward"
                self.edge_count += 1
                self.start_yaw = None
                self.target_yaw = None
                self.get_logger().info(
                    f"Köşe tamamlandı ({self.edge_count}/4)"
                )

        self.cmd_pub.publish(msg)

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle


def main(args=None):
    rclpy.init(args=args)
    node = KareRobot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

