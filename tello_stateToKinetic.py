# -----------------------------------------------
# 将 Tello 状态 数据整理并转发到 Kinetic Designer中
# 
# 2018/1/10 By Wason
#
# Version: V1.0
# -----------------------------------------------

# 加载模块
import socket
import threading
import time

# 启用 UDP 服务端
BUFSIZE = 1024
localserver_addr = ('0.0.0.0', 8890)
localserver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
localserver.bind(localserver_addr)
print("Bind UDP on prot:8890")

# 定义 Kinetic IP 地址以及 Port
kinetic_addr = ('192.168.1.64', 9800)
kinetic = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 数据处理
def position_x(data_list):
    x = data_list[1]
    new_x = x[2 : ]
    return new_x.zfill(4)

def position_y(data_list):
    y = data_list[2]
    new_y = y[2 : ]
    return new_y.zfill(4)

def position_z(data_list):
    z = data_list[3]
    new_z = z[2 : ]
    return new_z.zfill(4)

def pitch(data_list):
    p = data_list[5]
    new_p = p[6 : ]
    return new_p.zfill(4)

def roll(data_list):
    r = data_list[6]
    new_r = r[5 : ]
    return new_r.zfill(4)

def yaw(data_list):
    y = data_list[7]
    new_y = y[4 : ]
    return new_y.zfill(4)

def height(data_list):
    h = data_list[14]
    new_h = h[2 : ]
    return new_h.zfill(4)

def sendToKinetic(message):
    kinetic.sendto(message.encode(), kinetic_addr)
    # print("send succeed")

# 持续监听并发送数据
while True:
    data,addr = localserver.recvfrom(BUFSIZE)       # 获取 Tello 状态
    data = data.decode()                            # 数据解码
    data_list = data.split(';')                     # 生成数据列表
    # print("Receive massage:%s"% (position_x(data_list)))
    # print("%s%s%s%s"% (pitch(data_list), roll(data_list), yaw(data_list), height(data_list)))
    message = (
               pitch(data_list) + 
               roll(data_list) + 
               yaw(data_list) + 
               height(data_list) + 
               position_x(data_list) + 
               position_y(data_list) + 
               position_z(data_list)
               )
    sendToKinetic(message)
    print(data)