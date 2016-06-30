"""
A short and simple script to demonstrate the use of tkinter in Python 3

The programme only contains a Quit button
"""

import tkinter as tk

class Application(tk.Frame):
	# application class must inherit from tkinter's Frame class
	
	def __init__(self, master=None):
		# application class constructor
		
		# call the constructor for the parent class, Frame
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		# create a button labelled Quit
		self._quitButton = tk.Button(self, text="Quit", command=self.quit)
		self._quitButton.grid()


app = Application()
app.master.title('Simple Button App')
app.master.geometry("250x100")
# start the event loop
app.mainloop()
