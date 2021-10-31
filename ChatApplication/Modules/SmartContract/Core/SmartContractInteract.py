import json
import time

from ChatApplication.Modules.PrintOutput.print_output import *
from web3 import Web3
import os
import inspect
from datetime import date

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SmartContractInteract(metaclass=Singleton):
    def __init__(self):
        self.file_path = 'JSON_Files/MainContract.json'
        self.tempdatafilename = 'JSON_Files/temp.txt'
        self.gas = 1728712
        self.user_account = None
        FILENAME = 'JSON_Files/data.json'
        with open(FILENAME) as data_file:
            data = json.load(data_file)
            self.deploy_contracts_address = data['contract_deploycontracts_address']
            self.infura_node_url = data['infura_node_url']
            self.web3 = Web3(Web3.HTTPProvider(self.infura_node_url))


    def getWeb3(self):
        return self.web3

    def getMainContractInstance(self):
        filepath = self.file_path
        con = None
        with open(filepath) as f:
            data = json.load(f)
            abi = data['interface']
            address = self.web3.toChecksumAddress(self.deploy_contracts_address)
            con = self.web3.eth.contract(address=address, abi=abi)
        f.close()
        return con

    def customTransact(self, function, userAccount=None):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        fn_caller = calframe[1][3]
        if (fn_caller == 'transactRegisterUser'):
            Filename = self.getTemporaryDataFileName()
            with open(Filename, "rb") as binary_file:
                data = binary_file.read()
                ax = (self.web3.eth.account.privateKeyToAccount(data))
                self.user_account = ax
        elif userAccount != None:
            self.user_account = userAccount
            print(self.user_account)

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

    def checkStatusOfTransaction(self,tx_hash):
        debugOutput('Sending','red')
        while True:
            trx = self.web3.eth.get_transaction(tx_hash)
            if trx.blockNumber is not None:
                break
        printOutput('Transaction sent!!!','green')
        return

    def transactDeployChatRoom(self, name, roomType, user_account):
        self.customTransact(self.getMainContractInstance().functions.deployChatRoom(name, roomType), user_account)
        time.sleep(10)
        # if val[0]:
        #     self.checkStatusOfTransaction(val[1])

    # def transactAddMessage(self,chatroom_name,message):
    #     today = str(date.today())
    #     val = self.customTransact(self.getContractInstance().functions.addMessage(chatroom_name,message,today))
    #     # if val[0]:
    #     #     self.checkStatusOfTransaction(val[1])
    #     return

    # def transactSetChatRoomType(self, chatroom_name, roomType):
    #     val = self.customTransact(self.getContractInstance().functions.setChatRoomType(chatroom_name, roomType))
    #     if val[0]:
    #         self.checkStatusOfTransaction(val[1])

    # def callGetMessagesFromChatRoomByName(self,chatroom_name, username, addr):
    #     value = None
    #     if self.getAuthorizationForRoom(chatroom_name, username, addr):
    #         value = self.getContractInstance().functions.getMessagesFromChatRoomByName(chatroom_name).call({'from': addr})
    #     return value

    def getDeployedChatRoomAddressByName(self, chatRoomName, userPublicAddress):
        return self.getMainContractInstance().functions.getDeployedChatRoomAddressByName(chatRoomName).call({'from': userPublicAddress})

    def callgetAllChatRooms(self, public_address):
        data = []
        listOfAddresses = self.getMainContractInstance().functions.getAllDeployedChatRooms().call({'from': public_address})
        for address in listOfAddresses:
            data.append(self.getMainContractInstance().functions.getDeployedChatRoomInfo(address).call({'from': public_address}))
        return data

    # def getAuthorizationForRoom(self, chatRoomName, username ,public_address):
    #     return self.getContractInstance().functions.checkUserPresent(chatRoomName, username).call({'from':public_address})