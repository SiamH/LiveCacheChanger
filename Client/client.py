##########################SIAMH 02/06/2017##################################################
# Client communicates with Server via TCP and gets answers of it's valid commands

import socket
import sys

class cClient(object):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Bind(self, address, port):
        try:
            # Bind the socket to the port
            server_address = (address, port)
            print 'Use exit or Ctrl + C to quit'
            print 'connecting to ' + str(address) + ' port: ' + str(port)
            self.sock.connect(server_address)
            return True
        except:
            print 'failed to connect with ' + str(address) + ' on port: ' + str(port)
            return False

    def helpmenu():
        print "<------Four Basic operations ------>"
        print "Format of SET Operation: SET KEY=VALUE"
        print "Format of EXPAND Operation: EXPAND MSG, ${KEY}"
        print "Format of DELETE Operation: DEL KEY"
        print "Format of LIST Operation: LIST"
        print "<---------------------------------->"

    def SendMessage(self):
            try:
                while True:
                    message = raw_input().strip()
                    self.sock.sendall(message)
                    if message == 'exit':
                        break
                    data = self.sock.recv(512)
                    print data
            except KeyboardInterrupt:
                self.sock.sendall('exit')
                self.sock.close()
                print 'Client has been stopped.'
            except:
                self.sock.close()
                print 'Service is interrupted.'

            finally:
                print 'Closing socket'
                self.sock.close()

if __name__ == "__main__":
    client = cClient()
    if client.Bind('localhost', 59000) != True:
        exit()
    client.SendMessage()
    exit()
