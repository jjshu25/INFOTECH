import customtkinter
from ani_graphs import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MemoryUsage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1)

        # create a canvas for memory usage and embed the plot on it
        self.canvas = FigureCanvasTkAgg(fig_mem, master=self)
        self.canvas.get_tk_widget().pack(fill='both')

        # create animations that updates the plot real time every 1 second
        self.ani = FuncAnimation(fig_mem, animate_mem, interval=1000, cache_frame_data=False)
        self.canvas.draw()

        # create a label widget to display memory info
        self.memory_info_label = customtkinter.CTkLabel(self, text="", wraplength=400, bg_color='transparent', justify='left', font=("Comic Sans", 15, 'bold'), pady=80,
        padx=210)
        self.memory_info_label.pack(side='bottom')
        self.display_memory_info()

    def stop_animation(self):
        self.ani.pause()

    def start_animation(self):
        self.ani.resume()

    def display_memory_info(self):
        try:
            virtual_memory = psutil.virtual_memory()
            used_memory = virtual_memory.used
            total_memory = virtual_memory.total
            free_memory = virtual_memory.free
            memory_usage_percentage = (used_memory / total_memory) * 100

            memory_info = (
                f"Total Memory: {total_memory / (1024 ** 2):.2f} GB\n"
                f"Used Memory: {used_memory / (1024 ** 2):.2f} GB\n"
                f"Free Memory: {free_memory / (1024 ** 2):.2f} GB\n"
                f"Memory Utilization: {memory_usage_percentage:.2f}%"
            )
            self.memory_info_label.configure(text=memory_info)
        except Exception as e:
            print(f"Error getting memory information: {e}")
            self.memory_info_label.configure(text="Error getting memory information.")

    def get_memory_log_data(self):

        virtual_memory = psutil.virtual_memory()
        used_memory = virtual_memory.used
        total_memory = virtual_memory.total
        free_memory = virtual_memory.free
        memory_usage_percentage = (used_memory / total_memory) * 100

        memory_info = (
            f"Total Memory: {total_memory / (1024 ** 2):.2f} GB\n"
            f"Used Memory: {used_memory / (1024 ** 2):.2f} GB\n"
            f"Free Memory: {free_memory / (1024 ** 2):.2f} GB\n"
            f"Memory Utilization: {memory_usage_percentage:.2f}%\n"
            f"Memory Usage History: \n\t"
        )

        for i, usage in enumerate(y_mem):
            memory_info += f"{i + 1}: {usage:.2f}%\n\t"
        return memory_info