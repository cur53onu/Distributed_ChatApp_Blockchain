from SmartContractInteract import SmartContractInteract as SMC
from UserAuth import UserAuth as userAuth
import os

filepath = os.path.dirname(os.path.abspath(__file__))


class InteractDeployContracts(SMC):
    def __init__(self,username,password):
        global filepath
        SMC.__init__(self)
        self.account = None
        print(username,password)
        u = userAuth()
        self.userAuthVariable = userAuth()
        if u.Login(username, password)==False:
            return
        try:
            FILENAME = os.path.join(os.path.dirname(__file__), '../JSON_Files/userdata.txt')
            with open(FILENAME, "rb") as data_file:
                web3 = SMC.getWeb3(self)
                data = data_file.read()
                # print(data)
                act = (web3.eth.account.privateKeyToAccount(data))
                self.account = act


        except FileNotFoundError:
            print("Error")
            return

    def run(self):
        inputSetter = "(" + self.account.address + ")>>>"
        while True:
            value = input(inputSetter)
            if value == "exit":
                self.userAuthVariable.Logout()
                return
            if value=="createChatRoom":
                chatRoomName=input("name: ")
                self.createChatRoom(chatRoomName)
            if value=="owner":
                chatRoomName = input("name: ")
                self.getChatRoomOwner(chatRoomName)
            if value=="add":
                chatRoomName = input("chatroom_name: ")
                username=input("username: ")
                self.transactAddUserToChatRoomByUserName(chatRoomName,username)
            if value=="sendMsg":
                chatRoomName=input("chatroom_name: ")
                username = input("username: ")
                msg = input("msg: ")
                self.transactAddMessage(chatRoomName,username,msg)
            if value=="getMsg":
                chatRoomName = input("chatroom_name: ")
                print(self.callGetMessagesFromChatRoomByName(chatRoomName))


            else:
                print(value)


    def createChatRoom(self,name):
        SMC.transactDeployChatRoom(self,name)

    def getChatRoomOwner(self,name):
        print(SMC.callGetChatRoomOwner(self,name))
    def EnterChatRoom(self):
        print("chatRoom")

