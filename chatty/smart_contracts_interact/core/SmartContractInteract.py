import json
from web3 import Web3
import sys
class SmartContract:
    def __init__(self):
        with open('JSON_Files/data.json') as data_file:
            data = json.load(data_file)
            self.contract_address = data['contract_chatroom_address']
            self.contract_profile_address=data['contract_profile_address']
            self.user_private_key = data['user_private_key']
            self.infura_node_url = data['infura_node_url']
            self.web3 = Web3(Web3.HTTPProvider(self.infura_node_url))
            self.userdatafilename = data['user_privatekey_file_name']
            self.tempdatafilename = data['user_temporarydata_file_name']
            # print(self.get_user_account().address,self.getBalance())
        try:
            # trying to open a file in read mode
            fo = open(self.userdatafilename, "rb")
            print("File opened")
        except FileNotFoundError:
            print("File does not exist")
            sys.exit(0)
    def customTransact(self,function):
        builtTransaction = function.buildTransaction({
            'from': self.get_user_account().address,
            'nonce': self.web3.eth.getTransactionCount(self.get_user_account().address),
            'gas': 1728712,
            'gasPrice': self.web3.toWei('21', 'gwei')})

        signed = self.get_user_account().signTransaction(builtTransaction)
        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)

    def get_user_account(self):
        return self.web3.eth.account.privateKeyToAccount(self.user_private_key)

    def getContractAddress(self):
        return self.contract_address

    def getContractProfileAddress(self):
        return self.contract_profile_address
    def getWeb3(self):
        return self.web3

    def getUserKey(self):
        return self.user_private_key

    def getContractInstance(self,name):
        filepath='JSON_Files/'+name
        con=""
        with open(filepath) as f:
            data = json.load(f)
            abi = data['interface']
            address = self.web3.toChecksumAddress(self.contract_address)
            con = self.web3.eth.contract(address=address, abi=abi)
        f.close()
        return con

    def getBalance(self):
        return (self.web3.eth.getBalance(self.get_user_account().address))

    def getUserDataFileName(self):
        return (self.userdatafilename)

    def getTemporaryDataFileName(self):
        return self.tempdatafilename
