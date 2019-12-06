import socket
import threading
import time

def enc(in_str):
    res = cipher(in_str, 3, 3)
    return res


def decode(in_str):
    res = cipher(in_str, -3, -3)
    return res

def cipher(in_str, step, step1):
    alpha = ' abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNMабвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЧШЩЬЮЯ0123456789'
    res = ''
    digit = ''
    for c in in_str:
        if c.isalpha():
            if digit:
                res += str(int(digit) + int(step1))
                digit = ''
            res += alpha[(alpha.index(c) + step) % len(alpha)]
        elif c == ' ':
            if digit:
                res += str(int(digit) + int(step1))
                digit = ''
            res += c
        elif c.isnumeric():
            digit += c
        else:
            res += c
    if digit:
        res += str(int(digit) + int(step1))
    return res

key = 1

shutdown = False
join = False


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                decrypt = data.decode("utf-8")
                if not ("чату" in decrypt):
                    decrypt = decode(decrypt)
                print(decrypt)

                time.sleep(0.2)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.0.108", 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = input("Name: ")

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

while not shutdown:
    if not join:
        s.sendto(("[" + alias + "] => joined chat ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()
            message = enc(message)
            if message != "":
                s.sendto(("[" + alias + "] :: " + message).encode("utf-8"), server)

            time.sleep(0.2)
        except:
            s.sendto(("[" + alias + "] <= left chat ").encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()