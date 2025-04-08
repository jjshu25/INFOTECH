from ani_graphs import *
import platform
import psutil
import cpuinfo
import customtkinter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import os, sys
from PIL import Image


#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class CPUsage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # get cpu information
        self.cpu_info = cpuinfo.get_cpu_info()
        self.cpu_brand = self.cpu_info.get('brand_raw', 'Unknown')
        self.cpu_cores = psutil.cpu_count(logical=False)
        self.cpu_arch = platform.processor()
        self.cpu_speed = psutil.cpu_freq().current / 1000

        # load cpu images
        if "Intel" in self.cpu_brand:
            cpu_brand_image_path = os.path.join(resource_path("app_images\\intel_logo.png"))
        elif "AMD" in self.cpu_brand:
            cpu_brand_image_path = os.path.join(resource_path("app_images\\ryzen_logo.png"))
        else:
            cpu_brand_image_path = os.path.join(resource_path("app_images\\default.png"))

        if os.path.exists(cpu_brand_image_path):
            cpu_brand_image = customtkinter.CTkImage(Image.open(cpu_brand_image_path),size=(180,135))
        else:
            cpu_brand_image = customtkinter.CTkImage(Image.open(os.path.join(resource_path("app_images\\default.png"))),
                                                          size=(200, 200))

        # declare a variable with all the values of cpu information
        self.system_info_text = f"""
        CPU: {self.cpu_brand} 
        Cores: {self.cpu_cores}
        CPU Architecture: 
        {self.cpu_arch}
        CPU Speed: {self.cpu_speed:.2f} GHz
        """

        # create a label for cpu information
        self.info_label = customtkinter.CTkLabel(self, text=self.system_info_text,
                                           justify='left', font=("Comic Sans", 15, 'bold'), bg_color='transparent', anchor='sw',padx=130,pady=40)
        self.info_label.pack(side='bottom')
        self.cpu_brand_image_label = customtkinter.CTkLabel(self,text='  ', image=cpu_brand_image, bg_color='transparent', compound='right')
        self.cpu_brand_image_label.place(x=0, y=285)

        # create a canvas for CPU and embed the plot on it
        self.canvas = FigureCanvasTkAgg(fig_cpu, master=self)
        self.canvas.get_tk_widget().pack(side='top')
        self.canvas.draw()

        # create the animation that updates the plot realtime every 1 second
        self.ani = FuncAnimation(fig_cpu, animate_cpu, interval=1000, cache_frame_data=False)

        # help updates the plot smoothly
        self.update_idletasks()

        # start the CPU speed update loop
        self.update_cpu_speed()

    # function to update the CPU speed display
    def update_cpu_speed(self):
        self.cpu_count = psutil.cpu_count()
        self.cpu_utilization = psutil.cpu_percent(interval=1, percpu=True)
        self.cpu_speed = sum(self.cpu_utilization) / self.cpu_count * 100 / 1000
        self.system_info_text = f"""
                    CPU: {self.cpu_brand} 
                    Cores: {self.cpu_cores}
                    CPU Architecture: 
                    {self.cpu_arch}
                    CPU Speed: {self.cpu_speed:.2f} GHz
                    """
        self.info_label.configure(text=self.system_info_text)
        self.after(1000, self.update_cpu_speed)  # Update every 1 second

    def stop_animation(self):
        self.ani.pause()  # pause the FuncAnimation Statement

    def start_animation(self):
        self.ani.resume()  # resume the FuncAnimation Statement

    # function that get the cpu data and return it to log_data
    def get_cpu_log_data(self):
        self.cpu_info = cpuinfo.get_cpu_info()
        self.cpu_brand = self.cpu_info.get('brand_raw', 'Unknown')
        self.cpu_cores = psutil.cpu_count(logical=False)
        self.cpu_arch = platform.processor()
        self.cpu_speed = psutil.cpu_freq().current / 1000

        log_data = f"""
        CPU Information:
        Brand: {self.cpu_brand}
        Cores: {self.cpu_cores}
        Architecture: {self.cpu_arch}
        Speed: {self.cpu_speed:.2f} GHz
    
        CPU Usage History:
        """

        for i, usage in enumerate(y_cpu):
            log_data += f"{i + 1}: {usage:.2f}%\n\t"

        return log_data

