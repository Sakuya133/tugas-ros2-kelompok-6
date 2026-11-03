# member3.py
# Node Anggota 3 (biru), slot (x=8.0, y=6.5).
#
# TODO (tugas anggota 3): lengkapi node ini.
# Polanya sama seperti member1.py (tapi tanpa bagian leader & /clear):
#   1. subscribe topic /relay_turn
#   2. kalau active_member == 3, gambar angkanya di slot di atas
#   3. publish [angka+1, 4] untuk mengoper giliran ke anggota 4

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy
from std_msgs.msg import Int32MultiArray
from turtlesim.srv import TeleportAbsolute, SetPen

from digit_relay.digit_font import SEG, DIGITS

MY_ID = 3
NEXT_ID = 4
COLOR = (0, 125, 125)          
SLOT_X, SLOT_Y = 8.0, 6.5    
W, H = 1.2, 2.5 

def main():
    rclpy.init()
    node = Node('member3')

    qos = QoSProfile(depth=10)
    qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
    pub = node.create_publisher(Int32MultiArray, 'relay_turn', qos)

    tp = node.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
    pen = node.create_client(SetPen, '/turtle1/set_pen')
    tp.wait_for_service()
    pen.wait_for_service()

    def call(client, req):
        future = client.call_async(req)
        rclpy.spin_until_future_complete(node, future)
        return future.result()

    def set_pen(off):
        req = SetPen.Request()
        req.r, req.g, req.b = COLOR
        req.width = 3
        req.off = off            
        call(pen, req)

    def goto(x, y):
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = float(x), float(y), 0.0
        call(tp, req)

    def draw_number(num):
        for i, ch in enumerate(str(num)):
            base_x = SLOT_X + i * 1.6        
            for s in DIGITS[ch]:
                (x1, y1), (x2, y2) = SEG[s]
                set_pen(1)                   
                goto(base_x + x1 * W, SLOT_Y + y1 * H)
                set_pen(0)                   
                goto(base_x + x2 * W, SLOT_Y + y2 * H)
        set_pen(1)

    state = {'turn': False, 'num': 0}

    def on_turn(msg):
        num, active = msg.data[0], msg.data[1]
        if active == MY_ID:
            state['turn'] = True
            state['num'] = num

    node.create_subscription(Int32MultiArray, 'relay_turn', on_turn, qos)

    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0.1)
        if not state['turn']:
            continue                         
        state['turn'] = False
        num = state['num']

        node.get_logger().info(f'member3 gambar angka {num}')
        draw_number(num)

        nxt = Int32MultiArray()
        nxt.data = [num + 1, NEXT_ID]
        pub.publish(nxt)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
