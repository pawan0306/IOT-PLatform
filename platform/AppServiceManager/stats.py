import psutil
print(psutil.cpu_times_percent(interval=1).idle)
print(psutil.virtual_memory().percent)