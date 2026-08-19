import sys
import termios
import tty
import select

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped
from turtlesim.msg import Color
from std_msgs.msg import String


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        # ---- Parameters (Requirement 4) ----
        self.declare_parameter('cmd_vel_topic', '/turtle1/cmd_vel')
        self.declare_parameter('color_sensor_topic', '/turtle1/color_sensor')
        self.declare_parameter('dominant_color_topic', '/dominant_color')
        self.declare_parameter('use_stamped_vel', False)   # Bonus 2
        self.declare_parameter('linear_speed', 2.0)
        self.declare_parameter('angular_speed', 2.0)

        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        color_sensor_topic = self.get_parameter('color_sensor_topic').value
        dominant_color_topic = self.get_parameter('dominant_color_topic').value
        self.use_stamped_vel = self.get_parameter('use_stamped_vel').value
        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value

        # ---- Publisher: movement (Requirement 2) ----
        if self.use_stamped_vel:
            self.cmd_vel_pub = self.create_publisher(TwistStamped, cmd_vel_topic, 10)
        else:
            self.cmd_vel_pub = self.create_publisher(Twist, cmd_vel_topic, 10)

        # ---- Publisher: dominant color (Requirement 3, Action 2) ----
        self.dominant_color_pub = self.create_publisher(String, dominant_color_topic, 10)

        # ---- Subscriber: color sensor (Requirement 3) ----
        self.color_sub = self.create_subscription(
            Color, color_sensor_topic, self.color_callback, 10)

        # ---- Keyboard setup ----
        self.settings = termios.tcgetattr(sys.stdin)
        self.timer = self.create_timer(0.1, self.keyboard_loop)  # 10 Hz poll

        self.get_logger().info(
            'Turtle controller started. Use W/A/S/D or Arrow keys to move. CTRL+C to quit.')

    def get_key(self):
        """Non-blocking single keypress read from the terminal."""
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = ''
        if rlist:
            key = sys.stdin.read(1)
            if key == '\x1b':  # start of an arrow-key escape sequence
                key += sys.stdin.read(2)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def keyboard_loop(self):
        key = self.get_key()
        linear = 0.0
        angular = 0.0

        if key in ('w', '\x1b[A'):
            linear = self.linear_speed
        elif key in ('s', '\x1b[B'):
            linear = -self.linear_speed
        elif key in ('a', '\x1b[D'):
            angular = self.angular_speed
        elif key in ('d', '\x1b[C'):
            angular = -self.angular_speed
        elif key == '\x03':  # Ctrl+C
            rclpy.shutdown()
            return
        else:
            return  # no relevant key pressed this tick

        self.publish_velocity(linear, angular)

    def publish_velocity(self, linear, angular):
        # Non-holonomic: only linear.x and angular.z are ever set
        if self.use_stamped_vel:
            msg = TwistStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'turtle1'
            msg.twist.linear.x = linear
            msg.twist.angular.z = angular
        else:
            msg = Twist()
            msg.linear.x = linear
            msg.angular.z = angular
        self.cmd_vel_pub.publish(msg)

    def color_callback(self, msg: Color):
        r, g, b = msg.r, msg.g, msg.b
        if r >= g and r >= b:
            major = 'Red'
        elif g >= r and g >= b:
            major = 'Green'
        else:
            major = 'Blue'

        # Action 1: log it
        self.get_logger().info(f'Major color: {major} (R={r}, G={g}, B={b})')

        # Action 2: publish it
        out = String()
        out.data = major
        self.dominant_color_pub.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, node.settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()