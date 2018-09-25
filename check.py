#! /usr/bin/python3
from proxiesGet import IpGet
import time
if __name__ == '__main__':
	ip = IpGet()
	ip.checkIp()
	ip.client.close()
	t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	str = '执行时间：' + t + '\n'
	print(str)