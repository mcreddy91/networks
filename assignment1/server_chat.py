# Tcp Chat server
 
import socket, select
global CONNECTION_LIST
CONNECTION_LIST = []
global PEER_LIST
PEER_LIST  = {}
global Files
Files = {}
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

def welcome (sock_new):
    welcome_message = "-------------------------------------------------------------------------\n" + "                     Welcome to FileSharer                               \n" + "-------------------------------------------------------------------------\n" + "* press 1 to Register\n" + "* press 2 to share a file list\n" + "* press 3 to search for a file\n"
    welcome_message = "1" + welcome_message
    sock_new.send(welcome_message)

def register(name, sock_new):
    print 'request accepted for user name ' + name
    if name in PEER_LIST:
        sock_new.send("2User Name has been taken already")
    else:
        PEER_LIST[name] = sock_new
        sock_new.send("2Successfully Registered")

def addFileList(message, sock) :
    entries = []
    
    sock_name = ''
    entries = message.split('\n')
    print 'here i am'
    num = len(entries)
    for key in PEER_LIST.keys() :
        if PEER_LIST[key] == sock :
            sock_name = key
    print str(num) + " entries to be added in " + sock_name
    for entry in entries:
        entryBreakDown = []
        entryBreakDown = entry.split(' ')
        print 'filename : ' + entryBreakDown[0] + ' owner : ' + sock_name + ' path : ' + entryBreakDown[1] 

if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    
    
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                welcome(sockfd)
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        print " data is : " + data
                        if data[0] == '1':
                            register(data[1:], sock)
                        elif data[0] == '2':
                            addFileList(data[1:-1], sock)
                        elif data[0] == '3':
                            search(data[1:])             
                except:
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()