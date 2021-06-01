# from chatty.smart_contracts_interact.core.SmartContractInteract import SmartContract as SMC
from .UserAuthBase import UserAuthBase as BASE


class Profile(BASE):
    def __init__(self):
        BASE.__init__(self)
        self.contract_address = BASE.getContractProfileAddress(self)
        self.web3 = BASE.getWeb3(self)

    def getContractInstance(self):
        return BASE.getContractInstance(self, "DeployContracts.json")
        # return BASE.getContractInstance(self, "Profile.json")

    def getProfileContractInstance(self,addr):
        return BASE.getProfileContractInstance(self,"Profile.json",addr)


    def transactAddUser(self, user_name, encrypted_data):
        instance=Profile()
        instance.customTransact(instance.getContractInstance().functions.DeployProfiles(user_name,encrypted_data))
        # instance = Profile()
        # instance.customTransact(instance.getContractInstance().functions.addUser(user_name, encrypted_data))

    def callGetUsers(self, name):
        instance = Profile()
        return instance.getContractInstance().functions.getDeployedProfileByName(name).call()
        # return instance.getContractInstance().functions.getUserByName(name).call()

    def callGetUserData(self,name,addr):
        instance = Profile()
        return instance.getProfileContractInstance(addr).functions.getUserByName(name).call()

