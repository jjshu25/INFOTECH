import os,sys
import customtkinter
from ani_graphs import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import wmi
import ctypes

# Check for AMD support and conditionally import pyadl
try:
    import pyadl
    _= pyadl.ADLManager.getInstance().getDevices()
    GPU_SUPPORT = False
except ImportError:
    pass
except Exception as amd_error:
    print(f"Unexpected error while checking for AMD support: {amd_error}")
    GPU_SUPPORT = True


def get_unsigned_int(value):
    return ctypes.c_uint32(value).value


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class GPUsage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # create a canvas for GPU and embed the plot on it
        self.canvas = FigureCanvasTkAgg(fig_gpu, master=self)
        self.canvas.get_tk_widget().pack(side='top')

        # create animations that updates the plot real time every 1 second
        self.ani_gpu = FuncAnimation(fig_gpu, animate_gpu, interval=2000, cache_frame_data=False)
        self.canvas.draw()

        # create a label widget to display GPU info
        self.gpu_info_label = customtkinter.CTkLabel(self, bg_color='transparent',justify='left',anchor='sw', font=("Comic Sans", 15, 'bold'), pady=80,
                                           padx=110)
        self.gpu_info_label.place(x=150,y=250)

        # help updates the plot smoothly
        self.update_idletasks()

        # display gpu information
        self.display_gpu_info(GPU_SUPPORT)

    def display_gpu_logo(self, gpu_name):
        if "NVIDIA" in gpu_name:
            gpu_brand_image_path = os.path.join(resource_path("app_images\\nvidia_logo.png"))
        elif "AMD" in gpu_name or "Radeon" in gpu_name:
            gpu_brand_image_path = os.path.join(resource_path("app_images\\radeon_logo.png"))
        elif "Intel" in gpu_name or "INTEL" in gpu_name or "Intel UHD Graphics" in gpu_name:
            gpu_brand_image_path = os.path.join(resource_path("app_images\\intel_logo.png"))
        else:
            gpu_brand_image_path = os.path.join(resource_path("app_images\\default_gpu.png"))
        if os.path.exists(gpu_brand_image_path):
            gpu_brand_image = customtkinter.CTkImage(Image.open(gpu_brand_image_path),size=(180,180))
        else:
            gpu_brand_image = customtkinter.CTkImage(Image.open(os.path.join(resource_path("app_images\\default.png"))),size=(180,180))
        self.gpu_logo_label = customtkinter.CTkLabel(self, image=gpu_brand_image,text="             ", bg_color='transparent',compound='right')
        self.gpu_logo_label.place(x=0,y=250)

    def stop_animation(self):
        self.ani_gpu.pause()

    def start_animation(self):
        self.ani_gpu.resume()

    def display_gpu_info(self, amd_flag=GPU_SUPPORT):
        global gpu_info
        try:
            if amd_flag:    
                # For Intel an Nvidia Support
                gpu_device = wmi.WMI().Win32_VideoController()
                for device in gpu_device:
                    gpu_info = (
                        f"{device.wmi_property('Name').value}\n"
                        f"GPU Memory: {round(get_unsigned_int(device.wmi_property('AdapterRAM').value)) / (1024 ** 3):.2f} GB"
                    )
                    self.display_gpu_logo(device.wmi_property('Name').value)
            else:
                from pyadl import ADLManager
                # For AMD Support
                adl_devices = ADLManager.getInstance().getDevices()
                for device in adl_devices:
                    gpu_info = (
                        f"{device.adapterIndex} {device.adapterName}\n"
                        f"Clock Speed: {device.getCurrentEngineClock()} MHz \n"
                        f"Temperature: {device.getCurrentTemperature()} Celsius"
                    )
                self.display_gpu_logo("AMD RADEON")
            self.gpu_info_label.configure(text=gpu_info)
            self.after(1000, self.display_gpu_info)
        except Exception as e:
            print(f"Error getting GPU information: {e}")
            self.gpu_info_label.configure(text="Error getting GPU information.")

    def get_gpu_log_data(self,amd_flag=GPU_SUPPORT):
        global gpu_info
        try:
            if amd_flag:    
                # For Intel an Nvidia Support
                gpu_device = wmi.WMI().Win32_VideoController()
                for device in gpu_device:
                    gpu_info = (
                        f"{device.wmi_property('Name').value}\n"
                        f"GPU Memory: {round(get_unsigned_int(device.wmi_property('AdapterRAM').value)) / (1024 ** 3):.2f} GB"
                    )
                    self.display_gpu_logo(device.wmi_property('Name').value)
            else:
                from pyadl import ADLManager
                # For AMD Support
                adl_devices = ADLManager.getInstance().getDevices()
                for device in adl_devices:
                    gpu_info = (
                        f"{device.adapterIndex} {device.adapterName}\n"
                        f"Clock Speed: {device.getCurrentEngineClock()} MHz \n"
                        f"Temperature: {device.getCurrentTemperature()}u'\xb0` Celsius"
                    )
                self.display_gpu_logo("AMD RADEON")
            self.gpu_info_label.configure(text=gpu_info)
            self.after(1000, self.display_gpu_info)
        except Exception as e:
            print(f"Error getting GPU information: {e}")
            self.gpu_info_label.configure(text="Error getting GPU information.")

        for i, usage in enumerate(y_gpu):
            gpu_info += f"{i + 1}: {usage:.2f}%\n\t"

        return gpu_info


