import multiprocessing
import os

# Bind to the correct host/port
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# For ML workloads, keep workers small (CPU + RAM sensitive)
workers = multiprocessing.cpu_count() * 2 + 1

# Use gevent worker class for async I/O
worker_class = "gevent"

# Timeout in seconds (inference might take time, so keep it high)
timeout = 180

# Restart workers after a number of requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload app so models load once, not per worker
preload_app = True
