from ChatApplication.Modules.SmartContract.Core.SmartContractInteract import SmartContractInteract as SMC
import json

from datetime import date


class ChatRoom(SMC):
    def __init__(self, chatRoomContractAddress, userProfileAddress, userAccount):
        super().__init__()
        self.userPresent = False
        if chatRoomContractAddress != "0x0000000000000000000000000000000000000000":
            self.chatRoomContractInstance = self.getContractInstanceOfChatRoom(contract_address=chatRoomContractAddress)
            if self.callCheckUserPresent(userProfileAddress=userProfileAddress, userAccount=userAccount):
                self.user_account = userAccount
                self.userProfileAddress = userProfileAddress
                self.chatRoomContractAddress = chatRoomContractAddress
                self.chatRoomName = self.getChatRoomName()
                self.userPresent = True



    def getContractInstanceOfChatRoom(self, contract_address):
        con = None
        filepath = 'JSON_Files/ChatRoom.json'
        with open(filepath) as f:
            data = json.load(f)
            abi = data['interface']
            try:
                address = self.web3.toChecksumAddress(contract_address)
                con = self.web3.eth.contract(address=address, abi=abi)
            except Exception as e:
                print(e)
        f.close()
        return con

    def validateUser(self):
        return self.userPresent

    def callCheckUserPresent(self, userProfileAddress, userAccount):
        return self.chatRoomContractInstance.functions.checkUserPresent(userProfileAddress).call({'from': userAccount.address})

    def getChatRoomName(self):
        return self.chatRoomContractInstance.functions.getName().call()

    def getMessages(self):
        value = self.chatRoomContractInstance.functions.getAllMessages().call(
            {'from': self.user_account.address})
        return value

    def addMsg(self, message):
        today = str(date.today())
        self.customTransact(self.chatRoomContractInstance.functions.addMessage(
            self.user_account.address, self.chatRoomName, message, today))
        return
