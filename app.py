
from sys import platform
import os, sys
import customtkinter
from PIL import Image
from matplotlib import pyplot as plt
from cpu_usage import CPUsage
from gpu_usage import GPUsage
from memory import MemoryUsage
from storage import StorageUsage
from pop_out_graph import Graph
from logs_util import save_log


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("InfoTech")
        self.geometry("780x450")
        customtkinter.set_appearance_mode("dark")
        self.resizable(False,False)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.iconbitmap(default=resource_path("app_images\\Infotech_logo.ico"))

        # Because CTkToplevel currently is bugged on windows
        # and doesn't check if a user specified icon is set
        # we need to set the icon again after 200ms
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(resource_path("app_images\\Infotech_logo.ico")))

        # load images with light and dark mode image
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(resource_path("app_images\\HW_tool.png"))), size=(26, 26))
        self.CPU_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(resource_path("app_images\\CPU_Light_Mode.png"))),
                                                dark_image=Image.open(os.path.join(resource_path("app_images\\CPU_Dark_Mode.png"))), size=(50, 50))
        self.GPU_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(resource_path("app_images\\GPU_Light_Mode.png"))),
                                                dark_image=Image.open(os.path.join(resource_path("app_images\\GPU_Dark_Mode.png"))), size=(50, 50))
        self.Memory_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(resource_path("app_images\\RAM_Light_Mode.png"))),
                                                     dark_image=Image.open(os.path.join(resource_path("app_images\\RAM_Dark_Mode.png"))), size=(50, 50))
        self.Storage_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(resource_path("app_images\\ROM_Light_Mode.png"))),
                                                     dark_image=Image.open(os.path.join(resource_path("app_images\\ROM_Dark_Mode.png"))), size=(50, 50))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0,fg_color='transparent')
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=0)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="HW Info Tool",image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"),padx=5)
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.cpu_usage_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="CPU Usage",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.CPU_image, anchor="w", command=self.cpu_usage_button_event)
        self.cpu_usage_button.grid(row=1, column=0, sticky="ew")

        self.gpu_usage_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="GPU Usage",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.GPU_image, anchor="w", command=self.gpu_usage_button_event)
        self.gpu_usage_button.grid(row=2, column=0, sticky="ew")

        self.memory_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Memory",
                                                       fg_color="transparent", text_color=("gray10","gray90"), hover_color=("gray70","gray30"),
                                                       image=self.Memory_image, anchor="w", command=self.memory_3_button_event)
        self.memory_3_button.grid(row=3, column=0, sticky="ew")

        self.storage_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Storage",
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        image=self.Storage_image, anchor="w",
                                                        command=self.storage_4_button_event)
        self.storage_4_button.grid(row=4, column=0, sticky="ew")

        # create a save logs button
        self.save_logs_button = customtkinter.CTkButton(self, text="Save Logs", command=self.save_logs)
        self.save_logs_button.place(x=20,y=390)

        # create CPU usage frame
        self.cpu_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.cpu_frame.grid_columnconfigure(0, weight=1)

        # display CPU Info and Graph in cpu_frame
        self.cpu_usage = CPUsage(self.cpu_frame)
        self.cpu_usage.pack(fill='both',expand=1)

        # create gpu usage frame
        self.gpu_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.gpu_frame.grid_columnconfigure(0, weight=1)

        # display GPU Info and Graph in gpu_frame
        self.gpu_usage = GPUsage(self.gpu_frame)
        self.gpu_usage.pack(fill='both',expand=1)

        # create memory frame
        self.memory_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.memory_frame.grid_columnconfigure(0, weight=1)

        # display Memory Info and Graph in memory_frame
        self.memory_usage = MemoryUsage(self.memory_frame)
        self.memory_usage.pack(fill='both',expand=1)

        # create storage frame
        self.storage_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.storage_frame.grid_columnconfigure(0, weight=1)

        # display Storage Info and Graph in storage_frame
        self.storage_usage = StorageUsage(self.storage_frame)
        self.storage_usage.pack(fill='both', expand=1)

        # Add a button to pop out the CPU graph
        pop_out_cpu_button = customtkinter.CTkButton(self.cpu_frame, text="POP OUT GRAPH",width=5,
                                                     command=lambda: self.pop_out_graph("CPU"))
        pop_out_cpu_button.place(x=50, y=255)

        # Add a button to pop out the GPU graph
        pop_out_gpu_button = customtkinter.CTkButton(self.gpu_frame, text="POP OUT GRAPH",width=5,
                                                     command=lambda: self.pop_out_graph("GPU"))
        pop_out_gpu_button.place(x=260, y=285)

        # select default frame
        self.select_frame_by_name("cpu_usage")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def pop_out_graph(self, graph_type):
        # Create a new window
        pop_out_window = Graph(self)
        pop_out_window.title(f"{graph_type} Graph")
        pop_out_window.geometry('600x300')
        pop_graph = pop_out_window

        # Check what button is pressed to determine what animation to start
        if graph_type == "CPU":
            pop_graph.start_cpu_animation()
        elif graph_type == "GPU":
            pop_graph.start_gpu_animation()

        # stop the animation and close the window
        def on_closing():
            if graph_type == "CPU":
                pop_graph.stop_cpu_animation()
                pop_out_window.destroy()
            elif graph_type == "GPU":
                pop_graph.stop_gpu_animation()
                pop_out_window.destroy()

        # a statement to add a function when closing the window
        pop_out_window.protocol("WM_DELETE_WINDOW", on_closing)

    # a function where the logs of utilization of hardware and information is save
    def save_logs(self):
        cpu_log_data = self.cpu_usage.get_cpu_log_data()
        save_log("cpu", cpu_log_data)

        gpu_log_data = self.gpu_usage.get_gpu_log_data()
        save_log("gpu", gpu_log_data)

        memory_log_data = self.memory_usage.get_memory_log_data()
        save_log("memory", memory_log_data)

        storage_log_data = self.storage_usage.get_storage_log_data()
        save_log("storage", storage_log_data)

    # functions to determine which frame is selected
    def cpu_usage_button_event(self):
        self.select_frame_by_name("cpu_usage")

    def gpu_usage_button_event(self):
        self.select_frame_by_name("gpu_usage")

    def memory_3_button_event(self):
        self.select_frame_by_name("memory_3")

    def storage_4_button_event(self):
        self.select_frame_by_name("storage_4")

    # stop the all plot animation and close the root window
    def on_closing(self):
        plt.close('all')
        self.quit()
        self.destroy()

    """function that configure the color of the button and close the other frames when specified frame 
        of the button is pressed"""
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.cpu_usage_button.configure(fg_color=("gray75", "gray25") if name == "cpu_usage" else "transparent")
        self.gpu_usage_button.configure(fg_color=("gray75", "gray25") if name == "gpu_usage" else "transparent")
        self.memory_3_button.configure(fg_color=("gray75", "gray25") if name == "memory_3" else "transparent")
        self.storage_4_button.configure(fg_color=("gray75", "gray25") if name == "storage_4" else "transparent")

        # show selected frame
        if name == "cpu_usage":
            self.cpu_frame.grid(row=0, column=1, sticky="nsew")
            self.cpu_usage.start_animation()
        else:
            self.cpu_frame.grid_forget()
            self.cpu_usage.stop_animation()

        if name == "gpu_usage":
            self.gpu_frame.grid(row=0, column=1, sticky="nsew")
            self.gpu_usage.start_animation()
        else:
            self.gpu_frame.grid_forget()
            self.gpu_usage.stop_animation()

        if name == "memory_3":
            self.memory_frame.grid(row=0, column=1, sticky="nsew")
            self.memory_usage.start_animation()
        else:
            self.memory_frame.grid_forget()
            self.memory_usage.stop_animation()

        if name == "storage_4":
            self.storage_frame.grid(row=0, column=1, sticky="nsew")
            self.storage_usage.start_animation()
        else:
            self.storage_frame.grid_forget()
            self.storage_usage.stop_animation()

