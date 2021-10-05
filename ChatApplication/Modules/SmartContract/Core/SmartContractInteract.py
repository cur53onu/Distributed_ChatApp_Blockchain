import json
from ChatApplication.Modules.PrintOutput.print_output import *
from web3 import Web3
import os
import inspect
from datetime import date

class SmartContractInteract:
    def __init__(self):
        self.file_path = 'JSON_Files/DeployContracts.json'
        self.gas = 1728712
        self.account=None
        FILENAME = 'JSON_Files/data.json'
        with open(FILENAME) as data_file:
            data = json.load(data_file)
            self.deploy_contracts_address = data['contract_deploycontracts_address']
            self.infura_node_url = data['infura_node_url']
            self.web3 = Web3(Web3.HTTPProvider(self.infura_node_url))
            self.tempdatafilename = data['user_temporarydata_file_name']
            self.userdatafilename = data['user_privatekey_file_name']
            self.user_account = None

    def getContractProfileAddress(self):
        return self.deploy_contracts_address

    def getWeb3(self):
        return self.web3

    def getContractInstance(self):
        filepath = self.file_path
        con = None
        with open(filepath) as f:
            data = json.load(f)
            abi = data['interface']
            address = self.web3.toChecksumAddress(self.deploy_contracts_address)
            con = self.web3.eth.contract(address=address, abi=abi)
        f.close()
        return con

    def customTransact(self, function, filename=''):
        Filename = self.getUserDataFileName()
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        fn_caller = calframe[1][3]
        if fn_caller == 'Register':
            Filename = self.getTemporaryDataFileName()

        with open(Filename, "rb") as binary_file:
            data = binary_file.read()
            ax = (self.web3.eth.account.privateKeyToAccount(data))
            self.user_account = ax

        builtTransaction = function.buildTransaction({
            'from': self.user_account.address,
            'nonce': self.web3.eth.getTransactionCount(self.user_account.address),
            'gas': self.gas,
            'gasPrice': self.web3.toWei('21', 'gwei')})
        try:
            signed = self.user_account.signTransaction(builtTransaction)
            tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
            return True, tx_hash
        except ValueError as v:
            print(v)
            print("No Balance!!!")
            return False, None

    def getTemporaryDataFileName(self):
        return self.tempdatafilename

    def getUserDataFileName(self):
        return self.userdatafilename

    def checkStatusOfTransaction(self,tx_hash):
        debugOutput('Sending','red')
        while True:
            trx = self.web3.eth.get_transaction(tx_hash)
            if trx.blockNumber is not None:
                break
        printOutput('Transaction sent!!!','green')
        return

    def transactAddUser(self, user_name, encrypted_data):
        self.customTransact(self.getContractInstance().functions.deployProfiles(user_name, encrypted_data))

    def userExist(self, name):
        value = self.getContractInstance().functions.getDeployedProfileAddressByName(name).call()
        if value == "0x0000000000000000000000000000000000000000":
            return False
        return True

    def callGetUserData(self,addr):
        return self.getContractInstance().functions.getDeployedProfileData().call({'from': addr})

    def transactDeployChatRoom(self, name, roomType):
        val = self.customTransact(self.getContractInstance().functions.deployChatRoom(name,roomType))
        if val[0]:
            self.checkStatusOfTransaction(val[1])
    def callGetChatRoomOwner(self, name, addr):
        return self.getContractInstance().functions.getChatRoomOwner(name).call({'from':addr})

    def transactAddUserToChatRoomByUserName(self,chatroom_name,username):
        val = self.customTransact(self.getContractInstance().functions.addUserToChatRoomByUserName(chatroom_name,username))
        if val[0]:
            self.checkStatusOfTransaction(val[1])
        return
    def transactAddMessage(self,chatroom_name,message):
        today = str(date.today())
        val = self.customTransact(self.getContractInstance().functions.addMessage(chatroom_name,message,today))
        # if val[0]:
        #     self.checkStatusOfTransaction(val[1])
        return

    def transactSetChatRoomType(self, chatroom_name, roomType):
        val = self.customTransact(self.getContractInstance().functions.setChatRoomType(chatroom_name, roomType))
        if val[0]:
            self.checkStatusOfTransaction(val[1])

    def callGetMessagesFromChatRoomByName(self,chatroom_name, addr):
        return self.getContractInstance().functions.getMessagesFromChatRoomByName(chatroom_name).call({'from': addr})

    def callgetAllChatRooms(self):
        return self.getContractInstance().functions.getDeployedChatRoomInfo().call()