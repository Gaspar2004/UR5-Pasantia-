import socket
import time

DASHBOARD_IP = "192.168.0.2"  # Replace with your robot's IP
DASHBOARD_PORT = 29999

def send_dashboard_command(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((DASHBOARD_IP, DASHBOARD_PORT))
        s.sendall((cmd + '\n').encode())
        time.sleep(0.5)
        response = s.recv(1024)
        print(f"Dashboard response: {response.decode().strip()}")

# Step 1: Load the program
send_dashboard_command("load /programs/grptest3.urp")

# Step 2: Play the program
send_dashboard_command("play")
