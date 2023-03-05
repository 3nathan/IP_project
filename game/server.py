import socket
import thread
import pickle
#install these libraries on server !!!!!!!!!!!!!


print("We're in tcp server...")
#select an IP address and server port
server = '0.0.0.0'
port = 12000

#create a welcoming socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the server to the localhost at port server_port 
server_socket.bind((server, port))
server_socket.listen(2)

#ready message
print('Server running on port ', port)



#keep track of clients
client_sockets = []
scores = dict()

def client_thread(clientsocket, addr):
    while True:
        data = clientsocket.recv(1024).decode()
        #handle data here
        if data:
            scores[addr] = scores.get(addr, 0) + 1

        #update database


        # send the data to the client
        for client in client_sockets:
            pass
        connection_socket.send(cmsg.encode())
    clientsocket.close()


#Now the main server loop 
while True:
    connection_socket, caddr = server_socket.accept() 
    print("Connected to:", caddr) #Ana
    thread.start_new_thread(client_thread, (connection_socket, caddr))
