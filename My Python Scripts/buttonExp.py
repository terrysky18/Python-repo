import Tkinter
import tkMessageBox

top = Tkinter.Tk()

def helloCallBack():
	tkMessageBox.showinfo('Testing Python', 'Testing window and button')

B = Tkinter.Button(top, text = 'Hello', command = helloCallBack)
B.pack()
top.mainloop()

