import psutil
import subprocess as sp
import matplotlib.pyplot as plt

# create a subplot type graphs
fig_cpu, ax_cpu = plt.subplots(figsize=(6, 2.5))
fig_gpu, ax_gpu = plt.subplots(figsize=(6, 2.5))
fig_mem, ax_mem = plt.subplots(figsize=(6, 3))
fig_read_write, (read_ax, write_ax) = plt.subplots(1, 2, figsize=(6, 2.5))
fig_pop_cpu, ax_pop_cpu = plt.subplots(figsize=(6, 3))
fig_pop_gpu, ax_pop_gpu = plt.subplots(figsize=(6, 3))

# create the yaxis and length variables
frame_len = 100
y_cpu = []
y_gpu = []
y_mem = []
read_y = []
write_y = []
y_pop_cpu = []
y_pop_gpu = []

# powershell command to display the GPU usage for NVIDIA and Intel
gpu_usage_cmd = r'(((Get-Counter "\GPU Engine(*engtype_3D)\Utilization Percentage").CounterSamples | where CookedValue).CookedValue | measure -sum).sum'


# Check for AMD support and conditionally import pyadl
try:
    import pyadl
    _ = pyadl.ADLManager.getInstance().getDevices()
    AMD_SUPPORTED = False
except ImportError:
    pass
except Exception as amd_error:
    print(f"Unexpected error while checking for AMD support: {amd_error}")
    AMD_SUPPORTED = True


# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent()


# Function to get GPU usage
def get_gpu_usage(command, amd_flag=AMD_SUPPORTED):
    try:
        if amd_flag:
            # For Nvidia and Intel Support
            val = sp.run(['powershell', '-Command', command], capture_output=True, text=True, stderr=sp.DEVNULL, stdout=sp.PIPE).stdout.strip()

            return float(val.strip().replace(',', '.'))
        else:
            # For AMD Support
            from pyadl import ADLManager
            adl_devices = ADLManager.getInstance().getDevices()
            adl_device = adl_devices[0]
            usage = adl_device.getCurrentUsage()
            return usage / 100  # Convert to percentage
            
    except Exception as e:
        print(f"Error getting GPU usage: {e}")
        return 0

# Function to get Memory usage
def get_memory_usage():
    try:
        virtual_memory = psutil.virtual_memory()
        used_memory = virtual_memory.used
        total_memory = virtual_memory.total
        memory_usage_percentage = (used_memory / total_memory) * 100
        return memory_usage_percentage
    except Exception as e:
        print(f"Error getting memory usage: {e}")
        return 0

# Function to get Storage read usage
def get_read_usage():
    try:
        disk_io = psutil.disk_io_counters()
        total_io = disk_io.read_count + disk_io.write_count
        read_usage_percent = (disk_io.read_count / total_io) * 100 if total_io > 0 else 0
        return read_usage_percent
    except Exception as e:
        print(f"Error getting read usage: {e}")
        return 0

# Function to get Storage write usage
def get_write_usage():
    try:
        disk_io = psutil.disk_io_counters()
        total_io = disk_io.read_count + disk_io.write_count
        write_usage_percent = (disk_io.write_count / total_io) * 100 if total_io > 0 else 0
        return write_usage_percent
    except Exception as e:
        print(f"Error getting write usage: {e}")
        return 0


# Function to update and draw CPU the plot graph
def animate_cpu(frame_data):
    cpu_usage = get_cpu_usage()
    y_cpu.append(cpu_usage)
    if len(y_cpu) > frame_len:
        y_cpu.pop(0)
    ax_cpu.cla()
    x = list(range(len(y_cpu)))
    fig_cpu.set_facecolor('#333333')
    ax_cpu.set_facecolor('#333333')
    ax_cpu.tick_params(colors='white')
    ax_cpu.plot(x, y_cpu, 'turquoise', label='CPU Utilization')
    ax_cpu.fill_between(x, y_cpu, color='#40E0D0', alpha=0.5)
    ax_cpu.set_xlabel('Time', color='white')
    ax_cpu.set_ylabel('CPU Utilization (%)', color='white')
    ax_cpu.set_title('Real-Time CPU Usage', color='white')
    ax_cpu.set_ylim(0, 100)
    fig_cpu.tight_layout()


# Function to update and draw GPU the plot graph
def animate_gpu(frame_data):
    gpu_usage = round(get_gpu_usage(gpu_usage_cmd),2)
    y_gpu.append(gpu_usage)

    if len(y_gpu) > frame_len:
        y_gpu.pop(0)

    ax_gpu.cla()
    x = list(range(len(y_gpu)))
    fig_gpu.set_facecolor('#333333')
    ax_gpu.set_facecolor('#333333')
    ax_gpu.tick_params(colors='white')
    ax_gpu.plot(x, y_gpu, 'turquoise', label='GPU Utilization')
    ax_gpu.fill_between(x, y_gpu, color='#40E0D0', alpha=0.5)
    ax_gpu.set_title('Real-Time GPU Usage', color='white')
    ax_gpu.set_xlabel('Time', color='white')
    ax_gpu.set_ylabel('GPU Utilization (%)', color='white')
    ax_gpu.set_ylim(0, 100)
    fig_gpu.tight_layout()

# Function to update and draw memoru the plot graph
def animate_mem(frame_data):
    mem_usage = get_memory_usage()
    y_mem.append(mem_usage)

    if len(y_mem) > frame_len:
        y_mem.pop(0)

    ax_mem.cla()
    x = list(range(len(y_mem)))
    fig_mem.set_facecolor('#333333')
    ax_mem.set_facecolor('#333333')
    ax_mem.tick_params(colors='white')
    ax_mem.plot(x, y_mem, 'turquoise', label='Memory Utilization')
    ax_mem.fill_between(x, y_mem, color='#40E0D0', alpha=0.5)
    ax_mem.set_title('Real-Time Memory Usage', color='white')
    ax_mem.set_xlabel('Time', color='white')
    ax_mem.set_ylabel('Memory Utilization (%)', color='white')
    ax_mem.set_ylim(0, 100)
    fig_mem.tight_layout()

# Function to update and draw read usage in storage the plot graph
def animate_read(frame_data):
    read_usage = get_read_usage()
    read_y.append(read_usage)
    if len(read_y) > frame_len:
        read_y.pop(0)
    read_ax.cla()
    x = list(range(len(read_y)))
    fig_read_write.set_facecolor('#333333')
    read_ax.set_facecolor('#333333')
    read_ax.tick_params(colors='white')
    read_ax.plot(x, read_y, 'turquoise', label='Read Utilization')
    read_ax.fill_between(x, read_y, color='#40E0D0', alpha=0.5)
    read_ax.set_title('Real-Time Disk Read Usage', color='white')
    read_ax.set_xlabel('Time', color='white')
    read_ax.set_ylabel('Read Utilization (%)', color='white')
    read_ax.set_ylim(0, 100)
    fig_read_write.tight_layout()

# Function to update and draw write usage in storage the plot graph
def animate_write(frame_data):
    write_usage = get_write_usage()
    write_y.append(write_usage)
    if len(write_y) > frame_len:
        write_y.pop(0)
    write_ax.cla()
    x = list(range(len(write_y)))
    fig_read_write.set_facecolor('#333333')
    write_ax.set_facecolor('#333333')
    write_ax.tick_params(colors='white')
    write_ax.plot(x, write_y, 'turquoise', label='Write Utilization')
    write_ax.fill_between(x, write_y, color='#40E0D0', alpha=0.5)
    write_ax.set_title('Real-Time Disk Write Usage', color='white')
    write_ax.set_xlabel('Time', color='white')
    write_ax.set_ylabel('Write Utilization (%)', color='white')
    write_ax.set_ylim(0, 100)
    fig_read_write.tight_layout()


# Function to update and draw CPU the plot graph for pop up
def ani_pop_cpu(frame_data):
    cpu_usage = get_cpu_usage()
    y_pop_cpu.append(cpu_usage)
    if len(y_pop_cpu) > frame_len:
        y_pop_cpu.pop(0)
    ax_pop_cpu.cla()
    x = list(range(len(y_pop_cpu)))
    fig_pop_cpu.set_facecolor('#333333')
    ax_pop_cpu.set_facecolor('#333333')
    ax_pop_cpu.tick_params(colors='white')
    ax_pop_cpu.plot(x, y_pop_cpu, 'turquoise', label='CPU Utilization')
    ax_pop_cpu.fill_between(x, y_pop_cpu, color='#40E0D0', alpha=0.5)
    ax_pop_cpu.set_xlabel('Time', color='white')
    ax_pop_cpu.set_ylabel('CPU Utilization (%)', color='white')
    ax_pop_cpu.set_title('Real-Time CPU Usage', color='white')
    ax_pop_cpu.set_ylim(0, 100)
    fig_pop_cpu.tight_layout()


# Function to update and draw GPU the plot graph for pop up
def ani_pop_gpu(frame_data):
    gpu_usage = round(get_gpu_usage(gpu_usage_cmd),2)
    y_pop_gpu.append(gpu_usage)

    if len(y_pop_gpu) > frame_len:
        y_pop_gpu.pop(0)

    ax_pop_gpu.cla()
    x = list(range(len(y_pop_gpu)))
    fig_pop_gpu.set_facecolor('#333333')
    ax_pop_gpu.set_facecolor('#333333')
    ax_pop_gpu.tick_params(colors='white')
    ax_pop_gpu.plot(x, y_pop_gpu, 'turquoise', label='GPU Utilization')
    ax_pop_gpu.fill_between(x, y_pop_gpu, color='#40E0D0', alpha=0.5)
    ax_pop_gpu.set_title('Real-Time GPU Usage', color='white')
    ax_pop_gpu.set_xlabel('Time', color='white')
    ax_pop_gpu.set_ylabel('GPU Utilization (%)', color='white')
    ax_pop_gpu.set_ylim(0, 100)
    fig_pop_gpu.tight_layout()


