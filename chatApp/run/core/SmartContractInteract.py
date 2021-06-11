import json
from web3 import Web3


class SmartContractInteract:
    def __init__(self):
        self.file_path = 'JSON_Files/DeployContracts.json'
        self.gas = 1728712
        with open('JSON_Files/data.json') as data_file:
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

    def customTransact(self, function):
        with open(self.getTemporaryDataFileName(), "rb") as binary_file:
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
            return True, self.user_account
        except ValueError:
            print("No Balance!!!")
            return False

    def getTemporaryDataFileName(self):
        return self.tempdatafilename

    def getUserDataFileName(self):
        return self.userdatafilename

    def transactAddUser(self, user_name, encrypted_data):
        instance=SmartContractInteract()
        instance.customTransact(instance.getContractInstance().functions.deployProfiles(user_name,encrypted_data))

    def userExist(self, name):
        instance = SmartContractInteract()
        value = instance.getContractInstance().functions.getDeployedProfileAddressByName(name).call()
        if value=="0x0000000000000000000000000000000000000000":
            return False
        return True

    def callGetUserData(self,name):
        return self.getContractInstance().functions.getDeployedProfileData(name).call()
