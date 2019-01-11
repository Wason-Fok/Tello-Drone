# 调用模块
import socket
import threading
import time

# Tello IP地址以及 Port
tello_address = ('192.168.10.1', 8889)

# 本地 IP 地址以及 Port
local_address = ('', 9010)

# 创建 UDP socket 连接
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定本地 IP 以及端口
sock.bind(local_address)

# 向 Tello 发送命令并等待
def send(message, delay):
  # 尝试向 Tello 发送命令并打印输出
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # 等待时间
  time.sleep(delay)

# 从 Tello 接受信息
def receive():
  # 持续监听接收消息
  while True:
    # 尝试从 Tello 接受消息
    try:
      response, ip_address = sock.recvfrom(128)
      print("Received message: " + response.decode(encoding='utf-8'))
    except Exception as e:
      # 如果发生错误，跳出循环，关闭连接
      sock.close()
      print("Error receiving: " + str(e))
      break

# 创建并启动一个在后台运行的监听线程
# 调用 receive() 函数，并将持续监听传入的消息
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

# Each leg of the box will be 100 cm. Tello uses cm units by default.
box_leg_distance = 100

# Yaw 90 degrees
yaw_angle = 90

# Yaw clockwise (right)
yaw_direction = "cw"

# 设置 Tello 为命令模式
send("command", 3)

# 发送起飞命令
# send("takeoff", 8)

# Loop and create each leg of the box
for i in range(100):
  # Fly forward
  send("battery?", 15)

# Land
# send("land", 5)

# Print message
print("Mission completed successfully!")

# Close the socket
sock.close()