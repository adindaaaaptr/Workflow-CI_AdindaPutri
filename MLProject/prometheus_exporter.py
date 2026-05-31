from prometheus_client import start_http_server, Gauge, Counter
import psutil
import time

# CPU
cpu_usage = Gauge('cpu_usage_percent', 'CPU Usage')

# RAM
memory_usage = Gauge('memory_usage_percent', 'Memory Usage')

# Disk
disk_usage = Gauge('disk_usage_percent', 'Disk Usage')

# Network
network_sent = Gauge('network_sent_bytes', 'Network Sent')

# Request Counter
request_count = Counter('prediction_request_total', 'Total Prediction Requests')

# Error Counter
error_count = Counter('prediction_error_total', 'Total Prediction Errors')

# Latency
latency_metric = Gauge('prediction_latency_seconds', 'Prediction Latency')

# Uptime
uptime_metric = Gauge('system_uptime_seconds', 'System Uptime')

start_time = time.time()

def collect_metrics():
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    disk_usage.set(psutil.disk_usage('/').percent)
    network_sent.set(psutil.net_io_counters().bytes_sent)
    uptime_metric.set(time.time() - start_time)

if __name__ == '__main__':
    start_http_server(8000)

    while True:
        collect_metrics()
        time.sleep(5)