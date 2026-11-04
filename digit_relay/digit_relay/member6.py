# member6.py
# Node Anggota 6 (cyan), slot (x=8.0, y=1.5).
#
# Alur:
#   1. subscribe topic /relay_turn
#   2. kalau active_member == 6, gambar angkanya di slot di atas
#   3. siklus 1 (angka 6)  -> publish [7, 1] untuk mengoper giliran ke anggota 1
#   4. siklus 2 (angka 12) -> selesai, tidak mengoper giliran, node berhenti

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy
from std_msgs.msg import Int32MultiArray
from turtlesim.srv import TeleportAbsolute, SetPen

from digit_relay.digit_font import SEG, DIGITS

MY_ID = 6
NEXT_ID = 1                  # setelah anggota 6, giliran kembali ke anggota 1
COLOR = (0, 255, 255)        # cyan
SLOT_X, SLOT_Y = 8.0, 1.5    # posisi angka di kanvas

TOTAL = 12                   # angka terakhir (2 siklus)
W, H = 1.2, 2.5              # skala ukuran angka


def main():
    rclpy.init()
    node = Node('member6')

    # QoS "latched" (TRANSIENT_LOCAL), sama seperti member lain
    qos = QoSProfile(depth=10)
    qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
    pub = node.create_publisher(Int32MultiArray, 'relay_turn', qos)

    # Client service turtlesim
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
        req.off = off            # 1 = pena diangkat, 0 = pena diturunkan
        call(pen, req)

    def goto(x, y):
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = float(x), float(y), 0.0
        call(tp, req)

    def draw_number(num):
        for i, ch in enumerate(str(num)):
            base_x = SLOT_X + i * 1.6        # digit ke-2 digeser ke kanan
            for s in DIGITS[ch]:
                (x1, y1), (x2, y2) = SEG[s]
                set_pen(1)                   # angkat pena, pindah ke awal segmen
                goto(base_x + x1 * W, SLOT_Y + y1 * H)
                set_pen(0)                   # turunkan pena, tarik garis
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
            continue                         # idle, belum giliranku
        state['turn'] = False
        num = state['num']

        node.get_logger().info(f'member6 gambar angka {num}')
        draw_number(num)

        if num >= TOTAL:                     # angka 12 selesai -> sistem berhenti
            node.get_logger().info('member6 selesai, relay berhenti')
            break

        # Oper giliran kembali ke anggota 1 untuk siklus 2
        nxt = Int32MultiArray()
        nxt.data = [num + 1, NEXT_ID]
        pub.publish(nxt)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
