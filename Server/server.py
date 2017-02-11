##########################SIAMH 02/06/2017##################################################
# Server communicates with Client via TCP and provides answers for valid commands received
# It creates in-memory cache from database
# It validates received commands
# It performs the operations on the cahce
# In the end, when the server stops, then it commits cache to the database
# Depending on the requirement, the server can handle request from multiple clients

import socket
import sys
from Expressions import ParseExpr, UnitTesting_Expr
from Memory import ProcessQuery
from thread import*

def helpmenu():
    return "<------Four Basic operations ------>\n"\
    "Format of SET Operation: SET KEY=VALUE\n"\
    "Format of EXPAND Operation: EXPAND MSG, ${KEY}\n"\
    "Format of DELETE Operation: DEL KEY\n"\
    "Format of LIST Operation: LIST\n"\
    "<---------------------------------->"


# Per thread communciation function, which process the query and return the result to the client.
# When it leaves the communciation, it decreases the numer of clients.
def clientthread(connection, lock, client):
    while True:
        data = connection.recv(512)
        if data == 'help':
            connection.sendall(helpmenu())
            continue

        # 'exit' is the token to be sent when client is set to leave the communciation.
        if data == 'exit':
            print 'Client left', client
            server.decrease()
            connection.close()
            exit()
            break

        # Parsing the query from client
        ids, key, value, data, needlock = ParseExpr(data)
        try:
            # needlock is set to true in case we are settign the value of a key
            # or deleting a key. Other two operation is read operations.

            # Critical region : needs to lock before chaging the cache.
            if needlock:
                lock.acquire()
            msg = ProcessQuery(ids, key, value, data)
            if needlock:
                lock.release()

            # releasing the final answers to the client.
            connection.sendall(msg)
        except KeyboardInterrupt:
            interrupt_main()
        except error:
            print "Thread Specific error."
            server.decrease()
            connection.close()
            exit()
        except:
            print "Connection is lost."
            server.decrease()
            connection.close()
            exit()

class cServer(object):
    numofThreads = 0 # number of clients currently requesting
    MaxNumOfClients = 0 # maximum number of clients allowed
    lock_t = allocate_lock() # lock for writing operations
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.numofThreads = 0
        UnitTesting_Expr()

    def decrease(self):
        self.numofThreads = self.numofThreads - 1
        self.AcceptConnection()

    def Bind(self, address, port, maxClients):
        try:
            server_address = (address, port)
            # No threads are set to deamon, and as it waits infintely for receving messages
            # from clients, the clean up of threads are not properly handled here (use join
            # for all the threads to finsih their job).
            print 'Press Ctrl + C to quit'
            print 'starting up on ' + str(address) + ' port: ' + str(port)
            self.sock.bind(server_address)
            self.sock.listen(maxClients)
            self.MaxNumOfClients = maxClients
            return True
        except:
            print 'failed to connect with ' + str(address) + ' on port: ' + str(port)
            return False

    def RejectConnection(self):
        try:
            connection, client_address = self.sock.accept()
            connection.close()
        except KeyboardInterrupt:
            print 'Service is interrupted'
            exit()

    def AcceptConnection(self):
        while True:
            # Wait for a connection
            if self.numofThreads < self.MaxNumOfClients:
                print 'waiting for a new connection'
            else:
                print 'Server cannot accpet more connection'
                self.RejectConnection()
                continue

            try:
                connection, client_address = self.sock.accept()
                start_new_thread(clientthread,(connection, self.lock_t, client_address, ))
                self.numofThreads = self.numofThreads + 1
            except KeyboardInterrupt:
                    print "Service is interrupted."
                    return
            except:
                print "Could not bind with " + str(client_address)
                continue

if __name__ == "__main__":
    server = cServer()
    if server.Bind('localhost', 59000, 3) != True:
        exit()
    server.AcceptConnection()
    exit()
