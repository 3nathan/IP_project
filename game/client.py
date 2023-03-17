import socket
import pickle
import json

class Network:
    #functuion for accessing the server
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "13.40.119.55" 
        self.port = 10000
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    #calls the connect function
   # def getP(self):
    #    return self.p

    #standard TCP connection function that returns the received message    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(1024).decode()
        except:
            pass
    #fuction that sends the data to the server and receives pickled data
    #def sendf(self, data):
        #try:
            #self.client.send(str.encode(data))
            #return pickle.loads(self.client.recv(2048*2))
        #except socket.error as e:
            #print(e)
    
  # send a message 
    def sendm(self, data):
        try:
            msg = data
            self.client.send(msg.encode(data))
            msg_received = self.client.recv(1024) #we can add the decode in this line
            msg_received = msg_received.decode()
        except socket.error as e:
            print(e)
    
    def receive(self,):
        data = self.client.recv(1024)
        data_str = data.decode('utf-8')
        scores = json.loads(data_str)






#n = Network()
#def main():
#    run = True
#    clock = pygame.time.Clock()
#    player = int(n.getP())
#    print("You are player", player)
#
#    while run:
#        clock.tick(120)
#        #message version
#        n.sendm(score)
#        
#        #receives the data for the game 
#        try:
#            game = n.sendf("get")
#        except:
#            run = False
#            print("Couldn't get game")
#            break
#
#        if game.reset()==0:
#            pygame.time.delay(5000)
#            try:
#                game = n.sendf("reset")
#            except:
#                run = False
#                print("Couldn't get game")
#                break
#        
#
#    
#        for event in pygame.event.get():
#                if event.type == KEYDOWN:
#                    if event.key == K_ESCAPE or event.key == K_q:
#                        run = False
#                elif event.type == pygame.QUIT:
#                    run = False
#        
#        updateObjects(arrows)
#        updateScreen(screen, arrows)
#
#main() 
#         
    

