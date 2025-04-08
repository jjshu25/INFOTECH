import customtkinter
from ani_graphs import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StorageUsage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Get disk information
        self.disk_info = self.get_disk_info()

        # Create canvas and animations
        self.canvas = FigureCanvasTkAgg(fig_read_write, master=self)
        self.canvas.get_tk_widget().pack(side='top')

        # Create the animation of read and write graphs
        self.ani_read = FuncAnimation(fig_read_write, animate_read, interval=1000, cache_frame_data=False)
        self.ani_write = FuncAnimation(fig_read_write, animate_write, interval=1000, cache_frame_data=False)
        self.canvas.draw()

        # Create label for storage information
        self.storage_info_label = customtkinter.CTkLabel(self, text="", wraplength=400, bg_color='transparent', justify='left',
                                                        font=("Comic Sans", 15, 'bold'), pady=80,
                                                        padx=210)
        self.storage_info_label.pack(side='bottom')

        # display storage information
        self.get_storage_info()

        # help updates the plot smoothly
        self.update_idletasks()

    def get_disk_info(self):
        try:
            disk = psutil.disk_partitions()[0]
            return disk
        except Exception as e:
            print(f"Error getting disk information: {e}")
            return None

    def get_storage_info(self):
        if self.disk_info:
            disk_name = self.disk_info.device
            disk_total = psutil.disk_usage(self.disk_info.mountpoint).total / (1024 ** 3)
            disk_used = psutil.disk_usage(self.disk_info.mountpoint).used / (1024 ** 3)
            disk_free = psutil.disk_usage(self.disk_info.mountpoint).free / (1024 ** 3)
            storage_text = (
                f"Disk Name: {disk_name}\n"
                f"Total Disk Space: {disk_total:.2f} GB\n"
                f"Used Disk Space: {disk_used:.2f} GB\n"
                f"Free Disk Space: {disk_free:.2f} GB"
            )
        else:
            return "Error getting disk information."
        self.storage_info_label.configure(text=storage_text)

    def get_storage_log_data(self):
        disk_name = self.disk_info.device
        disk_total = psutil.disk_usage(self.disk_info.mountpoint).total / (1024 ** 3)
        disk_used = psutil.disk_usage(self.disk_info.mountpoint).used / (1024 ** 3)
        disk_free = psutil.disk_usage(self.disk_info.mountpoint).free / (1024 ** 3)
        read_text = (
            f"Disk Name: {disk_name}\n"
            f"Total Disk Space: {disk_total:.2f} GB\n"
            f"Used Disk Space: {disk_used:.2f} GB\n"
            f"Free Disk Space: {disk_free:.2f} GB\n"
            f"Read Usage History: \n\t"
        )
        write_text = (
            f"Write Usage History: \n\t"
        )

        for i, read_usage in enumerate(read_y):
            read_text += f"{i + 1}: {read_usage:.2f}%\n\t"

        for i, write_usage in enumerate(write_y):
            write_text += f"{i + 1}: {write_usage:.2f}%\n\t"

        return read_text, write_text

    def stop_animation(self):
        self.ani_read.pause()
        self.ani_write.pause()

    def start_animation(self):
        self.ani_read.resume()
        self.ani_write.resume()