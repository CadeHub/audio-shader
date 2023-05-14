# from gui import GUI

# gui = GUI()
# gui.launch_gui()

from app import App

# create the application
myapp = App()

#
# here are method calls to the window manager class
#
myapp.master.title("My Do-Nothing Application")
myapp.master.maxsize(1000, 800)

# start the program
myapp.mainloop()
