import multiprocessing
from app import App

if __name__ == "__main__":
    multiprocessing.freeze_support()  # prevent threading from happening when app is running on exe
    app = App()
    app.update_idletasks()
    app.mainloop()