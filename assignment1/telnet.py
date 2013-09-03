# telnet program example
import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
def register() :
    user_name = raw_input('enter a user name:')
    user_name = '1' + user_name
    s.send(user_name)

#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages'
    #prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    if data[0] == '1' :
                        print 'welcome message \n'
                    sys.stdout.write(data)
                    #prompt()
             
            #user entered a message
            else :
                msg_type = int(raw_input())
                if msg_type == 1:
                    print 'msg type = 1'
                    register()
                else if msg_type == 2:
                    print 'msg type = 2'
                    addFileList()
                else if msg_type == 3:
                    search()
                else
                    "msg_type not valid"
                #msg = sys.stdin.readline()
                #s.send(msg)
                #prompt()
                