"""
simple programme with a GUI using tkinter
"""

from tkinter import *

# create application window
root = Tk()

# modify root window
root.title("Simple Programme title")
root.geometry("350x225")

# make a frame
app = Frame(root)
# put app in a grid
app.grid()

# make a label
label = Label(app, text="This is a simple message")
# put label in a grid
label.grid()

# make a button, put it in grid
button1 = Button(app, text="Button1")
button1.grid()

# make another button, put it in grid
button2 = Button(app)
button2.grid()
# configure button2
button2.configure(text="random name")

# another button
button3 = Button(app)
button3.grid()
button3["text"] = "anything"

# kick off the event loop
# GUI application is event driven
root.mainloop()
