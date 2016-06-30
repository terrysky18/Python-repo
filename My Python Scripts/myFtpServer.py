from pyftpdlib import ftpserver

address = ("0.0.0.0", 21)
server = ftpserver.FTPServer(address, ftpserver.FTPHandler)
server.serve_forever()
