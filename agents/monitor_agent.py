import sys
sys.path.append('/home/ubuntu/addylabs')
import subprocess
import datetime
from utils.litellm_client import chat
from config.prompts import MONITOR_AGENT_PROMPT
from config.settings import VPN_PEER_IP, LOGS_DIR

def check_vpn():
    result = subprocess.run(
        ["ping", "-c", "3", "-W", "5", VPN_PEER_IP],
        capture_output=True
    )
    return result.returncode == 0

def check_services():
    services = ["litellm", "rstudio-server", "piper-tts", "kokoro-tts", "wg-quick@wg0"]
    status = {}
    for svc in services:
        result = subprocess.run(
            ["systemctl", "is-active", svc],
            capture_output=True, text=True
        )
        status[svc] = result.stdout.strip()
    return status

def get_system_stats():
    import shutil
    import os
    disk = shutil.disk_usage("/")
    with open("/proc/loadavg") as f:
        load = f.read().split()[0]
    with open("/proc/meminfo") as f:
        meminfo = dict(line.split(":", 1) for line in f if ":" in line)
    mem_total = int(meminfo["MemTotal"].strip().split()[0])
    mem_free = int(meminfo["MemAvailable"].strip().split()[0])
    mem_used_pct = round((1 - mem_free / mem_total) * 100, 1)
    return {
        "load_avg": load,
        "memory_used_pct": mem_used_pct,
        "disk_used_pct": round(disk.used / disk.total * 100, 1)
    }

def run_monitor():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    vpn = check_vpn()
    services = check_services()
    stats = get_system_stats()
    report_data = f"""
Timestamp: {timestamp}
VPN Tunnel (10.0.0.1): {"UP" if vpn else "DOWN - ALERT"}
Services: {services}
Load Average: {stats['load_avg']}
Memory Used: {stats['memory_used_pct']}%
Disk Used: {stats['disk_used_pct']}%
"""
    print(report_data)
    summary = chat(report_data, system=MONITOR_AGENT_PROMPT)
    logfile = f"{LOGS_DIR}/monitor_{timestamp}.txt"
    with open(logfile, "w") as f:
        f.write(report_data + "\n\nAI Summary:\n" + summary)
    print("\nAI Summary:")
    print(summary)
    return summary

if __name__ == "__main__":
    run_monitor()
