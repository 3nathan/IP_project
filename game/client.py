import socket
import pickle
import json

class Client:
    #functuion for accessing the server
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "13.40.114.182" 
        self.port = 10053
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
    def send_message(self, data):
            msg = json.dumps(data)
            self.client.send(bytes(msg, encoding = "utf-8"))
      

    def receive_message(self):
        msg_received = self.client.recv(1024) #we can add the decode in this line
        msg_received = msg_received.decode()
        return msg_received
    
    def receive_json(self):
        data = self.client.recv(1024).decode('utf-8')
        scores = json.loads(data)
        return scores







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
    

