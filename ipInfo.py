import socket
import subprocess

def get_ip_address():
    try:
        # Connect to an external host to force the system to use the default interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error: {e}"

def get_wifi_name():
    try:
        # Uses iwgetid to get the current WiFi SSID
        result = subprocess.check_output(["iwgetid", "-r"]).decode().strip()
        return result if result else "Not connected to Wi-Fi"
    except subprocess.CalledProcessError:
        return "Wi-Fi interface not found or not connected"

if __name__ == "__main__":
    ip = get_ip_address()
    ssid = get_wifi_name()

    print(f"IP Address: {ip}")
    print(f"Wi-Fi SSID: {ssid}")