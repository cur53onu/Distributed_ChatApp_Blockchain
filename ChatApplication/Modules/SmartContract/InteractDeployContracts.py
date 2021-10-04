from ChatApplication.Modules.SmartContract.UserAuth.UserAuth import UserAuth
from ChatApplication.Modules.PrintOutput.print_output import *
from ChatApplication.Modules.TerminalHandler.TerminalHandler import terminalHandlerMain
filepath = os.path.dirname(os.path.abspath(__file__))
run_threads = True



class InteractDeployContracts(UserAuth):
    def __init__(self):
        UserAuth.__init__(self)
        self.account = None
        self.chatRoomName = None
        self.msgSize = 0

    def interactRoom(self):
        terminalHandlerMain(self, self.chatRoomName, self.username)

    def run(self):
        if self.Login():
            inputSetter = "(" + self.username + ")>>>"
            while True:
                value = input(inputSetter)
                if value == "exit":
                    self.Logout()
                    os.exit(1)
                    return
                elif value == "createChatRoom":
                    chatRoomName = input("name: ")
                    self.transactDeployChatRoom(chatRoomName)
                elif value == "owner":
                    chatRoomName = input("name: ")
                    print(self.callGetChatRoomOwner(chatRoomName))
                elif value == "switchRoom":
                    name = input("Switch ChatRoom: ")
                    self.chatRoomName = name
                    self.interactRoom()
                elif value == "addUser":
                    chatRoomName = input("chat room name: ")
                    username = input("username : ")
                    self.transactAddUserToChatRoomByUserName(chatRoomName, username)
                else:
                    print(value)

    def EnterChatRoom(self):
        print("chatRoom")
