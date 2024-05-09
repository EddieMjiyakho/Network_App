import socket
import threading
from person import person     # Import the 'person' class from the 'person' module

DisconnectMSG = "DISCONNECT!" # A constant for disconnecting messages
key="12rty345key"             # A key used for communication
list=[]                       # A list to store client information
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
serverSocket.bind(('',5555))  # Bind the socket to a specific address and port
clients=[]                    # List to store connected clients

# Function to handle individual clients
def handle_client ( Person):
    conn=Person.connection   # Get the connection object from the person object
    clientAddress=Person.address
    print(f"[NEW CONNECTION] {clientAddress} is connected. ")
    connected = True

         
    while connected :
        # Receive and decode message from the client
        msg = eval(conn.recv(1024).decode('utf-8'))

        if msg :
            print(f"[{clientAddress}] : {msg} ") 
            if msg["request"] == "exit":
                Person.disconnect()
                connected = False
                conn.send("x".encode("utf-8"))

            elif msg["request"]=="visiblity":
                 Person.visibility=msg["arg"]

            elif msg["request"]=="yes" or msg["request"]=="no":
                continue

            elif msg["request"] == "Active_Clients":
                list.clear()
                # Iterate through clients to get active, non-blocked users
                for user in clients:
                    if user.visibility=="public" and user.state!="away" and user.is_blocked(Person.name)==False:
                        list.append(user.name+"->"+user.state)
                    print(user.name)

                # Send the list of active clients to the requesting client
                conn.send(','.join(list).encode("utf-8"))  

            elif msg["request"] =="chat_request":
                    check=True
                    for user in clients:
                        name=user.name
                        if msg["arg"]==name and user.state!="away" and user.is_blocked(Person.name)==False: #checks if name is the same as the word in msg 
                            check=False 
                            connection=user.connection

                            connection.send(key.encode("utf-8"))# trying send key to the friend 
                            message=eval(connection.recv(1024).decode('utf-8'))
                            print("waiting")
                            if  message["request"]=="no":
                                conn.send("user refused".encode("utf-8")) 
                                print("user refused")
                            if message["request"] =="yes":
                                ip=user.address#saves the client ip address to ip
                                conn.send(ip.encode("utf-8"))#send the ip address if user didnot refuse
                                break
                                
                    if check==True: conn.send("no such user".encode("utf-8"))
            
            elif msg["request"] =="block_user":
                check=False

                for user in clients:
                    name=user.name
                    if msg["arg"]==name: #checks if name is the same as the word in msg 
                        print(user)
                        check=True
                        Person.block(user)
                if user==False:
                    message="user does not exist"
                    conn.send(message.encode("utf-8"))
                else:
                    message=msg["arg"]+" been has blocked"
                    conn.send(message.encode("utf-8"))

            elif msg["request"] =="unblock_user":

                if Person.is_blocked(msg["arg"])==False:
                    message="user does not exist"
                    conn.send(message.encode("utf-8"))
                else:
                    Person.unblock(msg["arg"])
                    message=msg["arg"]+" been has unblocked"
                    conn.send(message.encode("utf-8"))         
                    
    conn.close()
    

# Function to initiate user registration or login
def initiate(service_req,conn,address):
    print("initiating..")

    user =""
    while user=="" :
        nameBool=False
        user=""
        for Saved_user in clients:#checks if the name has been taken by another user
            if Saved_user.name == service_req["name"]: 
                nameBool=True
                user=Saved_user
                break

        if service_req["request"]=="register" and nameBool==True:  #if user is trying to register and is name taken 
            user=""
            message="Username has been taken"
            conn.send(message.encode("utf-8"))
                    
        elif service_req["request"]=="register" and nameBool==False: #if user is trying to register and is name not taken
                
                user= person(service_req["name"],service_req["password"]) # creates a new user 
                user.connect(address,conn)
                clients.append(user) #adds the new user to the clients
                message="You have been registered"
                conn.send(message.encode("utf-8"))
             
        elif service_req["request"]=="login" and nameBool==False: #if user is trying to login and is name does not exist:
            message="the username you have entered does not exist"
            print(message)
            conn.send(message.encode("utf-8"))

        elif service_req["request"]=="login" and nameBool==True: #if user is trying to login and is exists
                    if user.password == service_req["password"]:
                        message="Login approved"
                        print(message)
                        user.connect(address,conn)
                        conn.send(message.encode("utf-8"))           
                    else:
                        message="The password you enterred is incorrect"
                        user=""
                        print(message)
                        conn.send(message.encode("utf-8"))

        if user=="": #user is empty listens for the next request 
            print("thing is working")
            service_req = eval(conn.recv(1024).decode('utf-8'))
    # clients.append(user) #adds user to the client list
    print(user.name)
    handle_client(user)# goes to hand client


#protocol {request:type , massage: argument, type }
    
#(name, ip, conn)
def start():
    serverSocket.listen()
    while True :
        conn, clientAddress = serverSocket.accept()
        service_req = eval(conn.recv(1024).decode('utf-8'))

        thread = threading.Thread(target = initiate , args= (service_req,conn,clientAddress[0]))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
print("[SERVER IS LISTENING...]")
start()
