import socket
import _thread
import threading
import pickle
import boto3
from boto3.dynamodb.conditions import Key
import json
#install these libraries on server !!!!!!!!!!!!!

lobby = list()
song = 0
foo = 0
print("We're in tcp server...")
#select an IP address and server port
server = '0.0.0.0'
port = 10053
#create a welcoming socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the server to the localhost at port server_port 
server_socket.bind((server, port))
server_socket.listen(2)
#ready message
print('Server running on port ', port)

client_sockets = set()
events = {}

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
        scores.append((item['user'], int(item['info']['score'])))
    print(scores)
    upto = min(5, len(scores))
    scores.sort(key = lambda x: x[1])
    return scores[:upto]

# TODO: send index of arrow hit to both players
def client_thread(clientsocket, addr):
    global lobby
    global song
    while True:
        rec_data = clientsocket.recv(1024).decode('utf-8')
        data = json.loads(rec_data)
        print("thread", data)
        user, label = data[0], data[1]
        if label == "_songname":
            if user != 0:
                song = data[0]
            msg = json.dumps(song)
            clientsocket.send(bytes(msg, encoding="utf-8"))
        elif label == "_user":
            if user not in lobby:
                lobby.append(user)
            client_data = json.dumps(["Updated table"])
            clientsocket.send(bytes(client_data, encoding="utf-8"))
        elif label == "_retreive":
            lobby_data = json.dumps(lobby)
            clientsocket.send(bytes(lobby_data, encoding="utf-8"))
        elif label == "_putscore":
            username, score = user[0], user[1]
            response = store_score(song, username, score, 0)
        elif label == "_getscores":
            #retrieve top 5 highest scores for that song and send it to every client
            top_scores = get_scores(song)
            print(top_scores)
            data = json.dumps(top_scores)
            clientsocket.send(bytes(data, encoding="utf-8"))
            if foo:
                song = 0
                events.clear()
                lobby.clear()
            foo += 1
            if foo == 2:
                foo = 0
        else:
            #update clients with scores
            if label:
                thisevents = events.get(user, [])
                thisevents.append(label)
                events[user] = thisevents
            for u in lobby:
                if u != user:
                    otheruser = u
            otherevents = events.get(otheruser, [])
            client_data = json.dumps(otherevents)
            if not label:
                events[otheruser] = []
            clientsocket.send(bytes(client_data, encoding="utf-8"))
    clientsocket.close()


#Now the main server loop 
while True:
    connection_socket, caddr = server_socket.accept()
    rec_data = connection_socket.recv(1024).decode()
    msg = json.dumps(["starting new thread"])
    connection_socket.send(bytes(msg, encoding="utf-8"))
    client_sockets.add(connection_socket)
    _thread.start_new_thread(client_thread, (connection_socket, caddr))
