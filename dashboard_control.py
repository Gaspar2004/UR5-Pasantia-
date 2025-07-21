# dashboard_control.py
import socket
import time
#from config import DASHBOARD_IP, DASHBOARD_PORT
DASHBOARD_IP = "192.168.0.2"
DASHBOARD_PORT = 29999

def send_dashboard_command(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((DASHBOARD_IP, DASHBOARD_PORT))
        s.sendall((cmd + '\n').encode())
        time.sleep(0.5)
        response = s.recv(1024)
        print(f"Dashboard response: {response.decode().strip()}")

# Funciones para abrir y cerrar pinza ejecutando programas en el robot

def open_gripper():
    send_dashboard_command("load /programs/open_gripper.urp")
    send_dashboard_command("play")

def close_gripper():
    send_dashboard_command("load /programs/close_gripper.urp")
    send_dashboard_command("play")
