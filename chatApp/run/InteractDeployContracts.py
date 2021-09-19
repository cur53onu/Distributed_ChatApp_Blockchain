import threading
import sys
from SmartContractInteract import SmartContractInteract as SMC
from UserAuth import UserAuth as userAuth
import os
from print_output import *

filepath = os.path.dirname(os.path.abspath(__file__))
run_threads = True



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
        self.msgSize = 0
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

    def getMsg(self):
        self.msgSize = len(self.callGetMessagesFromChatRoomByName(self.chatRoomName))
        global run_threads
        while run_threads:
            curr_msg = self.callGetMessagesFromChatRoomByName(self.chatRoomName)
            if self.msgSize < len(curr_msg):
                for i in range(self.msgSize,len(curr_msg)):
                    msg = curr_msg[i]
                    if self.username != msg[0]:
                        printMsg(msg[0],msg[1])
                self.msgSize = len(curr_msg)
        print('quitting getMsg...')
        return

    def interactRoom(self):
        listenMsgThread = threading.Thread(target=self.getMsg)
        listenMsgThread.start()
        global run_threads
        run_threads = True
        while run_threads:
            # query = input(inputSetter)
            query = sys.stdin.readline().rstrip('\n')
            if query == "add":
                chatRoomName = self.chatRoomName
                username = input("username: ")
                self.transactAddUserToChatRoomByUserName(chatRoomName, username)
            if query == "getMsg":
                curr_msg = self.callGetMessagesFromChatRoomByName(self.chatRoomName)
                print(len(curr_msg))
                print(curr_msg)
            if query == "exitRoom":
                # os.system("kill `pgrep xterm`")
                run_threads = False
                break
            else:
                msg = query
                self.transactAddMessage(self.chatRoomName, self.username, msg)
        listenMsgThread.join()
        return

    def run(self):
        inputSetter = "(" + self.username + ")>>>"
        while True:
            value = input(inputSetter)
            if value == "exit":
                self.userAuthVariable.Logout()
                self.username=None
                os._exit(1)
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
                # fetchMsgThread = threading.Thread(target=self.getMessages)
                # fetchMsgThread.start()
                # interactRoom = threading.Thread(target=self.interactRoom)
                # interactRoom.start()
                self.interactRoom()


            else:
                print(value)

    def createChatRoom(self, name):
        SMC.transactDeployChatRoom(self, name)

    def getChatRoomOwner(self, name):
        print(SMC.callGetChatRoomOwner(self, name))

    def EnterChatRoom(self):
        print("chatRoom")
