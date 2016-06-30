# An example script to demonstrate accessing VBScript from python

import win32com.client

# create a VBhost object
vbhost = win32com.client.Dispatch("WScript.Shell")
# vbhost.Language = "VBScript"
# vbhost.AddCode("Function two(x)\ntwo=2*x\nEnd Function\n")
# vbhost.Eval("two(2)")

vbs_file = 'C:\\Users\\jsong\\Documents\\VBScripts\\exampl1.vbs'
vbhost.Run(vbs_file)

