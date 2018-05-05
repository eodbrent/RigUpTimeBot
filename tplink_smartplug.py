# BORROWED, BUT IT ONLY WORKED IN PYTHON 2, SO CHANGES WERE MADE TO WORK WITH PYTHON 3,
#   AND A DISCORD BOT.
#   see softScheck/tplink-smartplug for original
#
import socket
# import argparse #argparse removed due to difficulty making it consistently functional.

version = 0.2  #0.2 is my version, 0.1 was the original.
port = 9999
command = ""
ip = ""
# Check if IP is valid
def validIP(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:
		 return "Invalid IP Address. " + ip
	return ip

#setter - ip (I know this can be more 'pythonic'...I'm still learning, leave me alone.)
def setIP(ip):
    ip = ip


# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
#NEW FUNCTION THAT WORKS WITH BOTH PYTHON 2 and 3 (thanks stackoverflow)
def encrypt(string):
    key = 171
    result = bytearray(b"\0\0\0\0")
    for i in bytearray(string):
        a = key ^ i
        key = a
        result.append(a)
    return result

#NEW FUNCTION THAT WORKS WITH BOTH PYTHON 2 and 3
def decrypt(string):
	key = 171
	result = ""
	for i in bytearray(string):
		a = key ^ i
		key = i
		result += chr(a)
	return result


def sendCmd(cmd):
    # Send command and receive reply
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((ip, port))
        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()

        print ("Sent:     ", cmd)
        #print ("Received: ", decrypt(data[4:]))
    except socket.error:
        quit("Cound not connect to host " + ip + ":" + str(port))
