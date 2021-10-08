from ChatApplication.Modules.SmartContract.UserAuth.UserAuth import UserAuth
from ChatApplication.Modules.PrintOutput.print_output import *
from ChatApplication.Modules.TerminalHandler.TerminalHandler import *
filepath = os.path.dirname(os.path.abspath(__file__))
run_threads = True



class InteractDeployContracts(UserAuth):
    def __init__(self):
        UserAuth.__init__(self)
        self.chatRoomName = None
        self.msgSize = 0

    def interactRoom(self):
        my_term = RoomTerminal(self, self.chatRoomName, self.username, self.public_address)
        my_term.loop = urwid.MainLoop(my_term)
        listenMsgThread = threading.Thread(target=my_term.getMsg)
        listenMsgThread.start()
        my_term.loop.run()
        try:
            listenMsgThread.join()
        except Exception as e:
            print("exit")
        return
    def roomInfo(self):
        printOutput('Chat Rooms Info', 'yellow')
        printOutput('Public chat rooms are green and private are red in color', 'yellow')
        listOfRooms = self.callgetAllChatRooms(self.public_address)
        if not listOfRooms:
            printOutput("No Rooms Available\nPlease create some rooms to get started!!!", "red")
            return
        for i in range(0, len(listOfRooms)):
            color="green"
            roomName, roomOwnerUsername, roomOwnerAddress, roomType = listOfRooms[i]
            if roomType:
                color="red"
            printOutput("ChatRoomName: "+ str(roomName) +" ChatRoomOwner: " + str(roomOwnerUsername), color)

    def run(self):
        if self.Login():
            self.roomInfo()
            inputSetter = "(" + self.username + ")<<<"
            while True:
                value = input(inputSetter)
                if value == "exit":
                    self.Logout()
                    os.exit(1)
                    return
                elif value == "createChatRoom":
                    chatRoomName = input("name: ")
                    print("\nChat Room Type\n1)Private\n2)Public")
                    chatRoomType = input("type: ")
                    if chatRoomType== '1':
                        self.transactDeployChatRoom(chatRoomName, True)
                    elif chatRoomType== '2':
                        self.transactDeployChatRoom(chatRoomName, False)
                    else:
                        print("Use 1 or 2 for Private and Public respectively")
                # elif value == "owner":
                #     chatRoomName = input("name: ")
                #     print(self.callGetChatRoomOwner(chatRoomName))
                elif value=="setRoomType":
                    chatRoomName = input("name: ")
                    print("\nChat Room Type\n1)Private\n2)Public")
                    chatRoomType = input("type: ")
                    if chatRoomType == '1':
                        self.transactSetChatRoomType(chatRoomName, True)
                    elif chatRoomType == '2':
                        self.transactSetChatRoomType(chatRoomName, False)
                    else:
                        print("Use 1 or 2 for Private and Public respectively")
                elif value == "switchRoom":
                    name = input("Switch ChatRoom: ")
                    self.chatRoomName = name
                    if self.getAuthorizationForRoom(self.chatRoomName, self.username, self.public_address):
                        self.interactRoom()
                    else:
                        printOutput("You are not authorized to enter in "+ self.chatRoomName +" room", "red")
                elif value == "addUser":
                    chatRoomName = input("chat room name: ")
                    username = input("username : ")
                    self.transactAddUserToChatRoomByUserName(chatRoomName, username)
                elif value == "allRooms":
                    self.roomInfo()
                else:
                    print(value)

    def EnterChatRoom(self):
        print("chatRoom")
