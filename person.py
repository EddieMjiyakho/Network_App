import socket

class person:
    def __init__(self , name , password):
        self.name=name
        self.password=password
        self.visibility="public"
        self.address=""
        self.connection=""
        self.state="away"
        self.blocked=[]
    
    def connect(self,Address, Connection):
        self.address=Address
        self.connection=Connection
        self.state="active"
    def disconnect(self):
        self.connection=""
        self.address=""
        self.state="away"
    def block(self ,Person):
        self.blocked.append(Person)
    def unblock(self,name):
        counter=0
        for user in self.blocked:
            if user.name ==name:
                del self.blocked[counter]
            counter=counter+1


    def is_blocked(self,name):
        for user in self.blocked:
            if user.name ==name:
                return True
        return False
    

