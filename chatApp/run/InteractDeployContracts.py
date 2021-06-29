import threading
import time

from SmartContractInteract import SmartContractInteract as SMC
from UserAuth import UserAuth as userAuth
import os

filepath = os.path.dirname(os.path.abspath(__file__))




class InteractDeployContracts(SMC):
    def __init__(self, username, password):
        global filepath
        SMC.__init__(self)
        self.account = None
        self.chatRoomName = None
        print(username, password)
        u = userAuth()
        self.userAuthVariable = userAuth()
        self.username = username
        if u.Login(username, password) == False:
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

    def getMessages(self):
        while True:
            if self.username==None:
                break
            time.sleep(5)
            print("\n")
            print(self.callGetMessagesFromChatRoomByName(self.chatRoomName))
            print("\n")
        

    def interactRoom(self):
        inputSetter = "(" + self.username + ":" + self.chatRoomName + ")>>>"
        while True:
            time.sleep(2)
            query = input(inputSetter)
            if query == "add":
                chatRoomName = input("chatroom_name: ")
                username = input("username: ")
                self.transactAddUserToChatRoomByUserName(chatRoomName, username)
            if query == "getMsg":
                print(self.callGetMessagesFromChatRoomByName(self.chatRoomName))
            if query == "exitRoom":
                break
            else:
                msg = query
                self.transactAddMessage(self.chatRoomName, self.username, msg)

    def run(self):
        inputSetter = "(" + self.username + ")>>>"
        while True:
            value = input(inputSetter)
            if value == "exit":
                self.userAuthVariable.Logout()
                self.username=None
                return
            if value == "createChatRoom":
                chatRoomName = input("name: ")
                self.createChatRoom(chatRoomName)
            if value == "owner":
                chatRoomName = input("name: ")
                self.getChatRoomOwner(chatRoomName)
            if value == "switchRoom":
                name = input("Switch ChatRoom: ")
                self.chatRoomName = name
                fetchMsgThread = threading.Thread(target=self.getMessages)
                fetchMsgThread.start()
                interactRoom = threading.Thread(target=self.interactRoom)
                interactRoom.start()

            else:
                print(value)

    def createChatRoom(self, name):
        SMC.transactDeployChatRoom(self, name)

    def getChatRoomOwner(self, name):
        print(SMC.callGetChatRoomOwner(self, name))

    def EnterChatRoom(self):
        print("chatRoom")
