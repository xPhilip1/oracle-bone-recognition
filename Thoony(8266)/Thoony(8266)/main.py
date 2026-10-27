# from fpioa_manager import fm
import socket
import network
import time
from machine import UART,Pin,PWM,Timer
from time import sleep

IP = 0
yuyin = Pin(13, Pin.OUT)  # GPIO 2
yuyin.value(0)
# binding UART2 IO:6->RX, 8->TX
# fm.register(6, fm.fpioa.UART2_RX)
# fm.register(8, fm.fpioa.UART2_TX)
# yb_uart = UART(0, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
# yb_uart = UART(UART.UART0, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
yb_uart = UART(0, 115200, tx=Pin(1), rx=Pin(3))
# yb_uart = UART(1, baudrate=115200)
# yb_uart.init(115200, bits=8, parity=None, stop=1)
write_bytes = b'$hello yahboom#\n'
read_data = b'123'
last_time = time.ticks_ms()
# read_data1 = 'dddd'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('YOUR_WIFI_SSID', 'YOUR_WIFI_PASSWORD')
    
    while not wlan.isconnected():
        pass
print('网络配置:', wlan.ifconfig())

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
s.bind((wlan.ifconfig()[0],9090))# 连接wifi后将获取到的ip地址进行绑定
data,IP = s.recvfrom(1024)
try:
    while True:
        # send data per 500ms
        #data,IP = s.recvfrom(1024)
        buf = 'YOUR_WIFI_SSID' # 获取图像数据camera.capture()
        unicode_wang = '29579'
        unicode_tu = '22303'
        unicode_da = '22823'
        #s.sendto(buf,IP) # 向客户端发送图像数据''
#         yuyin.value(0)
#         if time.ticks_ms() - last_time > 5000:
#             last_time = time.ticks_ms()
#             yb_uart.write(write_bytes)
#             yuyin.value(1)
#             sleep(500)
#             s.sendto(buf,IP)
#             print("write_data = ", read_data)
        # read and print data
#         read_data = yb_uart.read(5)
#         if read_data:
#             print("read_data = ", read_data)        
        if yb_uart.any():
#             read_data = yb_uart.read()
#             yb_uart.write(read_data)
#             print("read_data = ", read_data)
            last_time = time.ticks_ms()
            read_data = yb_uart.read()
            if read_data == b'29579':
#                 yb_uart.write(read_data)
#                 while True:
#                     data,IP = s.recvfrom(1024)
                s.sendto(unicode_wang,IP) # 向客户端发送图像数据ll''
                print("Hello")
            elif read_data == b'22303':
                s.sendto(unicode_tu,IP)
            elif read_data == b'22823':
                s.sendto(unicode_da,IP)
#             elif uart.data == b'22303':
#                 s.sendto(unicode_tu,IP)
#             elif uart.data == b'22823':
#                 s.sendto(unicode_da,IP)
#                     yuyin.value(0)
#                     if time.ticks_ms() - last_time > 5000:
#                         last_time = time.ticks_ms()
#                         yuyin.value(1)
#             else:
#                 yb_uart.write(read_data)
#         if read_data == 'q555':
#             print("read_data = ", read_data)
#             while True:
#                 data,IP = s.recvfrom(1024)
#                 s.sendto(buf,IP) # 向客户端发送图像数据''
#         else:
#             print("read_data = ", read_data)        
except:
    pass

yb_uart.deinit()
del yb_uart
