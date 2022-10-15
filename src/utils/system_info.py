import psutil

def get_ram_mb(): 
    free_ram = psutil.virtual_memory()[0]
    return int(free_ram / (10**6))

def get_cpus(): 
    return psutil.cpu_count()
    
def get_disk_memory_gb():
    free_disk_memory = psutil.disk_usage('/')[2]
    return int(free_disk_memory / (10**9))
        