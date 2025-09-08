import os

# Bind to the port Render provides (or 5000 locally)
bind = "0.0.0.0:" + os.getenv("PORT", "5000")

# Number of worker processes
workers = 2

# Use threaded workers instead of gevent (no extra deps required)
worker_class = "gthread"

# Number of threads per worker
threads = 4

# Timeout in seconds (increase if requests take longer)
timeout = 120

# Optional: preload app for faster worker startup
preload_app = True
