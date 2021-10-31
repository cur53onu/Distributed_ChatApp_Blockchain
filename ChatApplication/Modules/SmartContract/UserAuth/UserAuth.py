import os
import ast
import os.path

from termcolor import colored
from ChatApplication.Modules.SmartContract.Core.SmartContractInteract import SmartContractInteract as SMC
from ChatApplication.Modules.PrintOutput.print_output import printOutput
filepath = os.path.dirname(os.path.abspath(__file__))
import json

class UserAuth(SMC):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None
        self.user_account = None
        self.user_public_address = None
        self.profileContractInstance = None
        self.userProfileAddress = None
        self.userProfileContractFilePath = 'JSON_Files/Profile.json'


    def getUserProfileContractInstance(self):
        profileContractFilePath = self.userProfileContractFilePath
        con = None
        with open(profileContractFilePath) as f:
            data = json.load(f)
            abi = data['interface']
            address = self.web3.toChecksumAddress(self.userProfileAddress)
            con = self.web3.eth.contract(address=address, abi=abi)
        f.close()
        print(con)
        return con

    def callGetUsername(self):
        return self.profileContractInstance.functions.getUsername().call()

    def callUserAddressExist(self):
        return self.getMainContractInstance().functions.checkAccountExistWithPublicAddress().call({'from': self.user_public_address})

    def callGetUserData(self):
        return self.profileContractInstance.functions.getUserData().call({'from': self.user_public_address})

    def transactRegisterUser(self, username, password):
        return self.customTransact(self.getMainContractInstance().functions.deployProfile(username, password))

    def userExist(self, name):
        value = self.getMainContractInstance(
        ).functions.getDeployedProfileAddressByName(name).call()
        if value == "0x0000000000000000000000000000000000000000":
            return False
        return True

    def callGetUserProfileAddress(self):
        return self.getMainContractInstance().functions.getUserProfileAddress().call({'from': self.user_public_address})


    def PrepRegister(self):
        if not os.path.isfile(self.getTemporaryDataFileName()):
            # web3= SMC.getWeb3(self)
            account = self.web3.eth.account.create()
            printOutput("Your Account is Ready For Registration!!!" +
                        "\n>>> Your Public Address is: " + str(account.address) +
                        "\n>>> Transfer some ether to this and come back for registration!!!" + "\n\n" + str(
                            account.address) + "\n\n", "blue")
            privatekey_binary = account.privateKey
            with open(self.getTemporaryDataFileName(), "wb") as binary_file:
                binary_file.write(privatekey_binary)
            self.user_account = account
            self.user_public_address = self.user_account.address
            return account
        else:
            with open(self.getTemporaryDataFileName(), "rb") as binary_file:
                data = binary_file.read()
                account = (self.web3.eth.account.privateKeyToAccount(data))
                self.user_account = account
                self.user_public_address = account.address
                print('temp file present\nAccount address: ', account.address)

    def Register(self):
        self.PrepRegister()
        if self.callUserAddressExist():
            printOutput(
                "User account with " + self.user_public_address +
                " already exist!!!\nCannot create new account with same public address",
                "red")
            return

        if (self.web3.eth.getBalance(self.user_account.address)) == 0:
            printOutput("Wallet empty add some ethers and come back"
                        + " Public Address : " + str(self.user_account.address), 'red')
            printOutput("Waiting till u transfer ", 'red')
            while (self.web3.eth.getBalance(self.user_account.address)) == 0:
                pass
            print('\nEthers received.')
            print('Current balance: ',
                  (self.web3.eth.getBalance(self.user_account.address)))
        strRegister = ">>> Register <<<\nMake sure your account have ethers" + \
            "\nEnter Username and Password"
        printOutput(strRegister, "blue")
        self.username = input("username:")
        self.password = input("password:")
        if not os.path.exists(self.getTemporaryDataFileName()):
            printOutput("Run Prepearation Register", 'red')
            return
        if self.userExist(self.username):
            print(colored(">>> Username exist choose different username", 'red'))
            return

        encrypted_password = self.user_account.encrypt(self.password)
        value, account_received = self.transactRegisterUser(
            self.username, str(encrypted_password))

        if value == True:
            printOutput("Registered successfully..." + "\n>>> Name " + self.username
                        + "\n>>> Public Address: " + str(self.user_account.address), "blue")
        cnt = 0
        while not self.callUserAddressExist():
            cnt += 1

    def Login(self):
        self.username = input("username:")
        self.password = input("password:")

        # self.username = "cur53"
        # self.password = "cur53"

        profile_addr = self.userExist(self.username)
        if not profile_addr:
            printOutput("No user", 'red')
            return

        self.user_public_address = input('Required public address: ')

        # self.user_public_address = "0x85c4345d4177d4f689317B908634881f43f01CCb"
        self.userProfileAddress = self.callGetUserProfileAddress()
        self.profileContractInstance = self.getUserProfileContractInstance()
        print(self.callGetUsername())

        res = ast.literal_eval(self.callGetUserData())
        try:
            privatekey_binary = self.web3.eth.account.decrypt(
                res, self.password)
            self.user_account = self.web3.eth.account.privateKeyToAccount(
                privatekey_binary)
            printOutput("Logged in..." + "\n>>> Name " + self.username
                        + "\n>>> Public Address: " +
                        str(self.user_account.address)
                        + "\n>>> Balance : " + str(self.web3.eth.getBalance(self.user_account.address)), "blue")

            return True
        except ValueError:
            printOutput("Wrong Password", 'red')
        return False

    def Logout(self):
        if self.user_account:
            self.user_account = None
        else:
            printOutput("Not Logged in", 'red')
            return
        printOutput("Logged Out!!!", 'blue')
