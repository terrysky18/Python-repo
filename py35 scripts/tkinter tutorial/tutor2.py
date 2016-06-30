"""
A short and simple script to demonstrate the use of tkinter in Python 3

The programme window is resizable and the widget is automatically resized
"""

import tkinter as tk

class Application(tk.Frame):
	# application class must inherit from tkinter's Frame class
	
	def __init__(self, master=None):
		# application class constructor
		
		# call the constructor for the parent class, Frame
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		self.createWidgets()

	def createWidgets(self):
		top = self.winfo_toplevel()			# parent of Application instance
		top.rowconfigure(0, weight=1)		# makes row 0 of top level stretchable
		top.columnconfigure(0, weight=1)	# makes col 0 of top level stretchable
		self.rowconfigure(0, weight=1)		# makes row 0 of widget stretchable
		self.columnconfigure(0, weight=1)		# makes col 0 of widget strtchable
		self._quitButton = tk.Button(self, text='Quit', command=self.quit)
		# widget expands to fill its cell
		self._quitButton.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)


app = Application()
app.master.title('Simple Button App')
app.master.geometry("250x100")
# start the event loop
app.mainloop()
