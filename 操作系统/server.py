import socket
import time
from multiprocessing import Process, Queue , Lock
sk = socket.socket()
sk.bind(("192.168.3.4", 5008))
sk.listen(10)
command_list = {"帮助":"help",
     "时间":"time",
     "计算器":"computer",
     "Python控制台":"python",
     "历史记录":"history",
     "清空历史记录":"del history",
     "查看本机Ipv4地址":"ipconfig",
     "分析网页源码":"get url",
     "RGB转十六进制":"RGB -> hex",
     "连接云电脑":"connect cloud computer",
     "测试概率":"text random"}
print("服务器启动成功,端口号:5000()")
while True:
    conn, addr = sk.accept()
    print("客户端ip+端口:", addr)
    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
        except:
            break
        if not data:
            break
        if data == "ipconfig cloud computer":
            conn.send("192.168.3.4".encode("utf-8"))
        if data == "help":
            for i, j in command_list.items():
                conn.send((i+j).encode("utf-8"))
                time.sleep(0.5)
        print("客户端发过来的数据:", data)
        if data == "exit":
            break
        conn.send(data.upper().encode("utf-8"))
    conn.close()

