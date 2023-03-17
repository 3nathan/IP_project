import socket
import _thread
import pickle
import boto3
from boto3.dynamodb.conditions import Key
import json
#install these libraries on server !!!!!!!!!!!!!

lobby = list()

print("We're in tcp server...")
#select an IP address and server port
server = '0.0.0.0'
port = 10005

#create a welcoming socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the server to the localhost at port server_port 
server_socket.bind((server, port))
server_socket.listen(2)

#ready message
print('Server running on port ', port)

### at start of game
# start game when both clients have pressed start
# take in song name and username
# start loop
# initialize dictionary

### every iteration
# update dictionary
# send dictionary information to each client

### at the end of loop
# store entries in database
# return to client top 5 scores for the song

#keep track of clients
client_sockets = set()
scores = {"player0": 0, "player1": 0}

def store_score(song, user, score, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.Table('Scores')
    response = table.put_item(
       Item={
            'song': song,
            'user': user,
            'info': {
                'score': score
            }
        }
    )
    return response


def get_scores(song, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.Table('Scores')
    response = table.query(
        KeyConditionExpression=Key('song').eq(song)
    )
    scores = []
    for item in response['Items']:
        scores.append((item['user'], item['info']['score']))
    upto = min(5, len(scores))
    return scores.sort(key = lambda x: x[1])[:upto]


# TODO: send index of arrow hit to both players
def client_thread(clientsocket, addr):
    while True:
        rec_data = clientsocket.recv(1024).decode('utf-8')
        data = json.loads(rec_data)
        print(data)
        user, label = data[0], data[1]
        if label == "_songname":
            song = data[0]
        #if game has finished
        elif label == "_user":
            global lobby
            lobby.append(user)
        elif label == "_retreive":
            global lobby
            lobby_data = json.dumps(lobby)
            for client in client_sockets:
                client.send(bytes(lobby_data, encoding="utf-8"))
        elif label == "_stop":
            #insert score into database
            response = store_score(song, user, scores[user], 0)
            del scores[user]
            #retrieve top 5 highest scores for that song and send it to every client
            top_scores = get_scores(song)
            data = json.dumps(top_scores)
            for client in client_sockets:
                client.send(bytes(data, encoding="utf-8"))
                global lobby
                lobby.clear()
        else:
            #update clients with scores
            client_data = json.dumps(data)
            for client in client_sockets:
                client.send(bytes(client_data, encoding="utf-8"))
    clientsocket.close()


#Now the main server loop 
while True:
    connection_socket, caddr = server_socket.accept()
    print() 
    client_sockets.add(connection_socket)
    _thread.start_new_thread(client_thread, (connection_socket, caddr))
