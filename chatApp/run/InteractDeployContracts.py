from SmartContractInteract import SmartContractInteract as SMC
from UserAuth import UserAuth as userAuth
from print_output import *
from TerminalHandler import terminalHandlerMain
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

    def interactRoom(self):
        terminalHandlerMain(self.chatRoomName, self.username)

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
                self.interactRoom()
            else:
                print(value)

    def createChatRoom(self, name):
        SMC.transactDeployChatRoom(self, name)

    def getChatRoomOwner(self, name):
        print(SMC.callGetChatRoomOwner(self, name))

    def EnterChatRoom(self):
        print("chatRoom")
