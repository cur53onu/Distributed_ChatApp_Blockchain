import json
from web3 import Web3


class UserAuthBase:
    def __init__(self):
        with open('JSON_Files/data.json') as data_file:
            data = json.load(data_file)
            self.deploy_contracts_address = data['contract_deploycontracts_address']
            self.contract_profile_address = data['contract_profile_address']
            self.infura_node_url = data['infura_node_url']
            self.web3 = Web3(Web3.HTTPProvider(self.infura_node_url))
            self.tempdatafilename = data['user_temporarydata_file_name']
            self.userdatafilename = data['user_privatekey_file_name']
            self.user_account = None

    def getContractProfileAddress(self):
        return self.deploy_contracts_address

    def getWeb3(self):
        return self.web3

    def getContractInstance(self, name):
        filepath = 'JSON_Files/' + name
        con = ""
        with open(filepath) as f:
            data = json.load(f)
            abi = data['interface']
            address = self.web3.toChecksumAddress(self.contract_address)
            con = self.web3.eth.contract(address=address, abi=abi)
        f.close()
        return con

    def getProfileContractInstance(self,name,addr):
        filepath = 'JSON_Files/' + name
        con = ""
        with open(filepath) as f:
            data = json.load(f)
            abi = data['interface']
            address = self.web3.toChecksumAddress(addr)
            con = self.web3.eth.contract(address=address, abi=abi)
        f.close()
        return con

    def customTransact(self, function):
        with open(self.getTemporaryDataFileName(), "rb") as binary_file:
            data = binary_file.read()
            ax = (self.web3.eth.account.privateKeyToAccount(data))
            self.user_account = ax
        builtTransaction = function.buildTransaction({
            'from': self.user_account.address,
            'nonce': self.web3.eth.getTransactionCount(self.user_account.address),
            'gas': 1728712,
            'gasPrice': self.web3.toWei('21', 'gwei')})
        try:
            signed = self.user_account.signTransaction(builtTransaction)
            tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
            return True,self.user_account
        except ValueError:
            print("No Balance!!!")
            return False
    def getTemporaryDataFileName(self):
        return self.tempdatafilename

    def getUserDataFileName(self):
        return self.userdatafilename
