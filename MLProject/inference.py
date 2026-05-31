from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
import random
import psutil

app = Flask(__name__)

# ======================
# METRICS
# ======================

REQUEST_COUNT = Counter(
    'request_count_total',
    'Total Request'
)

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency'
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'CPU Usage'
)

MEMORY_USAGE = Gauge(
    'memory_usage_percent',
    'Memory Usage'
)

PREDICTION_TOTAL = Counter(
    'prediction_total',
    'Total Prediction'
)

# ======================
# MAIN ENDPOINT
# ======================

@app.route('/')
def home():

    REQUEST_COUNT.inc()

    start_time = time.time()

    # simulasi proses model
    time.sleep(random.random())

    latency = time.time() - start_time

    REQUEST_LATENCY.observe(latency)

    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

    PREDICTION_TOTAL.inc()

    return {
        "message": "Model inference success"
    }

# ======================
# METRICS ENDPOINT
# ======================

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

# ======================
# RUN APP
# ======================

if __name__ == '__main__':
    app.run(port=5000)