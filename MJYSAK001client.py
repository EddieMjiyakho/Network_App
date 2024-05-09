import socket
import threading 
import time

PORT = 5555
DisconnectMSG = "DISCONNECT!"
key="12rty345key"
ClientIP="localhost"
ADDRESS = ( ClientIP, PORT )
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDRESS)
recmsgs=[]

# Function for the chat functionality
def chat(ip=""):
    Port2 = 8888
    address =(ip,Port2)
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    # Function to send a file to a specific IP and port
    def send_file(file_path, destination_ip, destination_port):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024) # Read 1024 bytes at a time
                Socket.sendto(data, (destination_ip, destination_port))
                if not data:
                    break
    
    # Function to receive a file and save it
    def receive_file(save_path):
        save_path="Rec_"+save_path
        with open(save_path, 'wb') as file:
            while True:
                data, addr = Socket.recvfrom(1024) # Receive up to 1024 bytes
                if not data:
                    break
                file.write(data)

    # Function to continuously listen for incoming messages
    def listen():
        while True:
            try:
                message, serverAddress =  Socket.recvfrom(2048)
                if "file:" in message.decode():
                    print("receiving file...")
                    path=message.decode().split(":")[1]
                    print(path)
                    receive_file(path)
                print(message.decode() )

            except OSError as e:
                print("You have logged out of the chat")
                break

    # Function to send messages and handle file sending
    def sender():
        Socket.bind(('', Port2))
        print ('The server is ready to receive')
        message, address  = Socket.recvfrom(2048)
        print(message.decode())
        return address
    
    # Set up communication based on whether an IP is provided or not
    if ip == "":address =sender()
    else: Socket.connect(address)

    my_thread = threading.Thread(target=listen)
    my_thread.start()
    message=""
    while  message !="x":
        message = input("send:")
        Socket.sendto(message.encode(),address)
        if "file:" in message:
            
            path=message.split(":")[1]
            print(path)
            print(address[1])
            send_file(path,address[0],address[1])
            print("sending file....")
    Socket.close()  
    return      

# Function to continuously wait for messages from the server
def waiting():

     while True:
        s = clientSocket.recv(1024).decode()
        if s=="x":
            return
        if s==key:
            print(s)
            s=""
        elif s!="":
            recmsgs.append(s)
        s=""

# Function to send a message to the server
def send(msg) :
    message = msg.encode('utf-8')
    clientSocket.send(message)

def main():

    my_thread = threading.Thread(target=waiting)
    my_thread.start()
    message=""
    while True:
        # User input for registration or login
        request=input("Choose an option 1. Register or 2. Login: ")

        if request!="1" and request !="2" :continue
        if request=="1": request= "register"
        if request=="2": request="login"

        name=input("Enter your Name: ")
        password=input("Enter your Password: ")
        serv_req={"request":request ,"name":name , "password":password}

        send(str(serv_req))

        # Wait for a response from the server
        while True:
            if len(recmsgs)>0:
                break

        answer=recmsgs[0]
        del recmsgs[0] 
        print(answer)
        if answer=="You have been registered" or answer =="Login approved": break
      
    data=""

    while data.lower()!="5": 

        data= input("___Choose option from menu__\nMenu:\n1.change visibility\n2.list active clients\n3.start chat\n4.block/unblock user\n5.logout\n")
       #protocol{"request:type: args:..."}

        if data =="yes" or data =="no": 
            serv_req={"request":data}
            send(str(serv_req))
            send(str(serv_req))
            if data=="no":
                continue
            else:
                chat()

        elif data=="1":
            while True:
                data=input("choose visibilty:\n1.Public\n2.Private\n")
                if data=="1":
                    data="public"
                    break
                if data=="2":
                    data="private"
                    break 
                if data=="x":break

                print("invalid input")
            if data=="x":break
            serv_req={"request":"visiblity" , "arg": data}
            send(str(serv_req))

        elif data =="2":
            serv_req={"request":"Active_Clients"}
            send(str(serv_req))
            time.sleep(0.5)
            recmsg=recmsgs[0]
            del recmsgs[0]
            print("-Active Users-")
            for names in recmsg.split(","):
                counter=1
                print(str(counter)+"."+names)
                counter=counter+1

        elif data=="3" :
            data=input("Enter your friends name:")
            serv_req={"request":"chat_request" , "arg": data}
            send(str(serv_req))
            print("waiting for reply.")
            while True:
                if len(recmsgs)>0:
                    break

            recmsg=recmsgs[0]
            print(recmsg, "this is the message")
            del recmsgs[0] 

            if recmsg == "no such user": print(data,"was not found")
            elif recmsg=="user refused": print(data, "refused request")
            else: chat(recmsg)

        elif data=="4":
            request=""
            while True:
                request=input("Choose an option:\n1.block\n2.unblock\n")
                if request=="1":
                    request="block_user"
                    break
                if request=="2":
                    request="unblock_user"
                    break
                if request=="x":
                    break
            if request=="x":break

            data=input("Enter user name: ")
            serv_req={"request":request, "arg":data }
            send(str(serv_req))
            time.sleep(0.5)
            recmsg=recmsgs[0]
            del recmsgs[0]
            print(recmsg)

    # Logout and exit the program
    serv_req={"request":"exit"}
    send(str(serv_req))
    print("you have been logged out")

main()