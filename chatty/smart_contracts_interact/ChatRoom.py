from .core.SmartContractInteract import SmartContract as SMC


class ChatRoom(SMC):

    def __init__(self):
        SMC.__init__(self)
        self.contract_address = SMC.getContractAddress(self)
        self.web3 = SMC.getWeb3(self)

    def getContractInstance(self):
        return SMC.getContractInstance(self, "ChatRoom.json")

    def callGetName(self):
        instance = ChatRoom()
        return instance.getContractInstance().functions.getName().call()

    def callGetUsers(self):
        instance = ChatRoom()
        print('>>>', instance.getContractInstance().functions.getUsers().call(), end='\n')

    def transactAddUser(self, name,data):
        instance = ChatRoom()
        instance.customTransact(instance.getContractInstance().functions.addUser(name,data))

    def transactSetName(self, chatroom_name):
        instance = ChatRoom()
        prev = instance.getBalance()
        instance.customTransact(instance.getContractInstance().functions.setName(chatroom_name))
        print("Deducted: ", prev - instance.getBalance())
        print("Available ", instance.getBalance())


