import customtkinter
from matplotlib.animation import FuncAnimation
from ani_graphs import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys, os
from sys import platform


#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Graph(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.iconbitmap(default=resource_path("app_images\\Infotech_logo.ico"))

        # Because CTkToplevel currently is bugged on windows
        # and doesn't check if a user specified icon is set
        # we need to set the icon again after 200ms
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(resource_path("app_images\\Infotech_logo.ico")))

        # create animations that updates the plot real time every 1 second
        self.ani_cpu = FuncAnimation(fig_pop_cpu, ani_pop_cpu, interval=1000, cache_frame_data=False)

        # create animation that updates the plot realtime every 1 second
        self.ani_gpu = FuncAnimation(fig_pop_gpu, ani_pop_gpu, interval=2000, cache_frame_data=False)

    def start_cpu_animation(self):
        # create a canvas for CPU and embed the plot on it
        self.canvas = FigureCanvasTkAgg(fig_pop_cpu, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=1)
        self.canvas.draw()
        self.ani_cpu.event_source.start()

    def stop_cpu_animation(self):
        self.ani_cpu.event_source.stop()
    def start_gpu_animation(self):
        # create a canvas for GPU and embed the plot on it
        self.canvas_gpu = FigureCanvasTkAgg(fig_pop_gpu, master=self)
        self.canvas_gpu.get_tk_widget().pack(fill='both', expand=1)
        self.canvas_gpu.draw()
        self.ani_gpu.event_source.start()

    def stop_gpu_animation(self):
        self.ani_gpu.event_source.stop()


