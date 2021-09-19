import json
import sys
from print_output import *

from web3 import Web3
import os
from datetime import date
filepath = os.path.dirname(os.path.abspath(__file__))


class SmartContractInteract:
    def __init__(self):
        global filepath
        self.file_path = '../JSON_Files/DeployContracts.json'
        self.gas = 1728712
        self.account=None
        FILENAME = os.path.join(os.path.dirname(__file__), '../JSON_Files/data.json')
        with open(FILENAME) as data_file:
            data = json.load(data_file)
            self.deploy_contracts_address = data['contract_deploycontracts_address']
            self.infura_node_url = data['infura_node_url']
            self.web3 = Web3(Web3.HTTPProvider(self.infura_node_url))
            self.tempdatafilename = '../' + data['user_temporarydata_file_name']
            self.userdatafilename = '../' + data['user_privatekey_file_name']
            self.user_account = None
        try:
            FILENAME = os.path.join(os.path.dirname(__file__), '../JSON_Files/userdata.txt')
            with open(FILENAME, "rb") as data_file:
                web3 = self.getWeb3()
                data = data_file.read()
                act = (web3.eth.account.privateKeyToAccount(data))
                self.account = act
        except FileNotFoundError:
            print("FileNotFoundError")
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

    def customTransact(self, function):
        Filename=self.getUserDataFileName()
        instance=SmartContractInteract()
        if instance.account==None:
            Filename=self.getTemporaryDataFileName()

        with open(Filename, "rb") as binary_file:
            data = binary_file.read()
            ax = (instance.web3.eth.account.privateKeyToAccount(data))
            instance.user_account = ax

        builtTransaction = function.buildTransaction({
            'from': instance.user_account.address,
            'nonce': instance.web3.eth.getTransactionCount(instance.user_account.address),
            'gas': instance.gas,
            'gasPrice': instance.web3.toWei('21', 'gwei')})
        try:
            signed = instance.user_account.signTransaction(builtTransaction)
            tx_hash = instance.web3.eth.sendRawTransaction(signed.rawTransaction)
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
        instance = SmartContractInteract()
        instance.customTransact(instance.getContractInstance().functions.deployProfiles(user_name, encrypted_data))

    def userExist(self, name):
        instance = SmartContractInteract()
        value = instance.getContractInstance().functions.getDeployedProfileAddressByName(name).call()
        if value == "0x0000000000000000000000000000000000000000":
            return False
        return True

    def callGetUserData(self, name):
        return self.getContractInstance().functions.getDeployedProfileData(name).call()

    def transactDeployChatRoom(self, name):
        instance = SmartContractInteract()
        instance.customTransact(instance.getContractInstance().functions.deployChatRoom(name))

    def callGetChatRoomOwner(self, name):
        instance = SmartContractInteract()
        return instance.getContractInstance().functions.getChatRoomOwner(name).call()

    def transactAddUserToChatRoomByUserName(self,chatroom_name,username):
        instance=SmartContractInteract()
        val = instance.customTransact(instance.getContractInstance().functions.addUserToChatRoomByUserName(chatroom_name,username))
        if val[0]:
            self.checkStatusOfTransaction(val[1])
        return
    def transactAddMessage(self,chatroom_name,username,message):
        instance=SmartContractInteract()
        today = str(date.today())
        val = instance.customTransact(instance.getContractInstance().functions.addMessage(chatroom_name,username,message,today))
        if val[0]:
            self.checkStatusOfTransaction(val[1])
        return
    def callGetMessagesFromChatRoomByName(self,chatroom_name):
        instance=SmartContractInteract()
        return instance.getContractInstance().functions.getMessagesFromChatRoomByName(chatroom_name).call()